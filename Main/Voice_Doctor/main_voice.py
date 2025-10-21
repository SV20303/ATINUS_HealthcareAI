import os
import platform
import subprocess
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs

from dotenv import load_dotenv
import os

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# GTTS TTS Function
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

# ElevenLabs TTS Function
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",  # Replace with your actual voice ID or name
        output_format="mp3_22050_32",
        model="eleven_multilingual_v2"
    )
    elevenlabs.save(audio, output_filepath)

# Cross-platform audio player
def play_audio(output_filepath):
    try:
        os_name = platform.system()
        if os_name == "Darwin":
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-C', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# --- RUNNING THE CODE ---

input_text = "Hey, this is Atinus, how can I help you today?"

# Create folder if not exists
os.makedirs("Drecordings", exist_ok=True)

# Uncomment the one you want to test

# === GTTS ===
# gtts_path = "recordings/gtts_audio.mp3"
# text_to_speech_with_gtts(input_text, gtts_path)
# play_audio(gtts_path)

# === ElevenLabs ===
elevenlabs_path = "Drecordings/11_audio.mp3"
text_to_speech_with_elevenlabs(input_text, elevenlabs_path)
play_audio(elevenlabs_path)

if __name__ == "__main__":
    print("This will only run if main_voice.py is run directly")