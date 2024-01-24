import os
import json
from datetime import datetime
import pyperclip
import readline

from termcolor import colored, cprint
from rich.console import Console
from rich import print as rprint
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich import box
from rich.markdown import Markdown

import openai
from argparse import ArgumentParser

from utils import clearTerminal, Chat, bcolors

def main():
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
  parser.add_argument("--stream",
                      dest="steaming_mode",
                      default=False,
                      action="store_true",
                      help="Enable streaming mode.")
  parser.add_argument("-e", "--load-engine", 
                      dest="engine_type",
                      default="gpt-3.5-turbo",
                      help="Specify an engine type, default is `gpt-3.5-turbo`.")
  parser.add_argument("--tts",
                      dest="enable_tts",
                      default=False,
                      action="store_true",
                      help="Enable text-to-speech.")
  parser.add_argument("-q", "--question", 
                      dest="direct_question",
                      default=False,
                      action="store_true",
                      help="Ask a question to the chatbot and get an answer directly.")
  args = parser.parse_args()
  
  if args.direct_question is False:
    # Clear the terminal
    clearTerminal()
  
  # Set up the console
  console = Console()

  #    ____ _           _   
  #   / ___| |__   __ _| |_ 
  #  | |   | '_ \ / _` | __|
  #  | |___| | | | (_| | |_ 
  #   \____|_| |_|\__,_|\__|
  # 
  # Initialize the chat
  chat = Chat()

  if args.character_file is not None:
    chat.loadCharacters(args.character_file)
  character = chat.character

  messages = chat.getInitialMessage()
  chat_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")    
  
  if args.direct_question is True:
    try:
      print(colored('Enter your question: ', 'yellow'), end='')
      print(bcolors.WHITE, end='')
      user_input = input()
      print(bcolors.ENDC, end='')
      
      messages.append({"role": "user", "content": user_input})
      
      current_msg = ""
      for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        messages=messages,
        temperature=character['temperature'],
        stream=True,
      ):
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
          current_msg += content
          cprint(content, 'light_green', end='', flush=True)
      
      print()
      exit(0)
    except KeyboardInterrupt:
      # Exit the program if the user presses Ctrl+C
      chat.showGoodbyeMessage()
      exit(0)
    except Exception as e:
      # Print the exception and exit the program
      print(colored(e, 'red'))
      exit(0)
    
  chat.welcome(engine_type=args.engine_type)
  
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
      
      if args.steaming_mode:
        current_msg = ""
        for chunk in openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          # model="gpt-4",
          messages=messages,
          temperature=character['temperature'],
          stream=True,
        ):
          content = chunk["choices"][0].get("delta", {}).get("content")
          if content is not None:
            current_msg += content
            cprint(content, 'light_green', end='', flush=True)

        # Append assistant response to the list of messages
        messages.append({"role": "assistant", "content": current_msg})
        print()
      else:
          status = console.status(f"Waiting for {character['name']}...", spinner="bouncingBar")
          with Live(Panel(status, border_style="green bold", style="green"), refresh_per_second=4, transient=True):
            try:
              result = openai.ChatCompletion.create(
                model=args.engine_type,
                messages=messages,
                temperature=character['temperature'],
                timeout=30 # set a request timeout of 30 seconds
              )
            except Exception as e:
              error_msg = [e]
              rprint(Panel(error_msg, title="System", border_style="red bold", style="red"))
              
          status.stop()
          
          # Copy the response to the clipboard
          pyperclip.copy(result.choices[0].message.content)
          
          response = result.choices[0].message.content
          rprint(Panel(Markdown(response), 
            title=character['name'], 
            highlight=True,
            border_style="green bold",
            style="green",
          ))
          
          rprint(Panel("Copied to clipboard", 
                       title="SYSTEM", 
                       border_style="bright_black", 
                       style="bright_black"
          ))
          
          if args.enable_tts:
            chat.say(result.choices[0].message.content, character['voice'])
            
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