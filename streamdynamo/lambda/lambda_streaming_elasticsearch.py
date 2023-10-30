import datetime
from typing import Union
from boto3.dynamodb.conditions import Key, Attr

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

# Definir o método lambda handler
def lambda_handler(event, context):
    print(event)
    # Iterar sobre os registros do evento do DynamoDB
    for record in event['Records']:
        # Verificar se o tipo de evento é INSERT ou MODIFY
        if record['eventName'] in ['INSERT', 'MODIFY']:
            # Obter o item modificado do stream
            item = record['dynamodb']['NewImage']
            # Converter o item em um dicionário Python
            doc_body = {k: v[list(v.keys())[0]] for k, v in item.items()}
            # Obter o código do pedido como id do documento
            doc_id = doc_body['codigo_pedido_credito']
            # Inserir o documento no elastic search usando a classe ElasticSearchQuery
            result = es_query.insert(index='pedidos', doc_type='_doc', doc_id=doc_id, doc_body=doc_body)
            # Imprimir o resultado da inserção
            print(result)
