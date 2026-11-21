from pydantic import BaseModel, ConfigDict, Field, field_validator
from decimal import Decimal


model_config = ConfigDict(from_attributes=True)


class Produto(BaseModel):
    
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int 
    nome: str = Field(min_length=1, max_length=30)
    preco: Decimal = Field(gt=0)
    descricao: str = Field(min_length=10, max_length=200)
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

    


