from pydantic import ValidationError

from ..services.produto_service import ProdutoService
from .produto_tools import buscar_produto_por_id


class ToolDispatcher:
    def __init__(self, produto_service: ProdutoService):
        self.produto_service = produto_service

    def executar(self, nome: str, argumentos_json: str) -> dict[str, object]:
        if nome != "buscar_produto_por_id":
            raise ValueError(f"Ferramenta não permitida: {nome}")

        try:
            return buscar_produto_por_id(self.produto_service, argumentos_json)
        except ValidationError:
            return {"erro": "Argumentos inválidos para buscar_produto_por_id."}
