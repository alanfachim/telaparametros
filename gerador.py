# Importando as bibliotecas Faker e requests
from faker import Faker
import requests

# Criando uma instância do Faker com o idioma pt_BR
fake = Faker('pt_BR')

# Definindo uma função para gerar um objeto Pedido
def gerar_pedido():
  produto ={'1234':'LTC','1235':'Giro','1236':'Rotativos','1237':'Cartoes','1238':'Emprestimo'}
  # Gerando os atributos do pedido
  codigo_pedido_credito = fake.uuid4()
  cnpj = fake.cnpj()
  status_pedido = fake.random_element(elements=('Novo', 'Em análise', 'Aprovado', 'Rejeitado'))
  segmento_bancario = fake.random_element(elements=('Varejo', 'Atacado', 'Indústria', 'Serviços'))
  codigo_canal_solicitacao = fake.random_int(min=1, max=10)
  descricao_canal_solicitacao = fake.random_element(elements=('Site', 'App', 'Telefone', 'E-mail', 'Chat'))
  valor_pedido = fake.pydecimal(left_digits=6, right_digits=2, positive=True)
  unidade_monetaria = 'BRL'
  nome_grupo = fake.company()
  data_pedido = fake.date()
  prazo = fake.random_int(min=1, max=60)
  unidade_prazo = fake.random_element(elements=('Dias', 'Meses', 'Anos'))
  codigo_identificacao_origem = fake.random_int(min=1, max=100)
  parecer_origem_pedido = fake.sentence()

  # Criando o objeto pedido como um dicionário
  pedido = {
    'codigo_pedido_credito': codigo_pedido_credito,
    'cnpj': cnpj,
    'status_pedido': status_pedido,
    'segmento_bancario': segmento_bancario,
    'codigo_canal_solicitacao': codigo_canal_solicitacao,
    'descricao_canal_solicitacao': descricao_canal_solicitacao,
    'valor_pedido': valor_pedido,
    'unidade_monetaria': unidade_monetaria,
    'nome_grupo': nome_grupo,
    'data_pedido': data_pedido,
    'prazo': prazo,
    'unidade_prazo': unidade_prazo,
    'codigo_identificacao_origem': codigo_identificacao_origem,
    'parecer_origem_pedido': parecer_origem_pedido
  }

  # Retornando o objeto pedido
  return pedido

# Definindo uma função para gerar um objeto eventoPedido
def gerar_evento(pedido):
  # Gerando os atributos do evento
  codigo_pedido_credito = pedido['codigo_pedido_credito']
  descricao_evento = fake.random_element(elements=('Criação do pedido', 'Alteração de status', 'Cancelamento do pedido'))
  data_hora_evento = fake.date_time()
  alteracaoevento = []
  if descricao_evento == 'Alteração de status':
    # Gerando uma alteração de status aleatória
    status_anterior = pedido['status_pedido']
    status_possiveis = ['Novo', 'Em análise', 'Aprovado', 'Rejeitado']
    status_possiveis.remove(status_anterior)
    status_novo = fake.random_element(elements=status_possiveis)
    alteracaoevento.append({
      'propriedade': 'status',
      'valor_atual': status_anterior,
      'valor_alterado': status_novo
    })
    # Atualizando o status do pedido
    pedido['status_pedido'] = status_novo
  detalhe_evento = {}
  if descricao_evento == 'Alteração de status' and pedido['status_pedido'] == 'Aprovado':
    # Gerando um motivo de aprovação aleatório
    detalhe_evento['motivo_aprovacao'] = fake.sentence()
  responsavel = fake.random_element(elements=('Cliente', 'Sistema', 'Analista'))

  # Criando o objeto evento como um dicionário
  evento = {
    'codigo_pedido_credito': codigo_pedido_credito,
    'descricao_evento': descricao_evento,
    'data_hora_evento': data_hora_evento,
    'alteracaoevento': alteracaoevento,
    'detalhe_evento': detalhe_evento,
    'responsavel': responsavel
  }

  # Retornando o objeto evento
  return evento

# Definindo uma função para gerar uma lista de objetos Pedido e eventoPedido
def gerar_massa_de_dados(n_pedidos, n_eventos):
  # Criando uma lista vazia para armazenar os objetos
  massa_de_dados = []

  # Gerando n_pedidos objetos Pedido
  for i in range(n_pedidos):
    # Gerando um objeto Pedido
    pedido = gerar_pedido()
    # Adicionando o objeto Pedido à lista
    massa_de_dados.append(pedido)
    # Enviando uma requisição POST para a rota http://127.0.0.1:8000/pedidos com o pedido gerado no body
    url = 'http://127.0.0.1:8000/pedidos'
    response = requests.post(url, json=pedido)
    # Verificando a resposta da requisição
    if response.status_code == 200:
      print(f'Pedido {pedido["codigo_pedido_credito"]} enviado com sucesso.')
    else:
      print(f'Erro ao enviar o pedido {pedido["codigo_pedido_credito"]}.')
    # Gerando n_eventos objetos eventoPedido para cada pedido
    for j in range(n_eventos):
      # Gerando um objeto eventoPedido
      evento = gerar_evento(pedido)
      # Adicionando o objeto eventoPedido à lista
      massa_de_dados.append(evento)

  # Retornando a lista de objetos
  return massa_de_dados

# Testando a função gerar_massa_de_dados com 2 pedidos e 3 eventos cada
massa_de_dados = gerar_massa_de_dados(2, 3)

# Imprimindo a massa de dados gerada
for item in massa_de_dados:
  print(item)
