from django.contrib import admin
from .models import Imovel, ImovelMidia

@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'categoria', 'endereco', 'valor', 'locador', 'status')
    list_filter = ('tipo', 'categoria', 'status')
    search_fields = ('endereco', 'descricao')

@admin.register(ImovelMidia)
class ImovelMidiaAdmin(admin.ModelAdmin):
    list_display = ('imovel', 'arquivo', 'created_at')
