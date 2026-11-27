

from ..produts_agents.repositories.interacao_repository import MongoRepository
from ..produts_agents.database import SessionLocal
from ..produts_agents.services.produto_service import ProdutoService
from ..produts_agents.repositories.produto_repository import ProdutoRepository
from ..produts_agents.repositories.rate_limit_repository import RateLimitRepository
from ..produts_agents.repositories.produto_cache_repository import ProdutoRedisRepository
from ..produts_agents.redis_cliente import client
from ..produts_agents.mongo_cliente import db
from ..produts_agents.auth import get_current_user
from ..produts_agents.repositories.interacao_repository import MongoRepository
from ..produts_agents.services.chat_service import ChatService
from ..produts_agents.tools.dispatcher import ToolDispatcher
from ..produts_agents.llm_cliente import client as llm_client, model as llm_model




from fastapi import Depends, HTTPException

from pymongo.collection import Collection
from sqlalchemy.orm import  Session
from http import HTTPStatus 
from redis import Redis


LIMITE_REQUISICOES = 10


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_client():
    return client

def get_collection() -> Collection:
    return db["interacoes"] 


def get_cache_repository(client: Redis = Depends(get_client)) -> ProdutoRedisRepository:
    return ProdutoRedisRepository(client)


def get_repository(session: Session = Depends(get_session)) -> ProdutoRepository:
    return ProdutoRepository(session)


def get_service(cache: ProdutoRedisRepository = Depends(get_cache_repository) ,repo: ProdutoRepository = Depends(get_repository)) -> ProdutoService:
    return ProdutoService(repo,cache)



def get_interacao_repository(collection: Collection = Depends(get_collection)) -> MongoRepository:
    return MongoRepository(colecao=collection)


def get_chat_service(
    repo: MongoRepository = Depends(get_interacao_repository),
    produto_service: ProdutoService = Depends(get_service),
) -> ChatService:
    tool_dispatcher = ToolDispatcher(produto_service)
    return ChatService(
        repo=repo,
        tool_dispatcher=tool_dispatcher,
        llm_client=llm_client,
        model=llm_model,
    )



def get_rate_limit_repository(client : Redis = Depends(get_client)) -> RateLimitRepository:
    return RateLimitRepository(client)


def verificar_rate_limit(user_id: str = Depends(get_current_user),
                          repo : RateLimitRepository = Depends(get_rate_limit_repository)) -> str :
    contador = repo.incrementar(user_id)
    if contador > LIMITE_REQUISICOES:
        raise HTTPException(status_code=HTTPStatus.TOO_MANY_REQUESTS, headers={"Retry-After": "60"})

    return user_id