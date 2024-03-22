import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import asyncio

class SyncTestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("Connection established!")
        self.send(text_data=json.dumps({
            'type':'connection established',
            'message': 'You are now connected'
        }))
        for i in range (1, 10):
            self.send(text_data=json.dumps({
            'type':'chat',
            'message':i
            }))

    def receive(self, text_data):
        text_data_json=json.loads(text_data)
        message=text_data_json['message']
        print('Message:', message)
        self.send(text_data=json.dumps({
            'type':'your_message',
            'message':message

        }))
    def disconnect(self,close_code):
        print("Web Socket Disconnected")




class AsyncTestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("Connection established!")
        await self.send(text_data=json.dumps({
            'type':'connection established',
            'message': 'You are now connected'
        }))
        for i in range (1, 10):
            await self.send(text_data=json.dumps({
            'type':'chat',
            'message':i

            })) 
    
    async def receive(self, text_data):
        text_data_json=json.loads(text_data)
        message=text_data_json['message']
        print('Message:', message)
        await self.send(text_data=json.dumps({
            'type':'your_message',
            'message':message

        }))