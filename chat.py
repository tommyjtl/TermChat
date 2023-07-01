import os
import json
from datetime import datetime
from termcolor import colored, cprint
from rich.console import Console
from rich import print as rprint
import sys

import openai
from utils import clearTerminal

# Clear the terminal
clearTerminal()

openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
  print(colored('OPENAI_API_KEY is not set as a system environment variable', 'red'))
  exit(0)
else:
  print('[SYSTEM]', colored('OPENAI_API_KEY found.', 'green'))
  print('[SYSTEM]', colored('Chat dialogue will be saved to `chat.json`.', 'green'))
  print('[SYSTEM]', colored('<Press Ctrl+C to exit>', 'green'))
  
if not os.path.isdir("history"):
    print("Directory does not exist.")
    os.mkdir("history")

initial_msgs = [{"role": "system", "content": "You are a helpful assistant."}]
chat_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
console = Console()

def main():
  try:
    while True:
      # Prompt for user input
      user_input = input(colored('Enter your message: ', 'yellow'))
      
      # Append user input to the list of messages to the previous messages
      initial_msgs.append({"role": "user", "content": user_input})

      # Display indicator that the program is waiting for GPT-3
      # with console.status(colored('Waiting for GPT...','green')) as status:
      # Retrieve the response from the API
      current_msg = ""
      for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=initial_msgs,
        stream=True,
      ):
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
          current_msg += content
          # clearTerminal()
          cprint(content, 'green', end='', flush=True)

      # Append assistant response to the list of messages
      initial_msgs.append({"role": "assistant", "content": current_msg})
      
      print()
      
      with open('history/chat_history-' + str(chat_datetime) + '.json', 'w') as f:
        f.writelines(json.dumps(initial_msgs, indent=2))
      
  except KeyboardInterrupt:
    # Exit the program if the user presses Ctrl+C
    print('\n[SYSTEM]', colored("Bye!", 'green'))
    exit(0)
  except Exception as e:
    # Print the exception and exit the program
    print(colored(e, 'red'))
    exit(0)

if __name__ == "__main__":
    main()