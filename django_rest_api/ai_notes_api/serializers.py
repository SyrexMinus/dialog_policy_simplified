from rest_framework import serializers
from .models import Note
from .utils import DateTimeExtractor


class NoteSerializer(serializers.Serializer):
    input_text = serializers.CharField()
    times = serializers.CharField()
    dates = serializers.CharField()

    def create(self, validated_data):
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.input_text = validated_data.get('input_text', instance.input_text)

        date_time_extractor = DateTimeExtractor(instance.input_text)
        instance.times = "".join(date_time_extractor.extracted_times)
        instance.dates = "".join(date_time_extractor.extracted_dates)

        instance.save()
        return instance
