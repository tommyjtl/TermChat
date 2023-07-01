import fitz
import os
from termcolor import colored
from rich.console import Console

# @TODO: 
# - Save the chat history to a JSON file like what `chat.py` does

from utils import PDF
from utils import OCR
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
parser.add_argument("-f", "--file", 
                    dest="file_path",
                    required=True,  # required argument
                    help="Specify a PDF file location.")
parser.add_argument("--ocr",
                    dest="need_ocr",
                    action="store_true",
                    default=False,
                    help="Specify whether to OCR the PDF file.")
args = parser.parse_args()

check_api_key = os.getenv("OPENAI_API_KEY")
if check_api_key is None:
  print(colored('OPENAI_API_KEY is not set as a system environment variable', 'red'))
  exit(0)
else:
  print('[SYSTEM]', colored('OPENAI_API_KEY found.', 'green'))
  print('[SYSTEM]', colored('<Press Ctrl+C to exit>', 'green'))

# Initialize the console for displaying spinner status
console = Console()

# check if file exists
if not os.path.isfile(args.file_path):
  print('[SYSTEM]', colored(f"The file path you specified does not exist: `{args.file_path}`", 'red'))
  exit(0)

# check if temp directory exists
# all generated files (extracted content, embeddings) will be stored in this directory
if not os.path.isdir("temp"):
    print("Directory does not exist.")
    os.mkdir("temp")
    
# Initialize the PDF class
pdfUtils = PDF()
    
#    ____ _               _      _____           _              _     _ _                 
#   / ___| |__   ___  ___| | __ | ____|_ __ ___ | |__   ___  __| | __| (_)_ __   __ _ ___ 
#  | |   | '_ \ / _ \/ __| |/ / |  _| | '_ ` _ \| '_ \ / _ \/ _` |/ _` | | '_ \ / _` / __|
#  | |___| | | |  __/ (__|   <  | |___| | | | | | |_) |  __/ (_| | (_| | | | | | (_| \__ \
#   \____|_| |_|\___|\___|_|\_\ |_____|_| |_| |_|_.__/ \___|\__,_|\__,_|_|_| |_|\__, |___/
#                                                                               |___/     
# check if the extracted txt file exists

directory, filename = os.path.split(args.file_path)

need_generate_embeddings = False
if not os.path.isfile("./temp/" + filename.split(".")[0] + "_extracted_embeddings.json"):
  need_generate_embeddings = True
    
#   ____  ____  _____    ___   ____ ____  
#  |  _ \|  _ \|  ___|  / _ \ / ___|  _ \ 
#  | |_) | | | | |_    | | | | |   | |_) |
#  |  __/| |_| |  _|   | |_| | |___|  _ < 
#  |_|   |____/|_|      \___/ \____|_| \_\
# (Optional)

if args.need_ocr and need_generate_embeddings is True:
  print('[SYSTEM]', colored('Starting to OCR the file.', 'green'))
  with console.status(colored('OCR-ing the PDF file...','green')) as status:
    directory, filename = os.path.split(args.file_path)
    ocr = OCR(args.file_path)
    ocr.extract()
    
    ocr_output_path = "./temp/" + filename.split(".")[0] + ".pdf"
    args.file_path = ocr_output_path

#   ____  ____  _____   _          _____         _   
#  |  _ \|  _ \|  ___| | |_ ___   |_   _|____  _| |_ 
#  | |_) | | | | |_    | __/ _ \    | |/ _ \ \/ / __|
#  |  __/| |_| |  _|   | || (_) |   | |  __/>  <| |_ 
#  |_|   |____/|_|      \__\___/    |_|\___/_/\_\\__|
                          
if need_generate_embeddings is True:
  print('[SYSTEM]', colored('Extracting text from the PDF file.', 'green'))
  # Setting up the PDF extraction
  doc = fitz.open(args.file_path)
  out = open("./temp/" + filename.split(".")[0] + "_extracted.txt", "wb") # create a text output

  for page in doc: # iterate the document pages
    text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
    out.write(text) # write text of page
    out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
    out.write('\n\n\n'.encode("utf8"))
  
  # close the writing
  out.close()
  
if need_generate_embeddings is True:
  print('[SYSTEM]', colored("Embeddings not found. Generating embeddings from extracted text.", 'green'))
  pdfUtils.generateEmbeddingsFromFile("./temp/" + filename.split(".")[0] + "_extracted.txt")
else:
  print('[SYSTEM]', colored("Embeddings found. Loading the existing embeddings.", 'green'))
  pdfUtils.loadEmbeddingsFromFile("./temp/" + filename.split(".")[0] + "_extracted_embeddings.json")
  
def main():
  try:
    while True:
      question = input(colored('Enter your question: ', 'yellow'))
      question_embeddings = pdfUtils.generateEmbeddingsFromText(question)['embeddings']
      
      generate_success = False
      while generate_success is False:
        # By reducing the length of the context tokens,
        # this loop will keep running until the GPT-3 API returns a valid response
        try:
          closestParagraphs = pdfUtils.findClosestChunks(question_embeddings)
          
          # Display indicator that the program is waiting for GPT-3
          with console.status(colored('Waiting for GPT...','green')) as status:
            # Retrieve the response from the API
            generate_success, result = pdfUtils.generateAnswers(question, closestParagraphs)

          if generate_success is True:
            print(colored(result, 'green'))
          else:
            # print(colored(result, 'red'))
            pdfUtils.minimumComparisonCount -= 1
        except Exception as e:
          pass
      
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