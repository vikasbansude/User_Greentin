# from fastapi import Depends
# from typing import Annotated
# from sqlalchemy.orm import Session

# from helper.auth import get_current_tenant
# from database.tenant_database import get_db
# from database.models import Tenants
# # import database.models as models

# db_dependency = Annotated[Session, Depends(get_db)]
# tenant_dependency = Annotated[dict, Depends(get_current_tenant)]

# #importing the dto class
# from dto.tenant_class import CreateTenantRequest



# async def create_tenant(db:db_dependency, create_tenant_request: CreateTenantRequest):
#     create_tenant_model = Tenants(
#         tenantname = create_tenant_request.tenantname,
#         hashed_password = pwd_context.hash(create_tenant_request.password)
#     )
#     db.add(create_tenant_model)
#     db.commit()