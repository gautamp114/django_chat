import json
from channels.generic.websocket import WebsocketConsumer

from chat.models import Message, Contact, Chat

from asgiref.sync import async_to_sync

from django.contrib.auth.models import User

from itertools import chain

from chat.views import last_10_messages, get_msg_contact, get_chat

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        print("fetched_data",data)
        messages = last_10_messages(data['chatId'])
        
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }

        self.send_message(content)
        

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.contact.user.username,
            'content': message.content,
            'timestamp': str(message.timestamp),
        }


    def new_message(self, data):
        # print(data)
        author = data['from']
        author_user = get_msg_contact(author)
        message = Message.objects.create(
            contact=author_user,
            content=data['message'],
        )

        chat_me = get_chat(data['chatId'])
        chat_me.messages.add(message)
        chat_me.save()

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }

        return self.send_chat_message(content)


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }


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
        # print(text_data)
        data = json.loads(text_data)
        self.commands[data['command']](self,data) ## get the command according to frontend



    def send_chat_message(self, message):
        # Send message to room group
        ## broadcast the message
        async_to_sync( self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        print("send message", message);
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        # print('chat_message', event['message'])
        message = event['message']

        # print('message ho yo',message)
        # actually Send message to WebSocket
        self.send(text_data=json.dumps(message))
