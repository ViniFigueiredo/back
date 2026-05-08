from django.db import models
from django.conf import settings

class Imovel(models.Model):
    class CategoriaChoices(models.TextChoices):
        RESIDENCIAL = 'residencial', 'Residencial'
        COMERCIAL = 'comercial', 'Comercial'
        
    class TipoChoices(models.TextChoices):
        CASA = 'casa', 'Casa'
        APARTAMENTO = 'apartamento', 'Apartamento'
        QUARTO = 'quarto', 'Quarto'
        TERRENO = 'terreno', 'Terreno'
        
    class StatusChoices(models.TextChoices):
        DISPONIVEL = 'disponivel', 'Disponível'
        INDISPONIVEL = 'indisponivel', 'Indisponível'
        OCULTO = 'oculto', 'Oculto'

    locador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='imoveis')
    tipo = models.CharField(max_length=50, choices=TipoChoices.choices)
    categoria = models.CharField(max_length=50, choices=CategoriaChoices.choices)
    endereco = models.CharField(max_length=255)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.DISPONIVEL)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo} - {self.endereco}"

class ImovelMidia(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name='midias')
    arquivo = models.FileField(upload_to='imoveis/midias/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mídia {self.id} - Imóvel {self.imovel.id}"
    

