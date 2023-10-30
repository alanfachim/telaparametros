import unittest
from unittest.mock import patch, Mock
import requests

# Importa a classe SQSPoller do módulo que eu criei
from sqs_poller import SQSPoller

# Cria uma classe de teste para testar os métodos da classe SQSPoller
class TestSQSPoller(unittest.TestCase):

    # Define alguns valores para os parâmetros da classe SQSPoller
    queue_url = 'https://sqs.us-east-1.amazonaws.com/1234567890/minha-fila'
    wait_time = 20
    post_url = 'https://meu-endpoint.com'

    # Cria uma instância da classe SQSPoller com os valores definidos
    poller = SQSPoller(queue_url, wait_time, post_url)

    # Define um método de teste para testar o método poll da classe SQSPoller
    def test_poll(self):

        # Cria um objeto mock para simular o cliente SQS
        sqs_mock = Mock()

        # Define o retorno do método receive_message do cliente SQS
        sqs_mock.receive_message.return_value = {
            'Messages': [
                {
                    'Body': '{"foo": "bar"}',
                    'ReceiptHandle': 'abc123'
                }
            ]
        }

        # Define o retorno do método delete_message do cliente SQS
        sqs_mock.delete_message.return_value = {}

        # Substitui o atributo sqs da instância da classe SQSPoller pelo objeto mock
        self.poller.sqs = sqs_mock

        # Cria um objeto mock para simular o módulo requests
        requests_mock = Mock()

        # Define o retorno do método post do módulo requests
        requests_mock.post.return_value = Mock(status_code=200)

        # Usa o decorador patch para substituir o módulo requests pelo objeto mock
        with patch('requests', requests_mock):

            # Chama o método poll da instância da classe SQSPoller
            message = self.poller.poll()

            # Verifica se o método receive_message do cliente SQS foi chamado com os parâmetros corretos
            sqs_mock.receive_message.assert_called_with(
                QueueUrl=self.queue_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=1,
                WaitTimeSeconds=self.wait_time
            )

            # Verifica se o método post do módulo requests foi chamado com os parâmetros corretos
            requests_mock.post.assert_called_with(
                self.post_url,
                data='{"foo": "bar"}'
            )

            # Verifica se o método delete_message do cliente SQS foi chamado com os parâmetros corretos
            sqs_mock.delete_message.assert_called_with(
                QueueUrl=self.queue_url,
                ReceiptHandle='abc123'
            )

            # Verifica se o método poll retornou a mensagem esperada
            self.assertEqual(message, '{"foo": "bar"}')

# Executa os testes unitários
if __name__ == '__main__':
    unittest.main()
