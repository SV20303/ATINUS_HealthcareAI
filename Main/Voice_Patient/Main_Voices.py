# Setting up the audio recording using ffmpeg and pyaudio

import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import time

def get_latest_audio(directory="recordings"):
    audio_files = glob.glob(os.path.join(directory, "*.mp3"))
    if not audio_files:
        return None
    latest_file = max(audio_files, key=os.path.getctime)
    return latest_file

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit= 20):
    """
    Records audio from the microphone and saves it as an MP3 file.

    Args:
        file_path (str): Path to save the recorded audio file.
        timeout (int): Maximum time to wait for a phrase to start (in seconds).
        phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=3)
            recognizer.energy_threshold = 400    #higher value coz of less sensitive to noises.
            logging.info("Start speaking now...")

            audio_data = recognizer.listen(source, timeout=30, phrase_time_limit=None)
            logging.info("Recording complete.")

            # Convert the recorded audio to MP3
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            logging.info(f"✅ Audio saved to {file_path}")
    except Exception as e:
        logging.error(f"❌ Error recording audio: {e}")


timestamp = time.strftime("%Y%m%d-%H%M%S")
record_audio (file_path = f"recordings/audio_{timestamp}.mp3",timeout = 5)

if __name__ == "__main__":
    print("This will only run if Main_Voices.py is run directly")

#setting up the speech to text
from dotenv import load_dotenv
import os
import glob
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
stt_model = "whisper-large-v3"

def transcribe_with_groq(stt_model, get_latest_audio_func, GROQ_API_KEY):
    if not GROQ_API_KEY:
        raise ValueError("❌ GROQ_API_KEY not found. Please check your .env file.")

    # Call the function to get the latest audio path
    audio_path = get_latest_audio_func()
    if not audio_path or not os.path.exists(audio_path):
        raise FileNotFoundError("❌ No valid audio file found.")

    client = Groq(api_key=GROQ_API_KEY)

    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )

    return response.text