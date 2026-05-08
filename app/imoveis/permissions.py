from rest_framework import permissions

class IsLocador(permissions.BasePermission):
    """
    Permite acesso apenas se o usuário for do tipo 'locador'.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'tipo_de_usuario', None) == 'locador')

class IsLocatario(permissions.BasePermission):
    """
    Permite acesso apenas se o usuário for do tipo 'locatario'.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'tipo_de_usuario', None) == 'locatario')

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir que apenas os donos (locadores) do imóvel possam editá-lo.
    """
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura são dadas a qualquer requisição segura (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permissões de escrita são dadas apenas ao locador dono do imóvel
        return obj.locador == request.user
