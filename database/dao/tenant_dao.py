from fastapi import Depends, HTTPException, Request, status
from typing import Annotated
from sqlalchemy.orm import Session

#importing the database package
from database.tenant_database import get_db
from database.models import Tenants
import database.models as models

#importing the dto package
from dto.tenant_class import CreateTenantRequest
from dto.tenant_class import UpdateTenantRequest

#importing the auth package
from helper.auth import get_current_tenant
from helper.auth import pwd_context

db_dependency = Annotated[Session, Depends(get_db)]
tenant_dependency = Annotated[dict, Depends(get_current_tenant)]



async def create_tenant(tenant: tenant_dependency, db:db_dependency, create_tenant_request: CreateTenantRequest):
    
    if tenant["tenantname"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Only 'Admin' can view all tenants.")
    
    create_tenant_model = Tenants(
        tenantname = create_tenant_request.tenantname,
        hashed_password = pwd_context.hash(create_tenant_request.password)
    )
    db.add(create_tenant_model)
    db.commit()
    return {"msg": f"Tenant added successfully"}

# //////////////////////////

async def fetch_all_tenants(tenant: tenant_dependency, db : db_dependency):

    if tenant["tenantname"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Only 'Admin' can view all tenants.")
    
    tenants = db.query(Tenants).all()

    return {"tenants": [{"id": t.id, "tenantname": t.tenantname} for t in tenants]}

# //////////////////////////

async def update_tenant_name(tenant_id : int ,tenant: tenant_dependency, db: db_dependency, update_request: UpdateTenantRequest):
    # Fetch the current tenant from the database
    if tenant["tenantname"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied [Only Admin is AuthZ]")
    
    db_tenant = db.query(models.Tenants).filter(models.Tenants.id == tenant_id).first()

    if not db_tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")

    db_tenant.tenantname = update_request.new_tenantname
    db.commit()
    db.refresh(db_tenant)
    return {"msg": f"Tenant {tenant_id} name updated successfully", "new_tenantname": db_tenant.tenantname}

# //////////////////////////

async def delete_tenant(tenant_id: int, tenant : tenant_dependency, db : db_dependency):

    if tenant["tenantname"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied [Only Admin is AuthZ]")
    
    db_tenant = db.query(models.Tenants).filter(models.Tenants.id == tenant_id).first()
    
    if not db_tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to delete")
    
    db.delete(db_tenant)
    db.commit()
    return{"detail" : f"Tenant {tenant_id} deleted successfully"}