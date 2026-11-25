from http import HTTPStatus

from fastapi import APIRouter, Depends
from ..services.produto_service import ProdutoService
from ..dependencies import get_service 
from ..models.produto import Produto

produtos_router = APIRouter(prefix="/v1/produtos", tags=["Produtos"])




@produtos_router.get("", status_code=HTTPStatus.OK)
def listar_todos(
    service: ProdutoService = Depends(get_service),
) -> list[Produto]:
    return service.get_all()


@produtos_router.get("/{id}", status_code=HTTPStatus.OK)
def listar_por_id(
    id: int,
    service: ProdutoService = Depends(get_service),
) -> Produto:
    return service.get_by_id(id)
 