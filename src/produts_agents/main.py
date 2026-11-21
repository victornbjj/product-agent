from fastapi import FastAPI
from .routes.produto_controller import produtos_router 



app = FastAPI()


app.include_router(produtos_router)

