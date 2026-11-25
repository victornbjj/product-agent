from redis import Redis


class RateLimitRepository():

    def __init__(self, cliente : Redis) :
         self.cliente = cliente

    
    def incrementar(self, user_id: str) -> int:
        
        chave = f"rate:{user_id}"
        
        contador = self.cliente.incr(chave)
        if contador == 1:
            self.cliente.expire(chave, 60)

        return contador