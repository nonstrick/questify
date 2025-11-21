import os
from django.conf import settings
from gigachat import GigaChat


class GigaChatClient:
    def __init__(self):
        self.client_id = getattr(settings, 'GIGACHAT_CLIENT_ID', os.environ.get('GIGACHAT_CLIENT_ID'))
        self.client_secret = getattr(settings, 'GIGACHAT_CLIENT_SECRET', os.environ.get('GIGACHAT_CLIENT_SECRET'))
        self.credentials = getattr(settings, 'GIGACHAT_CREDENTIALS', os.environ.get('GIGACHAT_CREDENTIALS'))
        self.scope = getattr(settings, 'GIGACHAT_SCOPE', 'GIGACHAT_API_PERS')
        
        if not self.credentials and (not self.client_id or not self.client_secret):
            raise ValueError('Необходимо установить GIGACHAT_CREDENTIALS или GIGACHAT_CLIENT_ID и GIGACHAT_CLIENT_SECRET')
        
        if self.credentials:
            self.client = GigaChat(credentials=self.credentials, scope=self.scope)
        else:
            self.client = GigaChat(
                credentials=f'{self.client_id}:{self.client_secret}',
                scope=self.scope
            )
    
    def chat(self, messages, model='GigaChat', temperature=0.7):
        try:
            response = self.client.chat(messages, model=model, temperature=temperature)
            return response
        except Exception as e:
            raise Exception(f'Ошибка запроса к GigaChat: {str(e)}')
    
    def get_response_text(self, messages, model='GigaChat', temperature=0.7):
        try:
            response = self.chat(messages, model, temperature)
            if hasattr(response, 'choices') and len(response.choices) > 0:
                return response.choices[0].message.content
            return None
        except Exception as e:
            raise Exception(f'Ошибка получения ответа от GigaChat: {str(e)}')

