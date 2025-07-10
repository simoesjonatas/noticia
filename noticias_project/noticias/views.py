from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoticiaSerializer
from .models import *
from .tasks import processar_noticia_task
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .serializers import NoticiaListSerializer
from rest_framework.decorators import api_view
from .serializers import TagSerializer, TagComNoticiasSerializer



class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class NoticiasPorTagView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagComNoticiasSerializer
    lookup_field = 'pk'
    # lookup_field = 'nome'


class WebhookNoticiaView(APIView):
    def post(self, request):
        processar_noticia_task.delay(request.data)
        return Response({'message': 'Notícia recebida e enviada para fila'}, status=status.HTTP_202_ACCEPTED)

# teste manual
class WebhookNoticiaViewManual(APIView):
    def post(self, request):
        serializer = NoticiaSerializer(data=request.data)
        if serializer.is_valid():
            noticia = serializer.save()
            return Response({'message': 'Notícia recebida com sucesso', 'id': noticia.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoticiaListView(generics.ListAPIView):
    # queryset = Noticia.objects.all()
    queryset = Noticia.objects.all().order_by("-data_publicacao")
    serializer_class = NoticiaListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['categoria__nome', 'urgente', 'data_publicacao']
    ordering_fields = ['data_publicacao', 'criado_em']

@api_view(['PATCH'])
def marcar_como_urgente(request, pk):
    try:
        noticia = Noticia.objects.get(pk=pk)
        noticia.urgente = True
        noticia.save()
        return Response({'message': 'Notícia marcada como urgente.'}, status=status.HTTP_200_OK)
    except Noticia.DoesNotExist:
        return Response({'error': 'Notícia não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
