from pymongo.collection import Collection
from ..models.interacao_chat import InteracaoChat


class MongoRepository():

    def __init__(self, colecao: Collection):
        self.colecao = colecao

    def inserir(self, interacao: InteracaoChat):

        interacao_json = interacao.model_dump(exclude={"id"})
    
        self.colecao.insert_one(interacao_json)

    def listar_por_id(self, user_id:str ) -> list[InteracaoChat]:

        cursor = self.colecao.find({"user_id": user_id})


        interecoes = []

        for documento in cursor:
            documento["id"] = str(documento.pop("_id"))
            interecoes.append(InteracaoChat(**documento))

        return interecoes

            
    

        

      