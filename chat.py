import os
import json
from datetime import datetime
from termcolor import colored, cprint
from rich.console import Console
from rich import print as rprint
import sys

import openai
from utils import clearTerminal
from argparse import ArgumentParser

# Clear the terminal
clearTerminal()

#      _                  
#     / \   _ __ __ _ ___ 
#    / _ \ | '__/ _` / __|
#   / ___ \| | | (_| \__ \
#  /_/   \_\_|  \__, |___/
#               |___/     
# Initialize the argument parser
parser = ArgumentParser()
parser.add_argument("-c", "--load-character", 
                    dest="character_file",
                    help="Specify a character file location.")
args = parser.parse_args()

character = {
  "name": "Default Assistant",
  "system": "You are a helpful assistant.",
  "temperature": 0,
}

if args.character_file is not None:
  # check if the character profile exists
  if not os.path.isfile(args.character_file):
    print(colored('[SYSTEM]\t', 'white') + colored(f"The file path you specified does not exist: `{args.character_file}`", 'red'))
    exit(0)
    
  # check if the character's prompt exists
  if not os.path.isfile(args.character_file.replace('.json', '.txt')):
    print(colored('[SYSTEM]\t', 'white') + colored(f"The file path you specified does not exist: `{args.character_file}`", 'red'))
    exit(0)
  
  # load the character profile
  with open(args.character_file) as f:
    character_profile = json.load(f)
    character['name'] = character_profile['name']
    character['temperature'] = character_profile['temperature']
    
  # load the character's prompt
  with open(args.character_file.replace('.json', '.txt')) as f:
    character['system'] = ''.join(f.read())

# Checking OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
  print(colored('[SYSTEM]\t', 'white') + colored('OPENAI_API_KEY is not set as a system environment variable', 'red'))
  exit(0)
else:
  print(colored('[SYSTEM]\t', 'white') + colored(f"{character['name']} is ready now.", 'green'))
  print(colored('[SYSTEM]\t', 'white') + colored('Chat dialogue will be saved to `history/`', 'green'))
  print(colored('[SYSTEM]\t', 'white') + colored('<Press Ctrl+C to exit>', 'green'))
  
if not os.path.isdir("history"):
    print("Directory does not exist.")
    os.mkdir("history")

initial_msgs = [{"role": "system", "content": character['system']}]
chat_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
console = Console()

def main():
  try:
    while True:
      # Prompt for user input
      user_input = input(colored('Enter message:\t', 'yellow'))
      
      if user_input == "/exit":
        print(colored('\n[SYSTEM]\t', 'white') + colored("Bye!", 'green'))
        exit(0)
        break
      
      # Append user input to the list of messages to the previous messages
      initial_msgs.append({"role": "user", "content": user_input})

      # Display indicator that the program is waiting for GPT-3
      # with console.status(colored('Waiting for GPT...','green')) as status:
      # Retrieve the response from the API
      # cprint(character['name'] + ': ', 'white', end='')
      
      current_msg = ""
      for chunk in openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=initial_msgs,
        temperature=character['temperature'],
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
    print(colored('\n[SYSTEM]\t', 'white') + colored("Bye", 'green'))
    exit(0)
  except Exception as e:
    # Print the exception and exit the program
    print(colored(e, 'red'))
    exit(0)

if __name__ == "__main__":
    main()