from typing import Union

# Importar o módulo elasticsearch
from elasticsearch import Elasticsearch


# Criar uma classe para fazer consultas e inserções no elastic search
class ElasticSearchQuery:
    # Inicializar a classe com o endereço do servidor elastic search
    def __init__(self, host, port):
        self.es = Elasticsearch([{"host": host, "port": port, "scheme": "http"}])

    # Definir um método para fazer uma consulta simples por termo
    def query_by_term(self, index, field, term):
        # Construir o corpo da consulta
        query_body = {"query": {"term": {field: term}}}
        # Executar a consulta e retornar os resultados
        results = self.es.search(index=index, body=query_body)
        return results

        # Definir um método para fazer uma consulta com mais um campo de filtro

    def query_with_filter(self, index, filtros):
        filters = []
        for filtro in filtros:
            filters.append({"term": {filtro['prop']: filtro['val']}})
        # Construir o corpo da consulta
        query_body = {"query": {"bool": {"must": filters}}}
        # Executar a consulta e retornar os resultados
        results = self.es.search(index=index, body=query_body)
        return results

    # Definir um método para fazer uma consulta por intervalo de datas
    def query_by_date_range(self, index, field, start_date, end_date):
        # Construir o corpo da consulta
        query_body = {"query": {"range": {field: {"gte": start_date, "lte": end_date}}}}
        # Executar a consulta e retornar os resultados
        results = self.es.search(index=index, body=query_body)
        return results

    # Definir um método para fazer uma inserção no elastic search
    def insert(self, index, doc_type, doc_id, doc_body):
        # Executar a inserção e retornar o resultado
        result = self.es.index(index=index, doc_type=doc_type, id=doc_id, body=doc_body)
        return result


# Criar uma instância da classe com o endereço do servidor elastic search
es_query = ElasticSearchQuery("localhost", 9200)

# Criar um documento para inserir no índice 'tweets'
# doc = {
#    'text': 'Eu amo programar em python',
#    'user': 'João',
#    'date': '2023-10-21'
# }
# Fazer uma inserção no índice 'tweets' com o documento criado
# result = es_query.insert(index='tweets', doc_type='_doc', doc_id='123', doc_body=doc)
# Imprimir o resultado
# print(result) #
# Fazer uma consulta simples por termo no índice 'tweets' e no campo 'text'
# results = es_query.query_by_term(index='tweets', field='text', term='python')
# Imprimir os resultados
# print(results)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import uuid

app = FastAPI()


# Definindo o modelo do objeto
class PedidoCredito(BaseModel):
    codigo_pedido_credito: uuid.UUID = uuid.uuid4()
    cnpj: str
    status_pedido: str = None
    segmento_bancario: str = "K"
    codigo_canal_solicitacao: str = "01"
    descricao_canal_solicitacao: str = "mobile"
    valor_pedido: float
    unidade_monetaria: str = "BRL"
    nome_grupo: str
    data_pedido: str
    prazo: int
    unidade_prazo: str = "dias"
    codigo_identificacao_origem: str = "999999"
    parecer_origem_pedido: dict

    # O método para serializar o objeto
    def to_dict(self):
        # Retornando um dicionário com os atributos e valores do objeto
        return {
            "codigo_pedido_credito": self.codigo_pedido_credito,
            "cnpj": self.cnpj,
            "status_pedido": self.status_pedido,
            "segmento_bancario": self.segmento_bancario,
            "codigo_canal_solicitacao": self.codigo_canal_solicitacao,
            "descricao_canal_solicitacao": self.descricao_canal_solicitacao,
            "valor_pedido": self.valor_pedido,
            "unidade_monetaria": self.unidade_monetaria,
            "nome_grupo": self.nome_grupo,
            "data_pedido": self.data_pedido,
            "prazo": self.prazo,
            "unidade_prazo": self.unidade_prazo,
            "codigo_identificacao_origem": self.codigo_identificacao_origem,
            "parecer_origem_pedido": self.parecer_origem_pedido,
        }

    # Validando o cnpj usando uma função externa
    @validator("cnpj")
    def validacnpj(cls, v):
        if not v.isdigit():
            raise ValueError("cnpj deve conter apenas números")
        if len(v) != 14:
            raise ValueError("cnpj deve ter 14 dígitos")
        # Outras regras de validação do cnpj podem ser adicionadas aqui
        return v


# Criando uma lista vazia para armazenar os objetos
pedidos = []


# Criando as rotas para o crud
@app.post("/pedidos")
def create_pedido(pedido: PedidoCredito):
    # Adicionando o objeto à lista
    pedidos.append(pedido)
    result = es_query.insert(
        index="pedidos",
        doc_type="_doc",
        doc_id=pedido.codigo_pedido_credito,
        doc_body=pedido.to_dict(),
    )
    return {"message": "Pedido criado com sucesso"}


@app.get("/pedidos")
def read_pedidos(cnpj=None, segmento_bancario=None):
    # Retornando todos os objetos da lista
    filtros = []
    if cnpj:
        filtros.append({"prop": "cnpj", "val": cnpj})
    elif segmento_bancario:
        filtros.append({"prop": "segmento_bancario", "val": segmento_bancario})
    else:
        return pedidos

    _pedidos = es_query.query_with_filter(
        index="pedidos", filtros=filtros
    )
    return _pedidos


@app.get("/pedidos/{codigo_pedido_credito}")
def read_pedido(codigo_pedido_credito: uuid.UUID):
    # Procurando o objeto pelo código na lista
    for pedido in pedidos:
        if pedido.codigo_pedido_credito == codigo_pedido_credito:
            return pedido
    # Se não encontrar, retorna um erro 404
    raise HTTPException(status_code=404, detail="Pedido não encontrado")


@app.put("/pedidos/{codigo_pedido_credito}")
def update_pedido(codigo_pedido_credito: uuid.UUID, pedido: PedidoCredito):
    # Procurando o objeto pelo código na lista e atualizando os seus atributos
    for i, p in enumerate(pedidos):
        if p.codigo_pedido_credito == codigo_pedido_credito:
            pedidos[i] = pedido
            return {"message": "Pedido atualizado com sucesso"}
    # Se não encontrar, retorna um erro 404
    raise HTTPException(status_code=404, detail="Pedido não encontrado")


@app.delete("/pedidos/{codigo_pedido_credito}")
def delete_pedido(codigo_pedido_credito: uuid.UUID):
    # Procurando o objeto pelo código na lista e removendo-o
    for i, p in enumerate(pedidos):
        if p.codigo_pedido_credito == codigo_pedido_credito:
            pedidos.pop(i)
            return {"message": "Pedido deletado com sucesso"}
    # Se não encontrar, retorna um erro 404
    raise HTTPException(status_code=404, detail="Pedido não encontrado")
