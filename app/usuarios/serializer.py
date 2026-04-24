from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        error_messages={
            'unique': 'Este nome de usuário já está em uso.'
        }
    )
    cpf = serializers.CharField(
        error_messages={
            'unique': 'Este CPF já está cadastrado.'
        }
    )
    email = serializers.EmailField(
        error_messages={
            'unique': 'Este email já está cadastrado.'
        }
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'cpf', 'idade',
            'sexo', 'profissao', 'rua', 'bairro',   
            'cidade', 'estado', 'numero', 
            'email', 'password', 'tipo_de_usuario'
        ]
        
        extra_kwargs = {
            'password': {'write_only': True}  # Senha não aparece na resposta por padrão
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'idade',
            'sexo',
            'profissao',
            'rua',
            'bairro',
            'cidade',
            'estado',
            'numero',
            'tipo_de_usuario',
            'created_at',
            'updated_at'
        ]


class TypeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'tipo_de_usuario',
            'created_at',
            'updated_at'
        ]

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'idade', 'sexo', 'profissao', 
            'rua', 'bairro', 'cidade', 'estado', 'numero', 'email'
        ]
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
            'idade': {'required': False},
            'sexo': {'required': False},
            'profissao': {'required': False},
            'rua': {'required': False},
            'bairro': {'required': False},
            'cidade': {'required': False},
            'estado': {'required': False},
            'numero': {'required': False},
        }


class LoginSerializer(serializers.Serializer):
    """Serializer para login do usuário"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth.hashers import check_password
        
        email = data.get('email')
        password = data.get('password')

        try:
            usuario = User.objects.get(email=email)
            if not check_password(password, usuario.password):
                raise serializers.ValidationError('Credenciais inválidas')
        except User.DoesNotExist:
            raise serializers.ValidationError('Credenciais inválidas')

        data['usuario'] = usuario
        return data


