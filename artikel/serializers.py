from rest_framework import serializers
from .models import Artikel
from artikel.models import Kategori
from django.contrib.auth.models import User

class ArtikelSerializer(serializers.ModelSerializer):
    kategori_nama = serializers.CharField(source='kategori.nama', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Artikel
        fields = [
            'id', 'judul', 'konten', 'gambar',
            'kategori', 'kategori_nama',     # `kategori` untuk input, `kategori_nama` untuk tampilkan nama
            'status', 'created_at',
            'created_by', 'created_by_username',
        ]
        read_only_fields = ['created_by', 'created_by_username', 'kategori_nama', 'created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def get_serializer_context(self):
        return {'request': self.context['request']}
