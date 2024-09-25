from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(min_length=2, max_length=79)
    last_name: str = Field(min_length=2, max_length=79)
    email: EmailStr
    phone: str = Field(max_length=30)
    birthday: date
    address: str = Field(max_length=150)


class ContactResponse(ContactModel):
    id: int = Field(ge=1)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True