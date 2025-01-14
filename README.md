# TermChat

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![unstable](http://badges.github.io/stability-badges/dist/unstable.svg)](http://github.com/badges/stability-badges)

A minimal GPT chat client in the terminal. A toy experiment with OpenAI's GPT API.

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

```bash
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

<details>
  <summary> 🎬 Example usage </summary>

https://github.com/tommyjtl/termchat/assets/1622557/fb5d111b-42fb-4899-aeb6-c97202847a6f

</details>

#### Specifiy a personality

```bash
python chat.py -c <character>
```

<details>
  <summary> 🎬 Example usage </summary>

https://github.com/tommyjtl/termchat/assets/1622557/9d4ae7d7-d62b-4e28-b428-6b676d3780aa

</details>

### On-demand Terminal Q&A

```bash
python chat.py -q
```

<details>
  <summary> 🎬 Example usage </summary>

https://github.com/tommyjtl/termchat/assets/1622557/8b25b39f-3145-4ad8-886e-a39e3d165b9f

</details>

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

<details>
  <summary> 🎬 Example usage </summary>

https://github.com/tommyjtl/termchat/assets/1622557/40162508-3263-406b-bb7e-27558ae8d618

</details>

## Acknowledgments

- [QueryGPT](https://github.com/tsensei/QueryGPT)
