from pydantic import BaseModel, Field
from datetime import datetime, timezone


class InteracaoChat(BaseModel):
    id: str | None = None
    user_id: str = Field(min_length=1, max_length=50)
    pergunta: str = Field(min_length=1, max_length=1000)
    ferramentas: list[dict] = Field(default_factory=list)
    tempo_ms: int = Field(ge=0)
    resposta: str = Field(min_length=1)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))