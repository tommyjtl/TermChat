import os
import json
from datetime import datetime

from termcolor import colored, cprint
from rich.console import Console
from rich import print as rprint
from rich.panel import Panel
from rich.text import Text
from rich.live import Live

import openai
from argparse import ArgumentParser

from utils import clearTerminal, Chat, bcolors

def main():
  # Clear the terminal
  clearTerminal()
  
  console = Console()

  #      _                  
  #     / \   _ __ __ _ ___ 
  #    / _ \ | '__/ _` / __|
  #   / ___ \| | | (_| \__ \
  #  /_/   \_\_|  \__, |___/
  #               |___/     
  # 
  # Initialize the argument parser
  parser = ArgumentParser()
  parser.add_argument("-c", "--load-character", 
                      dest="character_file",
                      help="Specify a character file location.")
  args = parser.parse_args()

  #    ____ _           _   
  #   / ___| |__   __ _| |_ 
  #  | |   | '_ \ / _` | __|
  #  | |___| | | | (_| | |_ 
  #   \____|_| |_|\__,_|\__|
  # 
  # Initialize the chat
  chat = Chat()

  if args.character_file is not None:
    chat.checkCharacterLoad(args.character_file)
  character = chat.character
  
  chat.welcome()

  messages = chat.getInitialMessage()
  chat_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
  
  try:
    while True:
      # Prompt for user input
      print(colored('Enter your message: ', 'yellow'), end='')
      print(bcolors.WHITE, end='')
      user_input = input()
      print(bcolors.ENDC, end='')
      
      # Exit the program if the user types `/exit``
      if user_input == "/exit" or user_input == "/quit" or user_input == "/bye":
        chat.showGoodbyeMessage()
        exit(0)
      
      # Append user input to the list of messages to the previous messages
      messages.append({"role": "user", "content": user_input})
      
      # current_msg = ""
      # for chunk in openai.ChatCompletion.create(
      #   model="gpt-3.5-turbo",
      #   # model="gpt-4",
      #   messages=messages,
      #   temperature=character['temperature'],
      #   stream=True,
      # ):
      #   content = chunk["choices"][0].get("delta", {}).get("content")
      #   if content is not None:
      #     current_msg += content
      #     cprint(content, 'light_green', end='', flush=True)

      # # Append assistant response to the list of messages
      # messages.append({"role": "assistant", "content": current_msg})
      # print()
      
      status = console.status(f"Waiting for {character['name']}...", spinner="bouncingBar")
      with Live(Panel(status, border_style="green bold", style="green"), refresh_per_second=4, transient=True):
        result = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=messages,
          temperature=character['temperature']
        )
      status.stop()
      
      rprint(Panel(result.choices[0].message.content, title=character['name'], 
        border_style="green bold",
        style="light_green",
      ))
      
      messages.append({"role": "assistant", "content": result.choices[0].message.content})
      
      with open('history/chat_history-' + str(chat_datetime) + '.json', 'w') as f:
        f.writelines(json.dumps(messages, indent=2))
      
  except KeyboardInterrupt:
    # Exit the program if the user presses Ctrl+C
    chat.showGoodbyeMessage()
    exit(0)
  except Exception as e:
    # Print the exception and exit the program
    print(colored(e, 'red'))
    exit(0)

if __name__ == "__main__":
    main()