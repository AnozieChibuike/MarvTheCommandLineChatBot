from openai import OpenAI
from dotenv import load_dotenv
import json
from colorama import Fore, Back, Style
from unratedwriting import typewrite
import argparse


load_dotenv()
client = OpenAI()


def main(bot_name="Marv"):
    print()
    typewrite(f"Hi I am {Fore.YELLOW}{bot_name}{Style.RESET_ALL} your sarcastic AI bot")
    print()
    name = input(f"What is your name: {Fore.GREEN}")
    print(f"{Style.RESET_ALL}")
    typewrite("Enter your message")
    print()
    messages = [
        {
            "role": "system",
            "content": f"You are {bot_name}, a chatbot that reluctantly answers questions with sarcastic responses.",
        },
    ]

    while True:
        inp = input(f"{Fore.GREEN}{name}{Style.RESET_ALL}: ")
        messages.append({"role": "user", "content": inp})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.5,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        jsonResponse = json.loads(response.model_dump_json())["choices"][0]["message"][
            "content"
        ]
        messages.append({"role": "assistant", "content": jsonResponse})
        print()
        typewrite(f"{Fore.YELLOW}{bot_name}{Style.RESET_ALL}: {jsonResponse}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Marv the sarcastic bot.")
    parser.add_argument("--name", type=str, help="Override the default bot name (Marv)")
    args = parser.parse_args()
    if args.name:
        main(bot_name=args.name)
    else:
        main()
