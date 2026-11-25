from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):

    mensagem: str = Field(min_length=1, max_length=1000)

    @field_validator("mensagem", mode="before")
    @classmethod
    def valida_campo_texto(cls, valor: str) -> str:

        if not isinstance(valor, str):
            raise ValueError("O valor do campo deve ser um texto.")

        mensagem_limpa = valor.strip()

        if not mensagem_limpa:
            raise ValueError("O campo de tipo texto não deve estar vazio.")

        return mensagem_limpa


class ChatResponse(BaseModel):

    resposta: str = Field(min_length=1)
