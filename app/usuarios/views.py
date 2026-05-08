from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import TypeUserSerializer, UserSerializer, LoginSerializer, PublicUserSerializer, UpdateUserSerializer
from .models import User

# IsAuthenticated - só usuário logado pode acessar
# AllowAny - qualquer usuário pode acessar

#################################### GET #########################################

# MEU PERFIL - Retorna dados do usuário autenticado
@api_view(['GET'])
@permission_classes([AllowAny])
def profile(request):
    user = request.user
    
    if user.is_anonymous:
        from .models import User
        user = User.objects.first()

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def type_user(request):
    user = request.user  # já vem autenticado pelo JWT

    serializer = TypeUserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)

# BUSCAR USUÁRIO POR ID - Retorna dados públicos de qualquer usuário (SEM AUTENTICAÇÃO)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_by_id(request, user_id):
    try:
        usuario = User.objects.get(id=user_id)
        serializer = PublicUserSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {'error': 'Usuário não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Erro ao buscar usuário: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all(request):
    pass


################################# POST ###########################################

# CRIAR USUÁRIO
@api_view(['POST'])
@permission_classes([AllowAny])
def create(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        # Verificar duplicatas antes de salvar
        email = serializer.validated_data.get('email')
        cpf = serializer.validated_data.get('cpf')
        username = serializer.validated_data.get('username')

        # Verificar se email já existe
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Este email já está cadastrado'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar se CPF já existe
        if User.objects.filter(cpf=cpf).exists():
            return Response(
                {'error': 'Este CPF já está cadastrado'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar se username já existe
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Este username já está em uso'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Se passou todas as validações, salvar
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LOGIN - Gera tokens JWT
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        usuario = serializer.validated_data['usuario']
        refresh = RefreshToken.for_user(usuario)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'usuario': UserSerializer(usuario).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# REFRESH TOKEN - Gera novo access token usando o refresh token
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    from rest_framework_simplejwt.views import TokenRefreshView
    return TokenRefreshView.as_view()(request)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def destroy(request):
    pass


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update(request):
    usuario = request.user  # O usuário autenticado pode alterar apenas seu próprio perfil

    serializer = UpdateUserSerializer(usuario, data=request.data, partial=True)

    if serializer.is_valid():
        # Verificar duplicatas para email e username, se fornecidos
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')

        if email and User.objects.filter(email=email).exclude(id=usuario.id).exists():
            return Response(
                {'error': 'Este email já está cadastrado'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if username and User.objects.filter(username=username).exclude(id=usuario.id).exists():
            return Response(
                {'error': 'Este username já está em uso'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Salvar as alterações
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)