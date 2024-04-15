from typing import Optional
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length = 5, max_length = 15)
    overview: str = Field(min_length = 15, max_length = 30)
    year: int = Field(le = 2022)
    rating: float
    category: str