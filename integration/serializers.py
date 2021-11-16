# serializers.py
from rest_framework import serializers

from .models import Parrain, Campaign

class ParrainSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()
    background_color = serializers.SerializerMethodField()
    text_color = serializers.SerializerMethodField()

    class Meta:
        model = Parrain
        fields = ('message', 'background_color', 'text_color')

    def get_message(self, obj):
        return obj.campaign.message_personnalized(obj)

    def get_background_color(self, obj):
        return obj.campaign.background_color

    def get_text_color(self, obj):
        return obj.campaign.text_color

class CreateParrainSerializer(serializers.ModelSerializer):
    test = serializers.SerializerMethodField()
    class Meta:
        model = Parrain
        fields = ('__all__')