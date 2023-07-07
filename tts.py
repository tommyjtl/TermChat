# import pyttsx3
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# for voice in voices:
#   if "en-US" in voice.id:
#     engine.setProperty('voice', voice.id)
#     rate = engine.getProperty('rate')
#     engine.setProperty('rate', rate-50)
#     print(voice.id)
#     engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()

# ---------

# from gtts import gTTS
# tts = gTTS(text='Good morning', lang='en')
# tts.save("answer.mp3")

# ---------

from TTS.api import TTS
tts = TTS("tts_models/en/multi-dataset/tortoise-v2")

# cloning `lj` voice from `TTS/tts/utils/assets/tortoise/voices/lj`
# with custom inference settings overriding defaults.
tts.tts_to_file(text="Hello, my name is Manmay , how are you?",
                file_path="output.wav",
                voice_dir="path/to/tortoise/voices/dir/",
                speaker="lj",
                num_autoregressive_samples=1,
                diffusion_iterations=10)

# Using presets with the same voice
tts.tts_to_file(text="Hello, my name is Manmay , how are you?",
                file_path="output.wav",
                voice_dir="path/to/tortoise/voices/dir/",
                speaker="lj",
                preset="ultra_fast")

# Random voice generation
tts.tts_to_file(text="Hello, my name is Manmay , how are you?",
                file_path="output.wav")