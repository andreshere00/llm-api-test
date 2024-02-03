from rest_framework import serializers
from .models import File

class Serializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'creation_date']