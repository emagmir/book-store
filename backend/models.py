from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field, PositiveInt
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List, Annotated
from bson import ObjectId


#authentication models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class CreateUserRequest(BaseModel):
    username: str
    password: str

class ForgotPasswordSchema(BaseModel):
    email: str
    password: str

#mongo models below

PyObjectId = Annotated[str, BeforeValidator(str)]

class User(BaseModel):
    _id: ObjectId
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username" : "johndoe12",
                "password" : "test12",
                "email": "jdoe@example.com",
                "full_name" : "John Doe",
                "disabled" : False
            }
        }

class UserInDB(User):
    hashed_password: str

#Below are the item models
    
class Book(BaseModel):
    #id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    book_title: str
    author: str
    genre: str
    file_id: str  
    # Add more attributes as needed, such as price, supplier information, etc.

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "book_title" : "Critique of pure reason",
                "author" : "Immanuel Kant",
                "genre" : "philosophy",
            }
        }

class BookInDB(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    book_title: str
    author: str
    genre: str
    file_id: str  
    # Add more attributes as needed, such as price, supplier information, etc.

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "book_title" : "Critique of pure reason",
                "author" : "Immanuel Kant",
                "genre" : "philosophy",
                "file_id" : "Stringhere"
            }
        }

class UpdateInventoryItemModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity_in_stock: Optional[int] =None # Ensure positive integer values
    location: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Updated Widget",
                "description": "A more detailed description of the widget",
                "quantity_in_stock": 150,
                "location": "Aisle 2, Shelf 1"
            }
        }