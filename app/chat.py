import time

from ollama import ResponseError
from app.dependencies import ollama_client

from app.models import ChatRequest, ChatResponse

chat_histories = {}


def chat_message(chat_req: ChatRequest):
    start_time = time.perf_counter()

    user_name = chat_req.user_name
    user_message = chat_req.message

    conversation_history = chat_histories.get(user_name, [])
    current_message = {
        'role': 'user',
        'content': f'{user_message}'
    }
    messages = conversation_history + [current_message]
    try:
        print('process ollama')

        response = ollama_client.chat(
            model='llama3.2:1b-instruct-q5_K_M',
            messages=messages
        )

        assistant_response = response['message']['content']
        conversation_history += [
            {
                'role': 'user',
                'content': user_message
            },
            {
                'role': 'assistant',
                'content': assistant_response
            }
        ]

        chat_histories[user_name] = conversation_history[-10:]
        process_time = time.perf_counter() - start_time

        chat_response = ChatResponse(
            user_name=user_name,
            message=assistant_response,
            response_time=format_time(process_time)

        )

        return chat_response


    except ResponseError as e:
        return {
            'Error': e.error
        }

def format_time(second: float):
    minutes = int(second//60)
    remaining_second = int(second % 60)
    if minutes > 0:
        return f'{minutes}m{remaining_second}s'

    return f'{remaining_second}s'