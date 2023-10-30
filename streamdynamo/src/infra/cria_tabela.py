# Importando o módulo boto3
import boto3

# Criando um cliente para acessar o serviço DynamoDB
dynamodb = boto3.client("dynamodb", endpoint_url="http://localhost:4566")  

# Criando um recurso para acessar o serviço SQS
sqs = boto3.resource("sqs", endpoint_url="http://localhost:4566")

# Definindo os atributos da tabela regras
tabela_regras = {
    "TableName": "regras",
    "KeySchema": [
        {"AttributeName": "id_regra", "KeyType": "HASH"} # Chave primária
    ],
    "AttributeDefinitions": [
        {"AttributeName": "id_regra", "AttributeType": "N"} # Tipo numérico
    ],
    "ProvisionedThroughput": {
        "ReadCapacityUnits": 10,
        "WriteCapacityUnits": 10
    }
}

# Criando a tabela regras no DynamoDB
try:
    response = dynamodb.create_table(**tabela_regras)
    print(f"Criando a tabela {tabela_regras['TableName']}...")
    response["TableDescription"]["TableStatus"] == "ACTIVE"
except Exception as e:
    print(f"Não foi possível criar a tabela {tabela_regras['TableName']}. Motivo: {e}")

# Definindo os atributos da fila encaminha_requisicao_pedido.fifo
fila_encaminha = {
    "QueueName": "encaminha_requisicao_pedido.fifo",
    "Attributes": {
        "FifoQueue": "true", # Fila FIFO
        "ContentBasedDeduplication": "true" # Deduplicação baseada no conteúdo
    }
}

# Criando a fila encaminha_requisicao_pedido.fifo no SQS
try:
    queue = sqs.create_queue(**fila_encaminha)
    print(f"Criando a fila {fila_encaminha['QueueName']}...")
except Exception as e:
    print(f"Não foi possível criar a fila {fila_encaminha['QueueName']}. Motivo: {e}")
