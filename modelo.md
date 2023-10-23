| pk_solicitar_credito | sk_solicitar_credito | GSI1PK | GSI1SK | GSI2PK | GSI2SK | Atributos |
| --- | --- | --- | --- | --- | --- | --- |
| Pedido#<codigo_pedido_credito> | Pedido#<codigo_pedido_credito> | CNPJ#<cnpj> | Data#<data_pedido> | Segmento#<segmento_bancario> | Status#<status_pedido> | cnpj, status_pedido, segmento_bancario, codigo_canal_solicitacao, descricao_canal_solicitacao, valor_pedido, unidade_monetaria, nome_grupo, data_pedido, prazo, unidade_prazo, codigo_identificacao_origem, parecer_origem_pedido |
| Pedido#<codigo_pedido_credito> | Evento#<data_hora_evento> | - | - | - | - | descricao_evento, data_hora_evento, alteracaoevento, detalhe_evento, responsavel |

--------------------------------------------------

| pk_solicitar_credito | sk_solicitar_credito | GSI1PK | GSI1SK | GSI2PK | GSI2SK | Atributos |
| --- | --- | --- | --- | --- | --- | --- |
| Pedido#1234567890 | Pedido#1234567890 | CNPJ#12345678000123 | Data#2023-10-23 | Segmento#Varejo | Status#Em análise | cnpj: 12345678000123, status_pedido: Em análise, segmento_bancario: Varejo, codigo_canal_solicitacao: 01, descricao_canal_solicitacao: Site, valor_pedido: 100000.00, unidade_monetaria: BRL, nome_grupo: Loja ABC, data_pedido: 2023-10-23, prazo: 36, unidade_prazo: Meses, codigo_identificacao_origem: 001, parecer_origem_pedido: Aprovado |
| Pedido#1234567890 | Evento#2023-10-23T16:46:09 | - | - | - | - | descricao_evento: Criação do pedido, data_hora_evento: 2023-10-23T16:46:09, alteracaoevento: [], detalhe_evento: {}, responsavel: Cliente |
| Pedido#1234567890 | Evento#2023-10-23T17:00:00 | - | - | - | - | descricao_evento: Alteração de status, data_hora_evento: 2023-10-23T17:00:00, alteracaoevento: [{ propriedade: 'status', valor_atual: 'Novo', valor_alterado:'Em análise'}], detalhe_evento: {}, responsavel: Sistema |
| Pedido#1234567890 | Evento#2023-10-24T09:30:00 | - | - | - | - | descricao_evento: Alteração de status, data_hora_evento: 2023-10-24T09:30:00, alteracaoevento: [{ propriedade: 'status', valor_atual: 'Em análise', valor_alterado:'Aprovado'}], detalhe_evento: {motivo_aprovacao: 'Bom histórico de crédito'}, responsavel: Analista |
