from ..repositories.interacao_repository import MongoRepository
from ..models.interacao_chat import InteracaoChat
from ..models.chat import ChatResponse
from pymongo.errors import PyMongoError 

import logging  
from time import perf_counter

logger = logging.getLogger(__name__)

class ChatService:

    def __init__(self, repo : MongoRepository):
        self.repo = repo


    def responder(self, user_id :str , mensagem: str) -> ChatResponse:

        inicio = perf_counter()

        resposta = f"Olá, {user_id}, sua mensagem: '{mensagem}' foi recebida."

        tempo_ms = int((perf_counter() - inicio ) * 1000)
        interacao = InteracaoChat(user_id=user_id, resposta=resposta, pergunta=mensagem, ferramentas=[], tempo_ms=tempo_ms)

        try:
            self.repo.inserir(interacao=interacao)
        except PyMongoError:
            logger.exception("Falha ao gravar historico")

        return ChatResponse(resposta=resposta)  
