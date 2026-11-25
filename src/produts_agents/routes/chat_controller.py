from http import HTTPStatus
from fastapi import APIRouter, Depends
from ..auth import get_current_user
from ..models.chat import ChatResponse, ChatRequest

chat_router = APIRouter(prefix=("/v1/chat"), tags=["Chat"])


@chat_router.post("", status_code=HTTPStatus.OK)
def enviar_mensagem(request: ChatRequest ,user_id: str = Depends(get_current_user)) -> ChatResponse:
    return ChatResponse(resposta=f"Olá {user_id}, sua mensagem foi recebida!")
