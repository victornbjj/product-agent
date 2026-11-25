from fastapi import FastAPI

from .routes.chat_controller import chat_router
from .routes.produto_controller import produtos_router

app = FastAPI()

app.include_router(produtos_router)
app.include_router(chat_router)