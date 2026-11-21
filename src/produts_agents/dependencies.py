from fastapi import Depends
from sqlalchemy.orm import  Session
from ..produts_agents.database import SessionLocal
from  ..produts_agents.services.produto_service import ProdutoService
from ..produts_agents.repositories.produto_repository import ProdutoRepository


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_repository(session: Session = Depends(get_session)) -> ProdutoRepository:
    return ProdutoRepository(session)


def get_service(repo: ProdutoRepository = Depends(get_repository)) -> ProdutoService:
    return ProdutoService(repo)