from openai import OpenAI, APIConnectionError, OpenAIError, AuthenticationError
from dotenv import load_dotenv
import json
from colorama import Fore, Back, Style
from unratedwriting import typewrite
import argparse
import os


load_dotenv()
try:
    client = OpenAI()
except OpenAIError as e:
    print()
    typewrite(f'{Fore.RED}RuntimeError: {e}{Style.RESET_ALL}')
    print()
    exit(1)


def main(bot_name="Marv"):
    """
    >>>2 + 2
    4
    """
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
    retries = 0
    while True:
            inp = input(f"{Fore.GREEN}{name}{Style.RESET_ALL}: ")
            messages.append({"role": "user", "content": inp})
            try:
                jsonResponse = callGPT(messages)
                messages.append({"role": "assistant", "content": jsonResponse})
                print()
                typewrite(f"{Fore.YELLOW}{bot_name}{Style.RESET_ALL}: {jsonResponse}")
                print()
            except APIConnectionError:
                if retries == 3:
                    break
                print()
                typewrite(f'{Fore.RED}ConnectionError: You need an internet connection to use Marv{Style.RESET_ALL}')
                print()
                retries += 1
                typewrite(f'retrying({retries}/3).....')
                print()
            except AuthenticationError:
                typewrite(f'{Fore.RED}AuthenticationError: Invalid or Incorrect API_KEY{Style.RESET_ALL}')
                break
                
def callGPT(messages):
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
    return jsonResponse



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Marv the sarcastic bot.")
    parser.add_argument("--name", type=str, help="Override the default bot name (Marv)")
    args = parser.parse_args()
    if args.name:
        main(bot_name=args.name)
    else:
        main()
