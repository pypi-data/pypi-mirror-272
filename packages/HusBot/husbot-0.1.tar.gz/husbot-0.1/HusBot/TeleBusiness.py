import httpx
import json

class HClient:
    def __init__(self, token):
        self.token = token
        self.api_url = self.compose_api_url("")
        self.handlers = {}
        self.deleted_message_handler = None
        self.edited_message_handler = None

    def compose_api_url(self, method) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def message_handler(self, message):
        def decorator(func):
            self.handlers[message] = func
            return func
        return decorator

    def deleted_message(self):
        def decorator(func):
            self.deleted_message_handler = func
            return func
        return decorator
        
    def edited_message(self):
        def decorator(func):
            self.edited_message_handler = func
            return func
        return decorator
    def send_message(self, business_connection_id, chat_id, text):
        return httpx.post(
            self.compose_api_url("sendMessage"),
            data={
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "text": text,
                
            }
        ).json()

    def send_message_button(self, business_connection_id: str, chat_id: int, text: str, keyboard) -> dict:
        return httpx.post(
            self.compose_api_url("sendMessage"),
            data={
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "text": text,
                'reply_markup': json.dumps(keyboard)
            }
        ).json()

    def send_sticker(self, business_connection_id: str, chat_id: int, sticker: str) -> dict:
        return httpx.post(
            self.compose_api_url("sendSticker"),
            data={
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "sticker": sticker,
            }
        ).json()

    def send_photo(self, business_connection_id: str, chat_id: int, photo: str) -> dict:
        return httpx.post(
            self.compose_api_url("sendPhoto"),
            data={
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "photo": photo,
            }
        ).json()

    def send_document(self, business_connection_id: str, chat_id: int, document: str) -> dict:
        return httpx.post(
            self.compose_api_url("sendDocument"),
            data={
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "document": document,
            }
        ).json()

    def send_voice(self, business_connection_id: str, chat_id: int, voice: str) -> dict:
        return httpx.post(
            self.compose_api_url("sendVoice"),
            data={
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "voice": voice,
            }
        ).json()

    def send_video(self, business_connection_id: str, chat_id: int, video: str) -> dict:
        return httpx.post(
            self.compose_api_url("sendVideo"),
            data={
                "business_connection_id": business_connection_id,
                "chat_id": chat_id,
                "video": video,
            }
        ).json()

    def get_updates(self, offset=None, limit=100):
        return httpx.post(
            self.compose_api_url("getUpdates"),
            data={
                "offset": offset,
                "limit": limit,
            }
        ).json()

    def RunHClient(self):
        offset = 0
        while True:
            try:
                updates = self.get_updates(offset=offset, limit=100)
                
                for update in updates['result']:
                    if 'update_id' in update:
                        offset = update['update_id'] + 1
                    if 'business_message' in update and 'business_connection_id' in update['business_message']:
                        
                        if 'text' in update['business_message']:
                            business_connection_id = update['business_message']['business_connection_id']
                            message_id = update['business_message']['message_id']
                            chat_id = update['business_message']['chat']['id']
                            message_text = update['business_message']['text']
                            first_name = update['business_message']['chat']['first_name']
                            username = update['business_message']['chat']['username']
                            other = [message_id,first_name,username]
                            handler = self.handlers.get(message_text)
                            if handler is not None: handler(business_connection_id, chat_id, message_text,other)
                            else:
                                self.handlers.get(True)(business_connection_id, chat_id, message_text,other)
                    elif 'deleted_business_messages' in update and 'business_connection_id' in update['deleted_business_messages']:
                    	business_connection_id = update['deleted_business_messages']['business_connection_id']
                    	message_ids = update['deleted_business_messages']['message_ids']
                    	chat_id = update['deleted_business_messages']['chat']['id']
                    	first_name = update['deleted_business_messages']['chat']['first_name']
                    	username = update['deleted_business_messages']['chat']['username']
                    	other = [first_name,username]
                    	
                    	if self.deleted_message_handler is not None:
                    	    self.deleted_message_handler(business_connection_id, chat_id, message_ids,other)
                    elif 'edited_business_message' in update and 'business_connection_id' in update['edited_business_message']:
                    	business_connection_id = update['edited_business_message']['business_connection_id']
                    	message_id = update['edited_business_message']['message_id']
                    	message_text = update['edited_business_message']['text']
                    	chat_id = update['edited_business_message']['chat']['id']
                    	first_name = update['edited_business_message']['chat']['first_name']
                    	username = update['edited_business_message']['chat']['username']
                    	other = [first_name,username]
                    	
                    	
                    	if self.edited_message_handler is not None:
                    	    self.edited_message_handler(business_connection_id, chat_id, message_text,message_id,other)
            except Exception as e:
                print(f"An error occurred: {e}")