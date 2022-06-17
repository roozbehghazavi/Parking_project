# chat/consumers.py
import datetime
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        print(self.scope['user'])

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = event['user']
        print(user)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))


class RoomsConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'chat_rooms'
        print('rooms')

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text_data_json['time'] = datetime.datetime.now().__str__()
        message = text_data_json['message']
        user = text_data_json['user']
        time = text_data_json['time']
        print(self.scope['user'])

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'time': time
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = event['user']
        time = event['time']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'time': time
        }))
