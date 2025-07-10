from rest_framework import serializers
from .models import Categoria, Subcategoria, Tag, Noticia

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']


class SubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategoria
        fields = ['id', 'nome', 'categoria']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'nome']

class NoticiaListSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField()
    subcategoria = serializers.StringRelatedField()
    tags = serializers.SlugRelatedField(slug_field='nome', many=True, read_only=True)

    class Meta:
        model = Noticia
        fields = [
            'id', 'titulo', 'fonte', 'data_publicacao', 'categoria',
            'subcategoria', 'tags', 'urgente', 'criado_em'
        ]

class NoticiaSerializer(serializers.ModelSerializer):
    # categoria = serializers.CharField()
    # subcategoria = serializers.CharField(required=False, allow_blank=True)
    # tags = serializers.ListField(child=serializers.CharField(), required=False)
    categoria = serializers.StringRelatedField()
    subcategoria = serializers.StringRelatedField()
    tags = serializers.SlugRelatedField(slug_field='nome', many=True, read_only=True)


    class Meta:
        model = Noticia
        fields = [
            'id'
            , 'titulo'
            , 'corpo'
            , 'fonte'
            , 'data_publicacao'
            ,'categoria'
            , 'subcategoria'
            , 'tags'
            , 'urgente'
            , 'criado_em'
        ]
        read_only_fields = ['id', 'criado_em']

    def create(self, validated_data):
        categoria_nome = validated_data.pop('categoria')
        subcategoria_nome = validated_data.pop('subcategoria', None)
        tags_nomes = validated_data.pop('tags', [])

        categoria, _ = Categoria.objects.get_or_create(nome=categoria_nome)

        subcategoria = None
        if subcategoria_nome:
            subcategoria, _ = Subcategoria.objects.get_or_create(
                nome=subcategoria_nome,
                categoria=categoria
            )

        noticia = Noticia.objects.create(
            categoria=categoria,
            subcategoria=subcategoria,
            **validated_data
        )

        for tag_nome in tags_nomes:
            tag, _ = Tag.objects.get_or_create(nome=tag_nome)
            noticia.tags.add(tag)

        return noticia

class TagComNoticiasSerializer(serializers.ModelSerializer):
    noticias = NoticiaListSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'nome', 'noticias']