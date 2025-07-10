import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from noticias.models import Categoria, Subcategoria, Tag, Noticia
from unittest.mock import patch
from noticias.tasks import processar_noticia_task


@pytest.mark.django_db
def test_basico():
    assert 1 + 1 == 2


@pytest.mark.django_db
def test_webhook_cria_noticia_completa():
    client = APIClient()
    categoria = Categoria.objects.create(nome="Tributos")
    subcategoria = Subcategoria.objects.create(nome="Radar", categoria=categoria)
    Tag.objects.create(nome="Imposto de Renda")

    payload = {
        "titulo": "Teste de webhook",
        "corpo": "Notícia de teste.",
        "fonte": "https://exemplo.com",
        "data_publicacao": "2025-07-04T10:00:00Z",
        "categoria": "Tributos",
        "subcategoria": "Radar",
        "tags": ["Imposto de Renda"],
        "urgente": False
    }

    with patch.object(processar_noticia_task, 'delay', wraps=processar_noticia_task.run):
        response = client.post(
            reverse("webhook-noticia"),
            data=payload,
            format="json",
            # HTTP_AUTHORIZATION="Bearer supersecreto123"
        )

    assert response.status_code == 202
    assert Noticia.objects.filter(titulo="Teste de webhook").exists()


@pytest.mark.django_db
def test_listagem_de_noticias():
    categoria = Categoria.objects.create(nome="Saúde")
    noticia = Noticia.objects.create(
        titulo="Notícia de Teste",
        corpo="...",
        fonte="https://exemplo.com",
        data_publicacao="2025-07-04T10:00:00Z",
        categoria=categoria,
        urgente=True,
    )
    client = APIClient()
    response = client.get(reverse("listar-noticias"))

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["titulo"] == "Notícia de Teste"


@pytest.mark.django_db
def test_marcar_como_urgente():
    categoria = Categoria.objects.create(nome="Poder")
    noticia = Noticia.objects.create(
        titulo="Alerta",
        corpo="...",
        fonte="https://exemplo.com",
        data_publicacao="2025-07-04T10:00:00Z",
        categoria=categoria,
        urgente=False,
    )

    client = APIClient()
    response = client.patch(reverse("marcar-urgente", args=[noticia.id]))
    assert response.status_code == 200

    noticia.refresh_from_db()
    assert noticia.urgente is True
