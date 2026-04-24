from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        if not username:
            raise ValueError('O username é obrigatório')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, null=False)
    cpf = models.CharField(max_length=11, unique=True, null=False)
    idade = models.CharField(max_length=3, null=False)
    sexo = models.CharField(max_length=20, null=False)
    profissao = models.CharField(max_length=100, null=False)
    rua = models.CharField(max_length=150, null=False)
    bairro = models.CharField(max_length=100, null=False)
    cidade = models.CharField(max_length=100, default="Cedro")  # levando em conta que se trata do cedro
    estado = models.CharField(max_length=2, default="CE")
    numero = models.IntegerField(null=False)
    email = models.EmailField(unique=True, null=False)

    class UserType(models.TextChoices):
        LOCADOR = 'locador', 'Locador'
        LOCATARIO = 'locatario', 'Locatário'

    tipo_de_usuario = models.CharField(max_length=10, choices=UserType.choices, null=False)

    # Campos obrigatórios para AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser



    

