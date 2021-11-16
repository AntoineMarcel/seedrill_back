# serializers.py
from rest_framework import serializers

from emails.utils import replace_variable

from emails.models import Person
class BannerSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()
    background_color = serializers.SerializerMethodField()
    text_color = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('message', 'background_color', 'text_color')

    def get_message(self, obj):
        return replace_variable(obj.sequence.message, obj)

    def get_background_color(self, obj):
        return obj.sequence.background_color

    def get_text_color(self, obj):
        return obj.sequence.text_color

class CreateParrainSerializer(serializers.ModelSerializer):
    test = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = ('__all__')