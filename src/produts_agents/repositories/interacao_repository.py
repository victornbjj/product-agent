from pymongo.collection import Collection
from ..models.interacao_chat import InteracaoChat


class MongoRepository():

    def __init__(self, colecao: Collection):
        self.colecao = colecao
        self.colecao.create_index("user_id")

    def inserir(self, interacao: InteracaoChat):

        interacao_texto = interacao.model_dump(exclude={"id"})
    
        return self.colecao.insert_one(interacao_texto).inserted_id

    
    def listar_por_usuario(self, user_id:str ) -> list[InteracaoChat]:

        cursor = self.colecao.find({"user_id": user_id})


        interacoes = []

        for documento in cursor:
            documento["id"] = str(documento.pop("_id"))
            interacoes.append(InteracaoChat(**documento))

        return interacoes

            
    

        

      