# TO-DO

## High Priority

- [ ] Fix when user typed something and deleted until the start, the prompt would disappear
- [ ] Allow press enter but not send input (opiont for `ctrl + enter`` to send)
- [ ] Allow streaming in the syntax highlightin mode (non-streaming mode)
- [ ] Allow quickly reset the current input
- [ ] Allow reads the content of a external resource and extract knowledge from that webpage
	- Options for URL, Files (PDF, TXT, CSV)
	- Option to show verbose
- [ ] Address issue regarding model's maximum context length error
  - `This model's maximum context length is 4097 tokens. However, your messages resulted in 4107 tokens. Please reduce the length of the messages.`
- [ ] Develop feature allowing users to parse and select code snippets
- [ ] Design functionality to erase (clear) all current input using `shift`
- [ ] Integrate ability to interrupt unresponsive requests (adding timeout)
- [ ] Enable users to halt overly lengthy responses
- [ ] More examples for common use cases
- [ ] Setup a `~/.config/termchat/` directory for storing character presets
- [ ] Handle exceptions for unresponsive model API and enable retries
  - Options to retry with same previous chat context

```text
Enter your message: what spaceship are we in?
That model is currently overloaded with other requests. You can retry your request, or contact us through our help center at help.openai.com if the error persists. (Please include the request ID 68e572a183a8f9b1ab105972ff859e46 in your message.) (Error occurred while streaming.)
```

- [ ] Embed capability for customizing characters in `chat.py`
  - Extract information from provided articles or episode digests
  - Compare embeddings to find the closest match in given context [Reference 1](https://promptbase.com/prompt/chat-with-a-movieseriesgames-character)
- [ ] Facilitate loading of chat history from a JSON file
- [ ] Implement response prefixes using character names
- [ ] Enable restoration of prior chat context by loading chat history from a JSON file
- [x] Implement `-q` option for immediate question and answer interaction
- [x] Incorporate feature to copy answers to clipboard
- [x] Add support for Markdown in terminal display
- [x] Allow moving cursor in the input text

## Normal Priority

- [ ] Resolve issues with Q&A in PDFs (need to consider full context)
- [ ] Develop `termchat` as a PyPI package
- [ ] Consider supporting URLs for online PDF files
- [ ] Utilize KNN over naive dot product for finding closest context match
- [ ] Streamline chatbot responses with the streaming API [reference](https://til.simonwillison.net/gpt3/python-chatgpt-streaming-api)
- [x] Implement `/exit` command to terminate program