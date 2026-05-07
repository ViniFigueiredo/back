from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Imovel
from .serializers import ImovelSerializer
from .permissions import IsLocador, IsOwnerOrReadOnly

class ImovelViewSet(viewsets.ModelViewSet):
    serializer_class = ImovelSerializer
    
    def get_queryset(self):
        """
        Retorna o queryset base.
        Para ações de edição (update, partial_update, destroy), 
        filtramos apenas pelos imóveis do próprio usuário para garantir 404 se não for o dono.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return Imovel.objects.filter(locador=self.request.user)
        return Imovel.objects.all()
    
    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que a view requer.
        - GET/Listar pode ser feito por qualquer autenticado (ou público dependendo da regra).
        - POST requer IsLocador.
        - PUT/PATCH/DELETE requer ser o dono do imóvel.
        """
        if self.action in ['create']:
            permission_classes = [IsLocador]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticated] # Ajustar se a listagem puder ser pública
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(locador=self.request.user)
