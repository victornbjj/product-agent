from http import HTTPStatus
from fastapi import APIRouter, Depends
from ..dependencies import verificar_rate_limit
from ..models.chat import ChatResponse, ChatRequest

chat_router = APIRouter(prefix=("/v1/chat"), tags=["Chat"])


@chat_router.post("", status_code=HTTPStatus.OK)
def enviar_mensagem(request: ChatRequest ,user_id: str = Depends(verificar_rate_limit)) -> ChatResponse:
    return ChatResponse(resposta=f"Olá {user_id}, sua mensagem foi recebida!")
