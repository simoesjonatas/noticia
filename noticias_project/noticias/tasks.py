from celery import shared_task
from .models import Categoria, Subcategoria, Tag, Noticia
from django.utils.dateparse import parse_datetime
from .classifiers import classificar
from .classifiers import classificar

@shared_task
def processar_noticia_task(dados):
    # Executa classificação se dados não vierem preenchidos
    texto_completo = f"{dados['titulo']} {dados['corpo']}"
    classificacao = classificar(texto_completo)

    categoria_nome = dados.get('categoria') or classificacao['categoria']
    subcategoria_nome = dados.get('subcategoria') or classificacao['subcategoria']
    tags_nomes = dados.get('tags') or classificacao['tags']

    # Cria ou recupera categoria
    categoria, _ = Categoria.objects.get_or_create(nome=categoria_nome) if categoria_nome else (None, False)

    # Cria ou recupera subcategoria
    subcategoria = None
    if subcategoria_nome and categoria:
        subcategoria, _ = Subcategoria.objects.get_or_create(nome=subcategoria_nome, categoria=categoria)

    # Cria a notícia
    noticia = Noticia.objects.create(
        titulo=dados['titulo'],
        corpo=dados['corpo'],
        fonte=dados['fonte'],
        data_publicacao=parse_datetime(dados['data_publicacao']),
        categoria=categoria,
        subcategoria=subcategoria,
        urgente=dados.get('urgente', False),
    )

    # Adiciona tags
    for tag_nome in tags_nomes:
        tag, _ = Tag.objects.get_or_create(nome=tag_nome)
        noticia.tags.add(tag)

    noticia.save()
    return noticia.id
