from django.contrib import admin
from .models import Categoria, Subcategoria, Tag, Noticia
# Register your models here.

admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Tag)
admin.site.register(Noticia)
