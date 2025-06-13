from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: Optional[UUID] = None
    password: str = ""
    email: EmailStr
    

    
