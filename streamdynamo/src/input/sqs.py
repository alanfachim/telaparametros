import boto3
import requests
 
# Cria uma classe para fazer polling da fila SQS e encaminhar a mensagem via post
class SQSPoller:

    def __init__(self, queue_name, wait_time = 20): 
        self.wait_time = wait_time 
        # Cria um cliente SQS usando as credenciais da AWS
        self.sqs = boto3.client('sqs', endpoint_url="http://localhost:4566")
        # Obtém a URL da fila SQS pelo seu nome
        self.queue_url = self.sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
         
    # Define um método que envia uma mensagem para a fila SQS
    def send_to_sqs(self, message_body, message_attributes=None):
        # Se não houver atributos da mensagem, define um dicionário vazio
        if not message_attributes:
            message_attributes = {}
        # Envia a mensagem para a fila SQS usando o método send_message do cliente boto3
        response = self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message_body,
            MessageAttributes=message_attributes
        )
        # Retorna a resposta do SQS que contém o ID e o MD5 da mensagem
        return response      

    def poll(self):
        # Recebe uma mensagem da fila SQS usando long polling
        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            WaitTimeSeconds=self.wait_time
        )

        # Verifica se há alguma mensagem na resposta
        if 'Messages' in response:
            # Obtém a primeira mensagem da lista
            message = response['Messages'][0]

            # Obtém o corpo e o identificador da mensagem
            body = message['Body']
            receipt_handle = message['ReceiptHandle']

            # Envia a mensagem via post para o endpoint especificado
            requests.post(self.body['url'], data=body['payload'])

            # Deleta a mensagem da fila SQS
            self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )

            # Retorna a mensagem enviada
            return body

        else:
            # Retorna None se não houver nenhuma mensagem na resposta
            return None
