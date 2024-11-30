from fastapi import FastAPI

from app.chat import chat_message, chat_histories
from app.models import ChatRequest

app = FastAPI()

@app.get('/')
def root():
    return {
        'message': 'Hello World!'
    }

@app.post('/chat')
def chat(chat_request: ChatRequest):
    return chat_message(chat_request)

@app.get('/chat/{user_name}')
def chat_history(user_name):
    return chat_histories.get(user_name, [])