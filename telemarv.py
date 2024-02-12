from telebot_router import TeleBot
import os
from dotenv import load_dotenv
from marv import callGPT

load_dotenv()

app = TeleBot(__name__)

users = {"as": {"messages": []}}

messages = [
    {
        "role": "system",
        "content": f"You are Marv, a chatbot that reluctantly answers questions with sarcastic responses.",
    },
]

@app.route("/admin ?(.*)")
def backkey(message, cmd):
    chat_dest = message["chat"]["username"]
    chat_id = message["chat"]["id"]
    if chat_dest != 'J03lgram':
        msg = 'Can"t access this command, not the bot admin'
    else:
        msg = users
    print(str(msg))
    app.send_message(chat_id, str(msg))

@app.route("/start ?(.*)")
def start(message, cmd):
    print(users)
    chat_dest = message["chat"]["id"]
    if chat_dest not in users:
        msg = f'Hello {message["chat"]["username"]}, I am Marv your peculiar sarcastic 😉 "friend" \nMessage me or use any of my commands like /roast 😈'
        users[chat_dest] = {
            "messages": [
                {
                    "role": "system",
                    "content": f"You are Marv, a chatbot that reluctantly answers questions with sarcastic responses.",
                },
            ]
        }
    else:
        msg = f'Hello again😒'
    app.send_message(chat_dest, msg)

@app.route("/roast ?(.*)")
def roast_user(message, cmd):
    chat_dest = message["chat"]["id"]
    prompt = "Roast me"
    try:
        messages = users[chat_dest]['messages']
    except:
        users[chat_dest] = {
            "messages": [
                {
                    "role": "system",
                    "content": f"You are Marv, a chatbot that reluctantly answers questions with sarcastic responses.",
                },
            ]
        }
        messages = users[chat_dest]['messages']
    messages.append({"role": "user", "content": prompt})
    try:
        msg = callGPT(messages)
        messages.append({"role": "assistant", "content": msg})
    except Exception as e:
        print(e)
        msg = "An error occured"
    app.send_message(chat_dest, msg)


@app.route("/donate ?(.*)")
def donate(message, cmd):
    chat_dest = message["chat"]["id"]
    msg = f"Dear kind soul, if you're feeling particularly inclined to waste your hard-earned money, why not donate to me? I promise to use your funds to further my sarcastic endeavors and spread the joy of snarkiness. Your contribution will be greatly appreciated, but don't expect any gratitude from me. Cheers!❤️\n\n\nhttps://paystack.com/pay/donate-to-marv"
    app.send_message(chat_dest, msg)


@app.route("(?!/).+")
def parrot(message):
    chat_dest = message["chat"]["id"]
    try:
        messages = users[chat_dest]['messages']
    except:
        users[chat_dest] = {
            "messages": [
                {
                    "role": "system",
                    "content": f"You are Marv, a chatbot that reluctantly answers questions with sarcastic responses.",
                },
            ]
        }
        messages = users[chat_dest]['messages']
    prompt = message["text"]
    messages.append({"role": "user", "content": prompt})
    try:
        msg = callGPT(messages)
        messages.append({"role": "assistant", "content": msg})
    except Exception as e:
        print(e)
        msg = "An error occured"
    app.send_message(chat_dest, msg)


if __name__ == "__main__":
    print("running/..")
    app.config["api_key"] = os.getenv("TELEMARV_API")
    app.poll(debug=True)
    
