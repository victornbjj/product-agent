from ..models.produto import Produto
from sqlalchemy.orm import Session
from ..models.produto_entity import ProdutoEntity
from sqlalchemy import select


class ProdutoRepository:


    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Produto]:
        consulta = select(ProdutoEntity)
        entidades = self.session.scalars(consulta).all()
        return [Produto.model_validate(e) for e in entidades]

    def get_by_id(self, id: int) -> Produto | None:
        entidade = self.session.get(ProdutoEntity, id)
        if entidade is None:
            return None

        return Produto.model_validate(entidade)

