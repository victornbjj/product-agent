
from redis import Redis
from ..models.produto import Produto


class ProdutoRedisRepository:

    def __init__(self, cliente: Redis):
        self.cliente = cliente

    def get_by_id(self, id :int) -> Produto | None :
         cliente = self.cliente.get(f"produto:{id}")
         
         if cliente is None:
             return  None
         
         return Produto.model_validate_json(cliente)
        
         

    def set_by_id(self, produto: Produto):
        chave = f"produto:{produto.id}"

        produto_json = Produto.model_dump_json(produto)

        self.cliente.set(chave, produto_json, ex=600)



    
        
        

