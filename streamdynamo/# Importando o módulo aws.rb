# Importando o módulo aws
provider "aws" {
  region = "us-east-1"
}

# Criando um recurso do tipo aws_dynamodb_table
resource "aws_dynamodb_table" "Pedidos" {
  # Definindo o nome da tabela
  name = "Pedidos"
  # Definindo os atributos da tabela
  attribute {
    name = "cnpj"
    type = "S"
  }
  attribute {
    name = "codigo_pedido_credito"
    type = "S"
  }
  attribute {
    name = "segmento_bancario"
    type = "S"
  }
  attribute {
    name = "status_pedido"
    type = "S"
  }
  # Definindo a chave primária da tabela
  hash_key = "cnpj"
  range_key = "codigo_pedido_credito"
  # Definindo o throughput provisionado da tabela
  read_capacity = 5
  write_capacity = 5
  # Definindo o índice secundário global da tabela
  global_secondary_index {
    name = "cnpj-segmento_bancario-status_pedido-index"
    hash_key = "cnpj"
    range_key = "segmento_bancario"
    non_key_attributes = ["status_pedido"]
    projection_type = "INCLUDE"
    read_capacity = 5
    write_capacity = 5
  }
  # Habilitando o streaming da tabela
  stream_enabled = true
  stream_view_type = "NEW_AND_OLD_IMAGES" # Capturando as imagens antes e depois dos itens modificados
}

# Criando um recurso do tipo aws_lambda_function
resource "aws_lambda_function" "process_stream" {
  # Definindo o nome da função
  function_name = "process_stream"
  # Definindo o arquivo zip com o código da função
  filename      = "${path.module}/process_stream.zip"
  # Definindo a função handler
  handler       = "process_stream.lambda_handler"
  # Definindo o tempo de execução
  runtime       = "python3.8"
}

# Criando um recurso do tipo aws_lambda_event_source_mapping
resource "aws_lambda_event_source_mapping" "stream_trigger" {
  # Definindo a função lambda que será acionada pelo stream
  function_name = aws_lambda_function.process_stream.arn
  # Definindo o stream do dynamo que será a fonte do evento
  event_source_arn = aws_dynamodb_table.Pedidos.stream_arn
}