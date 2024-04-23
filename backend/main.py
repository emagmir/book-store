from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from connection import userdb
import warnings

app = FastAPI()

origins = [
    'https://localhost:3000'
]


def init_app():
    
    app = FastAPI()

    app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )

    import user_auth, user_profile, book_endpoints

    app.include_router(user_profile.router)
    app.include_router(user_auth.router)
    app.include_router(book_endpoints.router)

    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)

    return app

app = init_app()



