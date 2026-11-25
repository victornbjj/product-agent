from fastapi import Depends, HTTPException
from http import HTTPStatus 
from sqlalchemy.orm import  Session
from ..produts_agents.database import SessionLocal
from ..produts_agents.services.produto_service import ProdutoService
from ..produts_agents.repositories.produto_repository import ProdutoRepository
from ..produts_agents.repositories.rate_limit_repository import RateLimitRepository
from ..produts_agents.repositories.produto_cache_repository import ProdutoRedisRepository
from ..produts_agents.redis_cliente import client
from ..produts_agents.auth import get_current_user
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


def get_cache_repository(client: Redis = Depends(get_client)) -> ProdutoRedisRepository:
    return ProdutoRedisRepository(client)


def get_repository(session: Session = Depends(get_session)) -> ProdutoRepository:
    return ProdutoRepository(session)


def get_service(cache: ProdutoRedisRepository = Depends(get_cache_repository) ,repo: ProdutoRepository = Depends(get_repository)) -> ProdutoService:
    return ProdutoService(repo,cache)


def get_rate_limit_repository(client : Redis = Depends(get_client)) -> RateLimitRepository:
    return RateLimitRepository(client)


def verificar_rate_limit(user_id: str = Depends(get_current_user),
                          repo : RateLimitRepository = Depends(get_rate_limit_repository)) -> str :
    contador = repo.incrementar(user_id)
    if contador > LIMITE_REQUISICOES:
        raise HTTPException(status_code=HTTPStatus.TOO_MANY_REQUESTS, headers={"Retry-After": "60"})

    return user_id