import os
import ssl
import urllib3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''

default_cert_path = BASE_DIR / 'certs' / 'combined_certs.pem'
if default_cert_path.exists():
    os.environ['REQUESTS_CA_BUNDLE'] = str(default_cert_path)
    os.environ['SSL_CERT_FILE'] = str(default_cert_path)
    os.environ['GRPC_DEFAULT_SSL_ROOTS_FILE_PATH'] = str(default_cert_path)
else:
    ssl._create_default_https_context = ssl._create_unverified_context

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    import httpx
    
    original_init = httpx.Client.__init__
    
    def patched_init(self, *args, **kwargs):
        if 'verify' not in kwargs:
            kwargs['verify'] = False
        return original_init(self, *args, **kwargs)
    
    httpx.Client.__init__ = patched_init
    
    original_async_init = httpx.AsyncClient.__init__
    
    def patched_async_init(self, *args, **kwargs):
        if 'verify' not in kwargs:
            kwargs['verify'] = False
        return original_async_init(self, *args, **kwargs)
    
    httpx.AsyncClient.__init__ = patched_async_init
except:
    pass

ssl._create_default_https_context = ssl._create_unverified_context

import certifi
if default_cert_path.exists():
    try:
        with open(default_cert_path, 'rb') as f:
            cert_data = f.read()
        with open(certifi.where(), 'ab') as f:
            f.write(cert_data)
    except:
        pass

from django.conf import settings
from gigachat import GigaChat
from gigachat.models import Chat


class GigaChatClient:
    def __init__(self):
        self.client_id = getattr(settings, 'GIGACHAT_CLIENT_ID', os.environ.get('GIGACHAT_CLIENT_ID'))
        self.client_secret = getattr(settings, 'GIGACHAT_CLIENT_SECRET', os.environ.get('GIGACHAT_CLIENT_SECRET'))
        self.credentials = getattr(settings, 'GIGACHAT_CREDENTIALS', os.environ.get('GIGACHAT_CREDENTIALS'))
        self.auth_key = getattr(settings, 'GIGACHAT_AUTH_KEY', os.environ.get('GIGACHAT_AUTH_KEY', ''))
        self.scope = getattr(settings, 'GIGACHAT_SCOPE', 'GIGACHAT_API_PERS')
        self.cert_path = getattr(settings, 'GIGACHAT_CERT_PATH', os.environ.get('GIGACHAT_CERT_PATH', ''))
        verify_ssl = getattr(settings, 'GIGACHAT_VERIFY_SSL', os.environ.get('GIGACHAT_VERIFY_SSL', 'False')).lower() == 'true'
        
        gigachat_kwargs = {
            'scope': self.scope,
            'verify_ssl_certs': verify_ssl
        }
        
        if self.cert_path and os.path.exists(self.cert_path):
            gigachat_kwargs['ca_bundle_file'] = self.cert_path
        elif default_cert_path.exists():
            gigachat_kwargs['ca_bundle_file'] = str(default_cert_path)
        
        if self.auth_key:
            gigachat_kwargs['credentials'] = self.auth_key
            self.client = GigaChat(**gigachat_kwargs)
        elif self.credentials:
            gigachat_kwargs['credentials'] = self.credentials
            self.client = GigaChat(**gigachat_kwargs)
        elif self.client_id and self.client_secret:
            credentials_str = f'{self.client_id}:{self.client_secret}'
            gigachat_kwargs['credentials'] = credentials_str
            self.client = GigaChat(**gigachat_kwargs)
        elif self.client_id:
            gigachat_kwargs['credentials'] = self.client_id
            self.client = GigaChat(**gigachat_kwargs)
        else:
            raise ValueError('Необходимо установить GIGACHAT_CLIENT_ID в переменных окружения или settings.py')
    
    def chat(self, messages, model='GigaChat', temperature=0.7):
        try:
            chat_payload = {
                'model': model,
                'messages': messages,
                'temperature': temperature
            }
            response = self.client.chat(chat_payload)
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

