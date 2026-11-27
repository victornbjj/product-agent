import json
import logging
from time import perf_counter

from openai import OpenAI
from pymongo.errors import PyMongoError

from ..models.chat import ChatResponse
from ..models.interacao_chat import InteracaoChat
from ..repositories.interacao_repository import MongoRepository
from ..tools.dispatcher import ToolDispatcher
from ..tools.produto_tools import FERRAMENTAS

logger = logging.getLogger(__name__)

MAX_TOOL_ROUNDS = 5


class ChatService:
    def __init__(
        self,
        repo: MongoRepository,
        tool_dispatcher: ToolDispatcher,
        llm_client: OpenAI,
        model: str,
    ):
        self.repo = repo
        self.tool_dispatcher = tool_dispatcher
        self.llm_client = llm_client
        self.model = model

    def responder(self, user_id: str, mensagem: str) -> ChatResponse:
        inicio = perf_counter()
        historico = [{"role": "user", "content": mensagem}]
        ferramentas_executadas: list[dict[str, str]] = []

        resposta_llm = self.llm_client.responses.create(
            model=self.model,
            input=historico,
            tools=FERRAMENTAS,
        )

        for _ in range(MAX_TOOL_ROUNDS):
            chamadas = [
                item for item in resposta_llm.output
                if item.type == "function_call"
            ]
            if not chamadas:
                break

            historico.extend(resposta_llm.output)
            for chamada in chamadas:
                resultado = self.tool_dispatcher.executar(
                    chamada.name,
                    chamada.arguments,
                )
                historico.append(
                    {
                        "type": "function_call_output",
                        "call_id": chamada.call_id,
                        "output": json.dumps(resultado, ensure_ascii=False),
                    }
                )
                ferramentas_executadas.append(
                    {
                        "nome": chamada.name,
                        "argumentos": chamada.arguments,
                    }
                )

            resposta_llm = self.llm_client.responses.create(
                model=self.model,
                input=historico,
                tools=FERRAMENTAS,
            )
        else:
            if any(item.type == "function_call" for item in resposta_llm.output):
                raise RuntimeError(
                    f"A LLM excedeu o limite de {MAX_TOOL_ROUNDS} rodadas de tools."
                )

        texto_resposta = resposta_llm.output_text
        if not texto_resposta or not texto_resposta.strip():
            raise RuntimeError("A LLM não retornou uma resposta em texto.")

        tempo_ms = int((perf_counter() - inicio) * 1000)
        interacao = InteracaoChat(
            user_id=user_id,
            resposta=texto_resposta,
            pergunta=mensagem,
            ferramentas=ferramentas_executadas,
            tempo_ms=tempo_ms,
        )

        try:
            self.repo.inserir(interacao=interacao)
        except PyMongoError:
            logger.exception("Falha ao gravar historico")

        return ChatResponse(resposta=texto_resposta)
