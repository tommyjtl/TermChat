import openai
import json
import time
import os
import subprocess
import shutil
import ocrmypdf

from termcolor import colored, cprint
from rich.console import Console
from rich import print as rprint
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WHITE = '\33[97m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Chat:
  character = {
    "name": "Default Assistant",
    "system": "You are a helpful assistant.",
    "temperature": 0,
  }
  
  character_presets = {
    'hal9000': 'characters/hal9000.json'
  }
  
  def __init__(self):
  
  def checkCharacterLoad(self, character_file):
    if character_file in self.character_presets:
      character_file = self.character_presets[character_file]
    
    # check if the character profile exists
    if not os.path.isfile(character_file) or not os.path.isfile(character_file.replace('.json', '.txt')):
      error_msg = [
        f"The preset file path you specified does not exist: `{character_file}`"
      ]
      rprint(
        Panel('\n'.join(error_msg),
          title="TermChat",
          border_style="red bold",
          style="red",
      ))
      exit(0)
    
    # load the character profile
    with open(character_file) as f:
      character_profile = json.load(f)
      self.character['name'] = character_profile['name']
      self.character['temperature'] = character_profile['temperature']
      
    # load the character's prompt
    with open(character_file.replace('.json', '.txt')) as f:
      self.character['system'] = ''.join(f.read())
        
  def getInitialMessage(self):
    return [{"role": "system", "content": self.character['system']}]
  
  def welcome(self):
    # Checking OPENAI_API_KEY
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
      error_msg = [
        "OPENAI_API_KEY is not set as a system environment variable"
      ]
      rprint(
        Panel('\n'.join(error_msg),
          title="TermChat",
          border_style="red bold",
          style="red",
          # subtitle="Thank you"
      ))
      exit(0)
    
    welcome_msg = [
      f"[SYSTEM] {self.character['name']} is ready to chat.",
      "[SYSTEM] Chat dialogue will be saved to `history/`",
      "[SYSTEM] <Press Ctrl+C to exit>"
    ]
    rprint(
      Panel('\n'.join(welcome_msg),
        title="TermChat",
        border_style="white bold",
        style="white",
        # subtitle="Thank you"
    ))

    if not os.path.isdir("history"):
        print("Directory does not exist.")
        os.mkdir("history")
    
  def showGoodbyeMessage(self):
    goodbye_msg = [
      "Bye",
    ]
    print()
    rprint(
      Panel('\n'.join(goodbye_msg),
        title="TermChat",
        border_style="red bold",
        style="red",
    ))

class OCR:
  commands = {
    "pdf2jpg": "",
    "jpg2pdf": ""
  }
  
  def __init__(self, source_path, ocr_lang):
    self.source_path = source_path
    self.directory, self.filename = os.path.split(source_path)
    self.ocr_output_path = "./temp/" + self.filename.split(".")[0] + ".pdf"
    self.ocr_lang = ocr_lang
    
    self.commands['pdf2jpg'] = "pdftoppm -jpeg " + source_path + " temp/" + self.filename.split(".")[0] + "/"
    self.commands['jpg2pdf'] = "convert temp/" + self.filename.split(".")[0] + "/*.jpg temp/" + self.filename.split(".")[0] + "_tmp.pdf"
    
    generate_dir = "temp/" + self.filename.split(".")[0] + "/"
    if os.path.exists(generate_dir):
        # print(f"The directory '{generate_dir}' exists, removing previous work.")
        shutil.rmtree(generate_dir)
        os.mkdir(generate_dir)
    else:
        # print(f"The directory '{generate_dir}' does not exist, creating the directory.")
        os.mkdir(generate_dir)
  
  def extract(self):
    try:
      # print(self.commands["pdf2jpg"])
      stdout, stderr = self.exec(self.commands["pdf2jpg"])
      # print("stdout: \n", stdout)
      # print("stderr: \n", stderr)

      # print(self.commands["jpg2pdf"])
      stdout, stderr = self.exec(self.commands["jpg2pdf"])
      # print("stdout: \n", stdout)
      # print("stderr: \n", stderr)

      ocrmypdf.configure_logging(-1) # comment out to enable logging
      ocrmypdf.ocr("./temp/" + self.filename.split(".")[0] + "_tmp.pdf", 
                   "./temp/" + self.filename.split(".")[0] + ".pdf",
                   output_type="pdf",
                   language=self.ocr_lang
                   #  force_ocr=True
      )
      
      shutil.rmtree("temp/" + self.filename.split(".")[0] + "/")
      os.remove("temp/" + self.filename.split(".")[0] + "_tmp.pdf")
      
    except KeyboardInterrupt:
      print("KeyboardInterrupt")
      exit(0)
    except Exception as e:
      print(colored(e, 'red'))
      exit(0)
  
  def exec(self, command):
    # Execute the command and capture the output
    process = subprocess.Popen(command, 
                                shell=True, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)
    
    stdout = ''
    stderr = ''
    
    try:
      # Continuously read the output
      while True:
          # Read the output
        output = process.stdout.readline()
        # errorp = process.stderr.readline()
        
        # Check if the output is empty and the process has finished
        if process.poll() is not None:
          break
        
        # Append the output to stdout
        if output:
          # print(output.strip())
          stdout += output.strip() + '\n'
          # stderr += errorp.strip() + '\n'
    except KeyboardInterrupt:
      print("KeyboardInterrupt")
      process.terminate()
    
    # Capture the remaining output and error (if any)
    stdout_remainder, stderr_remainder = process.communicate()
    stdout += stdout_remainder
    stderr += stderr_remainder
    
    return stdout, stderr

