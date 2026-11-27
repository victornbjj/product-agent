from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field

from ..services.produto_service import ProdutoService


class BuscarProdutoPorIdArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    produto_id: int = Field(strict=True, gt=0, description="ID do produto.")


FERRAMENTAS = [
    {
        "type": "function",
        "name": "buscar_produto_por_id",
        "description": "Busca um produto pelo seu ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "produto_id": {
                    "type": "integer",
                    "description": "ID do produto.",
                }
            },
            "required": ["produto_id"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


def buscar_produto_por_id(
    produto_service: ProdutoService,
    argumentos_json: str,
) -> dict[str, object]:
    argumentos = BuscarProdutoPorIdArgs.model_validate_json(argumentos_json)

    try:
        produto = produto_service.get_by_id(argumentos.produto_id)
    except HTTPException as error:
        if error.status_code != 404:
            raise
        return {"erro": "Produto não encontrado."}

    return produto.model_dump(mode="json")
