# chat/views.py
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from chat.models import ChatMessage
from chat.serializers import ChatMessageSerializer


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


def rooms(request):
    return render(request, 'chat/rooms.html')


class GetChatMessages(generics.ListAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        room_name = request.GET['room_name']

        chat_messages = ChatMessage.objects.filter(user=user, room_name=room_name)
        serializer = self.get_serializer(chat_messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)