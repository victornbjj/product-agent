from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

# id, nome, preco, descricao, quantidade_estoque

class Produto(BaseModel):
    id: int 
    nome: str = Field(min_length=1, max_length=30)
    preco: Decimal = Field(gt=0)
    descricao: str = Field(min_length=10, max_length=280)
    quantidade_estoque: int = Field(ge=0)



    @field_validator("nome", "descricao", mode="before")
    @classmethod
    def validar_campo_texto(cls, valor : str) -> str:

        if not isinstance(valor, str):
            raise ValueError("O valor do campo deve ser um texto.")
        
        nome_limpo = valor.strip()
        
        if not nome_limpo:
            raise ValueError("O campo de tipo texto não deve estar vazio.")
        return nome_limpo

    


