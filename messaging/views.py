from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from django.contrib.auth.models import User

class ConversationViewSet(viewsets.ViewSet):
    def create(self, request):
        participants = request.data.get('participants')
        if participants:
            conversation = Conversation.objects.create()
            conversation.participants.set(participants)
            conversation.save()
            return Response({'status': 'Conversation started', 'conversation_id': conversation.id})
        return Response({'status': 'Error', 'message': 'Participants required'}, status=400)

    def list(self, request):
        conversations = Conversation.objects.filter(participants=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ViewSet):
    def create(self, request):
        conversation_id = request.data.get('conversation_id')
        content = request.data.get('content')

        conversation = get_object_or_404(Conversation, id=conversation_id)
        message = Message.objects.create(conversation=conversation, sender=request.user, content=content)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        conversation = get_object_or_404(Conversation, id=pk)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)