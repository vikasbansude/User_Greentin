from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Tenants
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

import os
from dotenv import load_dotenv

# from fastapi.responses import RedirectResponse

load_dotenv()

router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateTenantRequest(BaseModel):
    tenantname : str
    password : str
    
class Token(BaseModel):
    access_token:str
    token_type:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_tenant(db:db_dependency, create_tenant_request: CreateTenantRequest):
    create_tenant_model = Tenants(
        tenantname = create_tenant_request.tenantname,
        hashed_password = pwd_context.hash(create_tenant_request.password)
    )
    db.add(create_tenant_model)
    db.commit()
    
# //////////////////////////////////////////////////////////////////////////////////////////////

# AuthN
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db:db_dependency):
    tenant = authenticate_tenant(form_data.username , form_data.password, db) #fun.  | username is predefined
    if not tenant:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate tenant")
    
    # if not tenant or tenant.tenantname != "Admin": #generating token for admin-only
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized: Only 'Admin' is allowed to log in.")
    
    token = create_access_token(tenant.tenantname, tenant.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) #fun.  | tenantname over here is w.r.to models.py
    
    return {"access_token":token, "token_type":"bearer"}
    
def authenticate_tenant(tenantName: str, password: str, db):
    tenant = db.query(Tenants).filter(Tenants.tenantname == tenantName).first() # | tenantname over here is w.r.to models.py
    if not tenant:
        return False
    if not pwd_context.verify(password, tenant.hashed_password):
        return False
    return tenant

def create_access_token(tenant_name:str, tenant_id: int, expires_delta: timedelta):
    encode = {'sub' : tenant_name, 'id' : tenant_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode['exp'] = expires.timestamp()
    # encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Decoding the token
async def get_current_tenant(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        tenant_name : str = payload.get('sub')
        tenant_id : int = payload.get('id')
        if tenant_name is None or tenant_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate tenant as its NULL.')
        #EXAMPLE FOR Restricting PERTICULAR TENANT
        # if tenant_name == 'Aryan' or tenant_id == 1:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='TENANT - Aryan is not AuthZ.')
        
        # if tenant_name != "Aryan":
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource.")
        
        if 'exp' not in payload or payload['exp'] < datetime.now(timezone.utc).timestamp():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired.')
        return {'tenantname': tenant_name, 'id': tenant_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate tenant.')
    
# @router.get("/me")
# async def read_current_tenant(current_tenant: Annotated[dict, Depends(get_current_tenant)]):
#     return {"tenantname": current_tenant['tenantname'], "id": current_tenant['id']}