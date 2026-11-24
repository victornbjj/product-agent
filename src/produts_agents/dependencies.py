from fastapi import Depends
from sqlalchemy.orm import  Session
from ..produts_agents.database import SessionLocal
from  ..produts_agents.services.produto_service import ProdutoService
from ..produts_agents.repositories.produto_repository import ProdutoRepository
from ..produts_agents.repositories.produto_cache_repository import ProdutoRedisRepository
from ..produts_agents.redis_cliente import client
from redis import Redis




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