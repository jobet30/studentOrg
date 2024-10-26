from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

def create(self, validated_data):
        """
        Create and return a new Notification instance, given the validated data.
        """
        return Notification.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Notification instance, given the validated data.
        """
        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance