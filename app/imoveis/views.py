from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Imovel
from .serializers import ImovelSerializer
from .permissions import IsLocador, IsOwnerOrReadOnly

class ImovelViewSet(viewsets.ModelViewSet):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer
    
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
