from ..repositories.produto_repository import ProdutoRepository
from fastapi import HTTPException
from ..models.produto import Produto
from ..repositories.produto_cache_repository import ProdutoRedisRepository 


class ProdutoService:
    
    
    def __init__(self, repo : ProdutoRepository, cache : ProdutoRedisRepository):
        self.repo = repo
        self.cache = cache

    def get_all(self) -> list[Produto]:
        produtos = self.repo.get_all()
    
        
        return produtos

    def get_by_id(self, id: int) -> Produto:


        produto_cacheado = self.cache.get_by_id(id)

        if produto_cacheado is None:
            produto = self.repo.get_by_id(id)
            if not(produto):
                raise HTTPException(status_code=404, detail="Produto não encontrado.")
       
            self.cache.set_by_id(produto)
            return produto    
        return  produto_cacheado 
