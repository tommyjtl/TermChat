# TermChat

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Lightweight GPT chat client in the terminal. A toy experiment with OpenAI's GPT API.

> All code have only tested on macOS, not guaranteed to work on other platforms.

## Prerequisites

```bash
export OPENAI_API_KEY=<your key>
```

```bash
python -m termchat-venv
source termchat-venv/bin/activate
pip install -r requirements.txt
```

```bash
# Optional, for PDF OCR if you want multi-language support
# Read more here: https://github.com/ocrmypdf/OCRmyPDF#languages
brew install tesseract-lang
```

## Running

```shell
Usage: python script.py [OPTIONS]

Options:
  -c, --load-character FILE     Specify a character file location.
  --stream                      Enable streaming mode.
  -e, --load-engine TYPE        Specify an engine type, default is `gpt-3.5-turbo`.
  --tts                         Enable text-to-speech.
  -q, --question                Ask a question to the chatbot and get an answer directly.
  --help                        Show this message and exit.
```

### Chat with GPT

#### Default Assistant

```bash
python chat.py
```

<video controls>
  <source src="./docs/chat1.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Specifiy a personality

```bash
python chat.py -c <character>
```

<video controls>
  <source src="./docs/chat2.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Chat with PDF

```bash
# Normal usage
python pdf.py -f <file>

# Add --ocr if your PDF doesn't have text layer, default OCR language is English
python pdf.py -f <file> --ocr

# Add --ocr-lang to specify OCR language
# For <lang>, use 3-digit ISO 639-2 Code, see more here: https://github.com/tesseract-ocr/tessdata
python pdf.py -f <file> --ocr --ocr-lang <lang>
```

[![asciicast](https://asciinema.org/a/8EdULKTLvgi1nFlYRmS7zMl5U.svg)](https://asciinema.org/a/8EdULKTLvgi1nFlYRmS7zMl5U)

## Acknowledgments

- [QueryGPT](https://github.com/tsensei/QueryGPT)
