import time

text = "Besides, functions are easier to extend. Adding a new feature to a function is as easy as adding another keyword argument, whereas changing the language to support that new feature is much more cumbersome. Think of stream redirection or buffer flushing, for example."

for c in text.split(" "):
  print(c, end="", flush=True)
  time.sleep(0.2)