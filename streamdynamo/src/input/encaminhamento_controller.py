from fastapi import APIRouter, FastAPI, Depends, Path, Body 
import requests
 
# Criar uma classe controller para agrupar as rotas relacionadas ao encaminhamento das regras
class EncaminhamentoController:
    # Definir o construtor da classe
    def __init__(self, regras, sqs):
        self.encaminhamentos = []
        self.sqs = sqs
        self.regras = regras
        self.router = APIRouter()
        self.router.add_api_route(
            "/encaminhar", self.encaminhar_regra, methods=["POST"]
        )
        
    def _buscaRegra(self):
        for regra in self.regras['regras']:
            if regra['bypass']:
                return regra
            

    # Definir uma rota POST para criar um novo encaminhamento de uma regra
    def encaminhar_regra(self, encaminhamento=Body(...)):
        # Adicionar o encaminhamento à lista de encaminhamentos
        self.encaminhamentos.append(encaminhamento)
        regra = self._buscaRegra(encaminhamento)
        if regra.value.asincrono:
            self.sqs.send_to_sqs({"url": regra.value.url, "payload": encaminhamento})
        else:
            # Envia a mensagem via post para o endpoint especificado
            requests.post(self.body['url'], data=encaminhamento)

        # Retornar o encaminhamento criado com um status code 201 (Created)
        return {"encaminhamento": encaminhamento}, 201
