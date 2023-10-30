from decimal import Decimal
import uuid
from fastapi import APIRouter, FastAPI, Depends, Path, Body
from pydantic import BaseModel
from typing import List, Optional
import boto3  # Importar o módulo boto3 para interagir com o DynamoDB
from boto3.dynamodb.conditions import Key, Attr 

# Criar um modelo Pydantic para representar as regras
class Regra(BaseModel):
    id: int
    nome: str
    descricao: str
    condicao: str
    acao: str

    # Definir um construtor que recebe um dicionário de atributos do DynamoDB
    @staticmethod
    def from_dict(dictionary):
        # Converter o dicionário em uma lista de argumentos nomeados
        kwargs = {}
        for k, v in dictionary.items():
            # Adicionar o argumento nomeado ao dicionário de kwargs
            kwargs[k.lower()] = v
        # Chamar o construtor da classe base com os kwargs
        return Regra(**kwargs)

    def dict_to_dynamodb(dictionary):
        # Criar um dicionário vazio para armazenar os atributos do DynamoDB
        dynamodb_dict = vars(dictionary)
        # Iterar sobre os itens do dicionário de atributos Python
        for k, v in dynamodb_dict.items():
            # Obter o tipo e o valor do atributo
            tipo = type(v)
            # Converter o valor para uma string se for int ou float
            if tipo == float:
                dynamodb_dict[k] = Decimal(v)
            # Converter o valor para um booleano se for bool
            elif tipo == uuid.UUID:
                dynamodb_dict[k] = str(v)
        return dynamodb_dict
 
class RegraController:
    # Definir o construtor da classe
    def __init__(self):
        # Criando um cliente para acessar o serviço DynamoDB
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566")
        # Criando uma tabela chamada Pedidos
        self.table = dynamodb.Table("regras") 
        
        self.router = APIRouter()
        self.router.add_api_route("/regras", self.criar_regra, methods=["POST"])
        self.router.add_api_route("/regras", self.listar_regras, methods=["GET"])
        self.router.add_api_route("/regras/{id_regra}", self.obter_regra, methods=["GET"])
        self.router.add_api_route("/regras/{id_regra}", self.alterar_regra, methods=["PUT"])
        self.router.add_api_route("/regras/{id_regra}", self.excluir_regra, methods=["DELETE"])
        
        

    # Definir uma rota POST para criar uma nova regra 
    def criar_regra(self, regra: Regra = Body(...)):
        # Inserir a regra na tabela de regras do DynamoDB usando o método put_item do cliente do DynamoDB
        self.table.put_item(Item=regra.dict_to_dynamodb())

        # Retornar a regra criada com um status code 201 (Created)
        return {"regra": regra}, 201

    # Definir uma rota GET para listar todas as regras 
    def listar_regras(self):
        # Obter todas as regras da tabela de regras do DynamoDB usando o método scan do cliente do DynamoDB
        response = self.table.scan()

        # Converter os itens retornados em uma lista de regras Pydantic
        regras = []
        for item in response["Items"]:
            regra = Regra.from_dict(item)
            regras.append(regra)

        # Retornar a lista de regras com um status code 200 (OK)
        return {"regras": regras}, 200

    # Definir uma rota GET para obter uma regra pelo seu id 
    def obter_regra(self, id_regra: int = Path(..., ge=1)):
        # Definir a chave primária da regra como um dicionário de atributos do DynamoDB
        response = self.table.query(KeyConditionExpression=Key("id_regra").eq(id_regra))

        # Se o item existir na resposta, converter o item em uma regra Pydantic e retorná-la com um status code 200 (OK)
        if "Item" in response:
            item = response["Item"][0]
            regra = Regra.from_dict(item)
            return {"regra": regra}, 200
        # Se o item não existir na resposta, retornar um status code 404 (Not Found)
        else:
            return {"erro": "Regra não encontrada"}, 404

    # Definir uma rota PUT para alterar uma regra pelo seu id 
    def alterar_regra(
        self, id_regra: int = Path(..., ge=1), nova_regra: Regra = Body(...)
    ):
        # Atualizar a regra na tabela de regras do DynamoDB usando o método put_item do cliente do DynamoDB
        self.table.put_item(Item=nova_regra.dict_to_dynamodb())

        # Retornar a nova regra com um status code 200 (OK)
        return {"regra": nova_regra}, 200

    # Definir uma rota DELETE para excluir uma regra pelo seu id 
    def excluir_regra(self, id_regra: int = Path(..., ge=1)): 
        # Excluir a regra da tabela de regras do DynamoDB usando o método delete_item do cliente do DynamoDB
        self.table.delete_item(
            Key=Key("id_regra").eq(id_regra),
            ConditionExpression="attribute_exists(id)",
        )

        # Retornar um status code 204 (No Content)
        return None, 204

    # Definir uma rota GET para obter o histórico de uma regra pelo seu id 
    def obter_historico(self, id_regra: int = Path(..., ge=1)):
            return {"erro": "Histórico não encontrado"}, 404
