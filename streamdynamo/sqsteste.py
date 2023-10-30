import boto3
import requests

# Cria um cliente SQS usando as credenciais da AWS
sqs = boto3.client('sqs')

# Obtém a URL da fila SQS pelo seu nome
queue_url = sqs.get_queue_url(QueueName='minha-fila')['QueueUrl']

# Define o tempo máximo de espera para receber uma mensagem (em segundos)
wait_time = 20

# Define a URL do endpoint que receberá a mensagem via post
post_url = 'https://meu-endpoint.com'

# Cria uma classe para fazer polling da fila SQS e encaminhar a mensagem via post
class SQSPoller:

    def __init__(self, queue_url, wait_time, post_url):
        self.queue_url = queue_url
        self.wait_time = wait_time
        self.post_url = post_url

    def poll(self):
        # Recebe uma mensagem da fila SQS usando long polling
        response = sqs.receive_message(
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
            requests.post(self.post_url, data=body)

            # Deleta a mensagem da fila SQS
            sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )

            # Retorna a mensagem enviada
            return body

        else:
            # Retorna None se não houver nenhuma mensagem na resposta
            return None

# Cria uma instância da classe SQSPoller com os parâmetros definidos
poller = SQSPoller(queue_url, wait_time, post_url)

# Faz polling da fila SQS e encaminha a mensagem via post em um loop infinito
while True:
    message = poller.poll()
    if message:
        print(f'Mensagem enviada: {message}')
    else:
        print('Nenhuma mensagem recebida')
