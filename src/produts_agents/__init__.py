
from redis import Redis


class ProdutoRedisRepository:

    def __init__(self, cliente: Redis):
        self.cliente = cliente

    def get_by_id(self, id: int):
         cliente = self.cliente.get(id)

         if cliente is None:
             return  None
        
         return cliente

    def set_by_id(self, id):
        cliente = self.cliente.get(id)

        if cliente is not  None:
            return cliente

        return self.cliente.set(id) 
        

