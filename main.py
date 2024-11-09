from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
import models
from typing import Annotated, List
from database import SessionLocal,engine
# from models import Tenants
from auth import get_current_tenant
from auth import CreateTenantRequest

from sqlalchemy.orm import Session
import auth
from models import Tenants
from pydantic import BaseModel

# from starlette.middleware.base import BaseHTTPMiddleware

# import SimpleMiddleware
# from middleware import SimpleMiddleware 
from middleware import AdvMiddleware 


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)

# class TenantResponse(BaseModel):
#     tenantname: str
#     id : int

#     class Config:
#         orm_mode = True

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
tenant_dependency = Annotated[dict, Depends(get_current_tenant)]


# app.add_middleware(SimpleMiddleware)
app.add_middleware(AdvMiddleware)

@app.get("/test")
async def test_exception():
    raise HTTPException(status_code=403, detail="Unauthorized access")


@app.get("/", status_code=status.HTTP_200_OK)
async def tenant(tenant:tenant_dependency, db:db_dependency):
    if tenant is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    if tenant["tenantname"] == "Aryan":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: TENANT - Aryan not AuthZ.")
    return {"Tenant":tenant}

# @app.get("/get_tenants",response_model=List[TenantResponse])
# def get_tenant(db:Session=Depends(get_db)):
#     return db.query(Tenants).all()


# @app.get("/general-endpoint", status_code=status.HTTP_200_OK)
# async def general_endpoint(tenant: tenant_dependency):
#     return {"message": f"Hello, {tenant['tenantname']}! You have access to the general endpoint."}

@app.get("/view-all-tenants", status_code=status.HTTP_200_OK)
async def view_all_tenants(request: Request, tenant: tenant_dependency, db: Session = Depends(get_db)):

    if tenant["tenantname"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Only 'Admin' can view all tenants.")
    
    # Query the database for all tenants
    tenants = db.query(Tenants).all()
    # if "Authorization" in request.headers:
    #     return {"msg": request.headers["Authorization"]}
    # else:
    #     return {"error": "Authorization header not found"}
    
    # Return a list of tenant names (or other details as required)
    return {"tenants": [{"id": t.id, "tenantname": t.tenantname} for t in tenants]}


# ////////////////////
# @app.get("/view-all-tenants", status_code=status.HTTP_200_OK)
# async def view_all_tenants(request: Request, db: Session = Depends(get_db)):
#     tenant = request.state.tenant  # Access tenant info from request state
    
#     if tenant["tenantname"] != "Admin":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Only 'Admin' can view all tenants.")
    
#     tenants = db.query(Tenants).all()
#     return {"tenants": [{"id": t.id, "tenantname": t.tenantname} for t in tenants]}

# ////////////////////


@app.get("/admin-only", status_code=status.HTTP_200_OK)
async def admin_only_endpoint(tenant: tenant_dependency):
    if tenant["tenantname"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Only 'Admin' has access to this endpoint.")
    return {"message": "Welcome, Admin! You have exclusive access to this endpoint."}


# @app.get("/check-headers")
# async def check_headers(request: Request):
#     # Print all headers to see what's included in the request
#     print(request.headers)
#     # Optionally, check for the Authorization header specifically
#     if "accept" in request.headers:
#         return {"msg": request.headers["accept"]}
#     else:
#         return {"error": "Authorization header not found"}












class UpdateTenantRequest(BaseModel):
    new_tenantname: str

@app.put("/update_tenant_name", status_code=status.HTTP_200_OK)
async def update_tenant_name(
    tenant: tenant_dependency, 
    db: db_dependency, 
    update_request: UpdateTenantRequest
):
    # Fetch the current tenant from the database
    db_tenant = db.query(models.Tenants).filter(models.Tenants.id == tenant["id"]).first()

    if not db_tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")

    # Update the tenant's name
    db_tenant.tenantname = update_request.new_tenantname
    db.commit()
    db.refresh(db_tenant)

    return {"msg": "Tenant name updated successfully", "new_tenantname": db_tenant.tenantname}


# facenet_model = load_model("path_to_facenet_model/facenet_keras.h5")

# def generate_embedding(image):
#     """
#     Generate a 128-dimensional FaceNet embedding from an image.

#     Args:
#         image (np.array): Captured image in BGR format from OpenCV.

#     Returns:
#         np.array: 128-dimensional embedding vector.
#     """
#     # Convert BGR to RGB format as FaceNet model expects RGB images
#     rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
#     # Resize the image to the required FaceNet input size (160x160)
#     resized_image = cv2.resize(rgb_image, (160, 160))
    
#     # Normalize pixel values to be in the range [-1, 1]
#     normalized_image = (resized_image - 127.5) / 127.5

#     # Expand dimensions to fit FaceNet model input (1, 160, 160, 3)
#     face_input = np.expand_dims(normalized_image, axis=0)

#     # Generate embedding by passing the processed image through FaceNet
#     embedding = facenet_model.predict(face_input)
    
#     # Flatten the embedding array
#     return embedding.flatten()

# @app.post("/capture_photo/")
# def capture_photo(db: Session = Depends(get_db)):
#     # Initialize OpenCV to capture image from the default camera (usually index 0)
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         return {"error": "Camera could not be accessed"}
    
#     # Capture a single frame
#     ret, frame = cap.read()
#     if not ret:
#         cap.release()
#         return {"error": "Failed to capture image"}
    
#     # Release the camera
#     cap.release()

#     # Generate embedding from the captured image
#     embedding = generate_embedding(frame)

#     # Store metadata and embedding in MySQL
#     face_data = FaceData(
#         name="User's Name",
#         embedding=embedding.tolist(),  # Convert embedding to a list for storage
#         timestamp=datetime.now(),
#         attendance=True
#     )
#     db.add(face_data)
#     db.commit()

#     return {"message": "Image captured and processed successfully!"}