class PDF:
  embeddingStore = {
    'embeddings': [],
  }
  minimumComparisonCount = 5

  def generateEmbeddingsFromFile(self, file_path):
    
    with open(file_path, "r", encoding="utf-8") as file:
      rawText = file.read()    
    
    paras = []
    rawParas = rawText.split("\n\n")
    
    for rawPara in rawParas:
      rawPara = rawPara.strip().replace("\n", " ").replace("\r", "")
      if rawPara and rawPara[-1] != "?" and len(rawPara.split()) >= self.minimumComparisonCount:
        paras.append(rawPara)

    countParas = len(paras)
    
    # get current timestamp
    current_timestamp = int(time.time())
    
    response = openai.Embedding.create(
      input=paras,
      model="text-embedding-ada-002"
    )
    
    # Check if data received correctly
    if len(response["data"]) >= countParas:
      for i in range(countParas):
        # Adding each embedded para to embeddingStore
        self.embeddingStore['embeddings'].append({
          "raw": paras[i],
          "embedding": response["data"][i]["embedding"],
          "created": current_timestamp
        })
    
    export_file_name = "./temp/" + file_path.split("/")[-1].split(".")[0] + "_embeddings.json"
    
    with open(export_file_name, "w") as file:
      json.dump(self.embeddingStore, file, indent=2)

    '''
    {
      "embeddings": [
        {
          "raw": "..."
          "embedding": [0.1, 0.2, ...]
          "created": 1234567890
        },
        ...
      ]
    }
    '''

  def loadEmbeddingsFromFile(self, file_path):
    with open(file_path, 'r') as f:
      embeddings = json.load(f)
    
    self.embeddingStore = embeddings
    # print(json.dumps(self.embeddingStore, indent=2))
      
  def generateEmbeddingsFromText(self, text: str):
    response = openai.Embedding.create(
      input=text,
      model="text-embedding-ada-002"
    )
    
    if response['data'][0]['embedding'] is None:
      print("Error: Embeddings not generated for `" + text + "`")
      return None
    
    # get current timestamp
    current_timestamp = int(time.time())
    
    embeddings = {
      "raw": text,
      "embeddings": response['data'][0]['embedding'],
      "created": current_timestamp
    }
    
    # print(f"# of prompt tokens: {response['usage']['prompt_tokens']}")
    # print(f"# of total tokens: {response['usage']['total_tokens']}")
    
    return embeddings

  def createPrompt(self, question, paragraph):
    # Prompt taken from https://github.com/tsensei/QueryGPT
    return (
        "Answer the following question, also use your own knowledge when necessary:\n\n"
        "Context:\n"
        + "\n\n".join(paragraph)
        + "\n\nQuestion:\n"
        + question
        + "?"
        + "\n\nAnswer:"
    )
    
  def compareEmbeddings(self, embedding1, embedding2):
    # naive comparing of embeddings from https://github.com/tsensei/QueryGPT
    # @TODO: 
    # - use KNN
    
    length = min(len(embedding1), len(embedding2))
    dotprod = 0

    for i in range(length):
        dotprod += embedding1[i] * embedding2[i]

    return dotprod

  def findClosestChunks(self, questionEmbedding):
    items = []

    for embedding in self.embeddingStore['embeddings']:
      paragraph = embedding['raw']

      currentEmbedding = embedding['embedding']

      items.append({
          'paragraph': paragraph,
          'score': self.compareEmbeddings(questionEmbedding, currentEmbedding),
      })

    items.sort(key=lambda x: x['score'], reverse=True)
    return [item['paragraph'] for item in items[:self.minimumComparisonCount]]

  def generateAnswers(self, prompt, closestParagraphs):
    try:
      completion = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=[
          {
            "role": "user",
            "content": self.createPrompt(prompt, closestParagraphs),
          },
        ],
        # max_tokens=2000,
        temperature=0
      )

      if (len(completion['choices']) == 0):
        print('No answers generated.')
        return None
      
      return True, completion['choices'][0]['message']['content']
    
    except Exception as e:
      # print(colored(e, 'red'))
      return False, e
    
def clearTerminal():
  # Clear command for Windows
  if os.name == 'nt':
    _ = os.system('cls')
  # Clear command for Unix-like systems (Linux, macOS)
  else:
    _ = os.system('clear')
    
