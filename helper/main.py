from fastapi import FastAPI
import helper.auth as auth
# import main
from api import tenant_controller
import database.models as models
from database.tenant_database import engine
from .middleware import AdvMiddleware 

app = FastAPI()

app.add_middleware(AdvMiddleware)

app.include_router(auth.router)
app.include_router(tenant_controller.router)

models.Base.metadata.create_all(bind=engine)
