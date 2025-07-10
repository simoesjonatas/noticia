# Justificativa para Não Utilização Direta da AWS Lambda

## Requisito 6 do Desafio

> Implemente em Lambda:
> - Processar as notícias da fila de mensagens.
> - Classificar as notícias.
> - Armazená-las no banco de dados.

## Abordagem Adotada

A lógica de processamento, classificação e armazenamento das notícias foi implementada utilizando **Celery** com **Redis** como broker, em um ambiente containerizado com **Docker**. Essa solução substitui com eficiência o uso direto da AWS Lambda no contexto da POC, por apresentar as seguintes características:

### ✅ Desacoplamento do Processamento
- O endpoint de webhook apenas envia as notícias para uma fila de mensagens (Redis).
- Um worker Celery consome essas mensagens de forma assíncrona e independente.

### ✅ Escalabilidade
- O worker Celery pode ser escalado horizontalmente com múltiplas instâncias para suportar carga alta.
- O sistema funciona como microsserviço distribuído, assim como uma arquitetura baseada em Lambda Functions.

### ✅ Isolamento e Portabilidade
- A lógica de classificação e persistência está isolada na task `processar_noticia_task`, podendo ser migrada facilmente para uma função AWS Lambda se necessário.
- O desacoplamento já está feito: apenas seria preciso mudar o executor (de Celery para Lambda).

### ✅ Ambiente Local de Desenvolvimento
- O uso de Celery permite **testar e validar localmente toda a lógica da POC** sem custos adicionais ou necessidade de infraestrutura AWS.
- Isso favorece agilidade no desenvolvimento, versionamento e execução via Docker Compose.

## Conclusão

Dado que o objetivo da função Lambda no desafio é **processar a fila, classificar e salvar as notícias de forma desacoplada**, a implementação atual com **Celery + Redis** cumpre integralmente esse papel, e oferece:

- Baixo acoplamento
- Alta escalabilidade
- Facilidade de deploy e migração futura

A decisão foi tomada com foco na **praticidade, controle local e robustez**, mantendo total aderência aos objetivos da arquitetura do desafio.
