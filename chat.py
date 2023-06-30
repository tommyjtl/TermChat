import os
import json
from datetime import datetime
from termcolor import colored
from rich.console import Console

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
      print(colored('<Press Ctrl+C to exit>', 'dark_grey'))
      user_input = input(colored('Enter your message: ', 'yellow'))
      
      # Append user input to the list of messages to the previous messages
      initial_msgs.append({"role": "user", "content": user_input})

      # Display indicator that the program is waiting for GPT-3
      with console.status(colored('Waiting for GPT...','green')) as status:
        # Retrieve the response from the API
        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=initial_msgs
        )
      
      # Append assistant response to the list of messages
      initial_msgs.append({"role": "assistant", "content": completion.choices[0].message.content})
      
      # Print the assistant response
      print(colored(completion.choices[0].message.content, 'green'))
      
      with open('history/chat_history-' + str(chat_datetime) + '.json', 'w') as f:
        f.writelines(json.dumps(initial_msgs, indent=2))
      
  except KeyboardInterrupt:
    # Exit the program if the user presses Ctrl+C
    print('\n[SYSTEM]', colored("\nBye!", 'green'))
    exit(0)
  except Exception as e:
    # Print the exception and exit the program
    print(colored(e, 'red'))
    exit(0)

if __name__ == "__main__":
    main()