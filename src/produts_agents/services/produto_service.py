from ..repositories.produto_repository import ProdutoRepository
from fastapi import HTTPException
from ..models.produto import Produto

class ProdutoService:
    
    
    def __init__(self, repo : ProdutoRepository):
        self.repo = repo

    def get_all(self) -> list[Produto]:
        produtos = self.repo.get_all()
    
        
        return produtos

    def get_by_id(self, id: int) -> Produto:
        produto = self.repo.get_by_id(id)
        if not(produto):
            raise HTTPException(status_code=404, detail="Produto não encontrado.")
       
        return produto
