# TermChat

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Chatting with GPT in the terminal. Just a toy experiment with OpenAI's GPT API.

> All code have only tested on macOS, not guaranteed to work on other platforms.

## Prerequisites

```bash
export OPENAI_API_KEY=<your key>
```

```bash
pip install -r requirements.txt
```

```bash
# Optional, for PDF OCR if you want multi-language support
# Read more here: https://github.com/ocrmypdf/OCRmyPDF#languages
brew install tesseract-lang
```

## Running

```bash
python chat.py
```

[![asciicast](https://asciinema.org/a/Ewv7HoFCBc1s2RrulEQ2ou3SC.svg)](https://asciinema.org/a/Ewv7HoFCBc1s2RrulEQ2ou3SC)


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
