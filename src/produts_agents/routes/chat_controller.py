from http import HTTPStatus

from fastapi import APIRouter, Depends

from ..dependencies import get_chat_service, verificar_rate_limit
from ..services.chat_service import ChatService
from ..models.chat import ChatResponse, ChatRequest

chat_router = APIRouter(prefix="/v1/chat", tags=["Chat"])


@chat_router.post("", status_code=HTTPStatus.OK)
def enviar_mensagem(body: ChatRequest, user_id: str = Depends(verificar_rate_limit),
                     service: ChatService = Depends(get_chat_service),) -> ChatResponse:
    return service.responder(user_id, body.mensagem)
