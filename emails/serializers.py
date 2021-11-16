from rest_framework import serializers

from .models import Person, EmailModel, Sequence

class SequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequence
        fields = ('__all__')

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('__all__')

class EmailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailModel
        exclude = ('order', )