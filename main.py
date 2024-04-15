from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from router.movie import movie_router
from router.auth import auth_router

app = FastAPI()
app.title = "My application with FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler) # Adding Middleware
app.include_router(movie_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

@app.get('/', tags = ['home'])
def message():
    return HTMLResponse("<h1>Hello world!</h1>")