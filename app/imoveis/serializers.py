from rest_framework import serializers
from .models import Imovel, ImovelMidia

class ImovelMidiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImovelMidia
        fields = ['id', 'arquivo', 'created_at']

class ImovelSerializer(serializers.ModelSerializer):
    midias = ImovelMidiaSerializer(many=True, read_only=True)
    midias_upload = serializers.ListField(
        child=serializers.FileField(max_length=10000000, allow_empty_file=False, use_url=False), # Ex: max 10MB
        write_only=True,
        required=False
    )

    class Meta:
        model = Imovel
        fields = ['id', 'locador', 'tipo', 'categoria', 'endereco', 'descricao', 'valor', 'status', 'midias', 'midias_upload', 'created_at', 'updated_at']
        read_only_fields = ['locador', 'status']

    def create(self, validated_data):
        midias_data = validated_data.pop('midias_upload', [])
        imovel = Imovel.objects.create(**validated_data)
        
        for midia in midias_data:
            ImovelMidia.objects.create(imovel=imovel, arquivo=midia)
            
        return imovel
