from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Drama"
    }
]

app = FastAPI()
app.title = "My application with FastAPI"

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length = 5, max_length = 15)
    overview: str = Field(min_length = 15, max_length = 30)
    year: int = Field(le = 2022)
    rating: float
    category: str
    
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

@app.get('/', tags = ['home'])
def message():
    return HTMLResponse("<h1>Hello world!</h1>")

@app.get('/movies', tags = ['movies'])
def get_movies():
    return JSONResponse(content = movies)

@app.get('/movies/{id}', tags = ['movies'])
def get_movie(id: int = Path(ge = 1, le = 2000)):
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(content = movie)
        
    return JSONResponse(content = [])

@app.get('/movies/', tags = ['movies'])
def get_movies_by_category(category: str = Query(min_length = 5, max_length = 15)):
    return [ movie for movie in movies if movie['category'] == category ]

@app.post('/movies', tags = ['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies

@app.put('/movies/{movie_id}', tags = ['movies'])
def update_movie(id: int, movie: Movie):
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = movie.title
            movie['overview'] = movie.overview
            movie['year'] = movie.year
            movie['rating'] = movie.rating
            movie['category'] = movie.category
            return movies
        
@app.delete('movies/{movie_id}', tags = ['movies'])
def delete_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return movies