from http.client import HTTPException
from fastapi import Depends, FastAPI, Body, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Coroutine, Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

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
app.version = "0.0.1"

class JWTBeater(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credentials are not valid!")

class User(BaseModel):
    email: str
    password: str

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

@app.post('/login', tags = ['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(content=token, status_code=200)

@app.get('/movies', tags = ['movies'], response_model = List[Movie], status_code=200, dependencies=[Depends(JWTBeater())])
def get_movies() -> List[Movie]:
    return JSONResponse(content = movies)

@app.get('/movies/{id}', tags = ['movies'], response_model = Movie)
def get_movie(id: int = Path(ge = 1, le = 2000)) -> Movie:
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(content = movie)
        
    return JSONResponse(content = [])

@app.get('/movies/', tags = ['movies'], response_model = List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length = 5, max_length = 15)):
    data = [ movie for movie in movies if movie['category'] == category ]
    return JSONResponse(content = data)

@app.post('/movies', tags = ['movies'], response_model = dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content = {"message: Movie registered"})

@app.put('/movies/{movie_id}', tags = ['movies'], response_model = dict)
def update_movie(id: int, movie: Movie) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = movie.title
            movie['overview'] = movie.overview
            movie['year'] = movie.year
            movie['rating'] = movie.rating
            movie['category'] = movie.category
            return JSONResponse(content = {"message: Movie updated"})
        
@app.delete('movies/{movie_id}', tags = ['movies'], response_model = dict)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return JSONResponse(content = {"message: Movie deleted"})