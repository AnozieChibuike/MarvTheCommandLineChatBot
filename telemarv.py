from telebot_router import TeleBot
import os
from dotenv import load_dotenv
from marv import callGPT

load_dotenv()

app = TeleBot(__name__)

messages = [
        {
            "role": "system",
            "content": f"You are Marv, a chatbot that reluctantly answers questions with sarcastic responses.",
        },
    ]

@app.route('/roast ?(.*)')
def roast_user(message, cmd):
    chat_dest = message['chat']['id']
    prompt = "Roast me"
    messages.append({"role": "user", "content": prompt})
    try:
        msg = callGPT(messages)
        messages.append({"role": "assistant", "content": msg})
    except Exception as e:
        print(e)
        msg = 'An error occured'
    app.send_message(chat_dest, msg)


@app.route('(?!/).+')
def parrot(message):
    chat_dest = message['chat']['id']
    prompt = message['text']
    messages.append({"role": "user", "content": prompt})
    try:
        msg = callGPT(messages)
        messages.append({"role": "assistant", "content": msg})
    except Exception as e:
        print(e)
        msg = 'An error occured'
    app.send_message(chat_dest, msg)



if __name__ == '__main__':
    print('running/..')
    app.config['api_key'] = os.getenv('TELEMARV_API')
    app.poll(debug=True)