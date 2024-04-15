from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "My movie",
                "overview": "This is a description",
                "year": 2022,
                "rating": 5.0,
                "category": "action"
            }
        }