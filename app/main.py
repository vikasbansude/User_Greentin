from fastapi import FastAPI
from app.auth import auth
from app.api import tenant_controller
from app.models import models
from app.database.tenant_database import engine
from app.middleware.middleware import AdvMiddleware


app = FastAPI()

app.add_middleware(AdvMiddleware)

app.include_router(auth.router)
app.include_router(tenant_controller.router)

models.Base.metadata.create_all(bind=engine)
