from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    username : str
    password : str
    
class UpdateUserRequest(BaseModel):
    new_username: str