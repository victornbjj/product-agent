# ProductMind 
<h3>E um sistema desenvolvido na forma de uma API REST em Python/FastAPI com endpoints para listar produtos e conversar com um agente.<h3>

- PostgreSQL (Supabase): Guarda o cadastro oficial dos produtos e preços de forma relacional e segura.

- Redis (Cache + Proteção): Quando alguém buscar um produto, a API consulta primeiro o Redis. Se não estiver lá, busca no PostgreSQL do Supabase e salva no Redis por 10 minutos (TTL).

- Redis usdo  para limitar cada usuário a no máximo 10 mensagens por minuto (Rate Limiting).

- MongoDB (Histórico Flexível): Salvando cada interação do usuário com o Agente (pergunta, ferramentas acionadas, tempo de resposta e resposta final) como um documento JSON no MongoDB.
