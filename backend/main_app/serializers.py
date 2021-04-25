from rest_framework import serializers
from .models import *


class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        depth = 2
        model = Message
        fields = ('id', 'description', 'created_at', 'answer', 'correct', 'incorrect', 'kml', 'num_correct', 'num_incorrect')
