# 📚 Noticia

Criar um sistema capaz de:

- Receber webhooks de notícias
- Classificá-las automaticamente
- Armazená-las em banco de dados
- Disponibilizá-las via API REST
- Processar a fila de forma assíncrona
- Escalar horizontalmente

---

## 🚀 Tecnologias utilizadas

- **Python 3.11**
- **Django 5.2**
- **Django REST Framework**
- **Celery**
- **Redis**
- **PostgreSQL**
- **Docker & Docker Compose**
- **drf-spectacular (Swagger UI)**
- **Flower (monitoramento de tarefas)**

---

## 📦 Como rodar o projeto

### Pré-requisitos

- Docker e Docker Compose instalados

### Passos:

```bash
# Subir o ambiente
cd docker
docker-compose up --build
```

A aplicação estará disponível em:

- Django: [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/)
- Flower (Celery): [http://localhost:5555](http://localhost:5555)

---

## 🔐 Variáveis de Ambiente

Definidas no `docker-compose.yml`, você pode sobrescrever:

```env
WEBHOOK_SECRET_TOKEN=supersecreto123
CELERY_BROKER_URL=redis://redis:6379/0
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
```

---

## 📬 Endpoints principais

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/webhook/noticia/` | Recebe uma notícia via JSON (requer token no header) |
| `GET`  | `/api/noticias/` | Lista todas as notícias com filtros, busca e paginação |
| `PATCH` | `/api/noticias/<id>/marcar-urgente/` | Marca uma notícia como urgente |
| `GET` | `/api/tags/` | Lista todas as tags cadastradas |
| `GET` | `/api/tags/<id>/noticias/` | Lista todas as notícias com a tag informada |
| `GET` | `/api/docs/swagger/` | Documentação Swagger |
| `GET` | `/api/schema/` | Arquivo OpenAPI (json) |
| `GET` | `/api/docs/redoc/` | Documentação alternativa Redoc |
| `GET` | `/admin/` | Admin do Django |

---

## ✅ Requisitos atendidos

- ✅ Webhook com segurança
- ✅ Processamento assíncrono com fila
- ✅ Classificação automática por palavras-chave
- ✅ Banco de dados relacional com relacionamentos
- ✅ API REST com filtros, paginação, ordenação
- ✅ Docker com serviços separados
- ✅ Monitoramento com Flower
- ✅ Testes automatizados com Pytest
- ✅ Swagger (OpenAPI 3.0)
- ✅ Justificativa técnica para não usar Lambda diretamente (ver `/doc/README_lambda_justificativa.md`)

---

## 🧪 Executar os testes

```bash
docker-compose run web pytest
```

ou fazer um exec no container do django e executar

```bash
pytest noticias/tests.py
```

---

## 📁 Estrutura do Projeto

```
noticias/
├── models.py
├── views.py
├── tasks.py
├── classifiers.py
├── serializers.py
├── urls.py
├── tests/
│   └── test_api.py
noticias_project/
├── settings.py
├── urls.py
├── celery.py
├── __init__.py
docker/
├── docker-compose.yml
├── Dockerfile
doc/
└── README_lambda_justificativa.md
```

---

## 📄 Sobre a decisão de não usar AWS Lambda

A justificativa técnica completa está documentada em:

```
doc/README_lambda_justificativa.md
```
📎 Veja também: [Evidências Visuais](noticias_project/doc/README_imagens.md)
