from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routers import auth, users
from fast_zero.schemas import Message

app = FastAPI(
    title='Fast Zero', description='Curso de FastAPI Dunossauro', version='0.1'
)
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
