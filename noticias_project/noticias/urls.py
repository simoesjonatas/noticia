from django.urls import path
from .views import WebhookNoticiaView, NoticiaListView, marcar_como_urgente,  TagListView, NoticiasPorTagView

urlpatterns = [
    path('webhook/noticia/', WebhookNoticiaView.as_view(), name='webhook-noticia'),
    path('noticias/', NoticiaListView.as_view(), name='listar-noticias'),
    path('noticias/<int:pk>/marcar-urgente/', marcar_como_urgente, name='marcar-urgente'),
    
    path('tags/', TagListView.as_view(), name='listar-tags'),
    # path('tags/<str:nome>/noticias/', NoticiasPorTagView.as_view(), name='noticias-por-tag'),
    path('tags/<int:pk>/noticias/', NoticiasPorTagView.as_view(), name='noticias-por-tag'),

]
