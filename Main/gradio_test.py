#setting up the gradio app
import os
import gradio as gr
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Brain_Doctor.Doc_brain import get_image_files,analysis_with_query
from Voice_Doctor.main_voice import text_to_speech_with_gtts,text_to_speech_with_elevenlabs
from Voice_Patient.Main_Voices import transcribe_with_groq

system_prompt = """
    You are a compassionate and knowledgeable doctor speaking directly to a patient.
    I know you are not but for training and learning purposes.
    Based on the image and text input, provide your medical impression and suggest possible remedies. 
    If there are multiple possibilities (differential diagnoses), mention them naturally and offer supportive suggestions or remedies for each.
    Never include numbers, bullet points, or special characters. Do not use phrases like "the image I see" or "as an AI model" — instead, speak naturally as a real doctor would, using phrasing like "With what I see, I think you have...".
    Avoid markdown or formatting. Your response should be a single, concise paragraph with a maximum of two sentences, and must read like you're speaking to a real person. Never include any disclaimers about being an AI or a language model.
    Start directly with the diagnosis or observation without preamble."""

def process_inputs(audio_filepath, image_filepath):
    try:
        speech_to_text_output = transcribe_with_groq(
            stt_model="whisper-large-v3",
            get_latest_audio_func=lambda: audio_filepath,
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
        )

        # Step 2: Handle the image input and generate doctor's response
        if image_filepath:
            encoded_img = get_image_files(image_filepath)
            doctor_response = analysis_with_query(
                query=system_prompt + speech_to_text_output,
                encoded_image=encoded_img,
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
        else:
            doctor_response = "No image provided for me to analyze."

        # Step 3: Convert text response to speech
        voice_of_doctor = text_to_speech_with_elevenlabs(doctor_response, "final.mp3")

        # Step 4: Return results to UI
        return speech_to_text_output, doctor_response, voice_of_doctor

    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error", "Error", None


iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(type="filepath", label="Speak your query"),
        gr.Image(type="filepath", label="Upload related image")
    ],
    outputs=[
        gr.Textbox(label="Transcribed Speech"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Response Audio")
    ],
    title="ATINUS AI",
    description="An AI-powered assistant that listens, sees, and responds like a doctor. Speak your symptoms and upload related images.",
    allow_flagging="never",
    theme="default"
)

iface.launch(share=True)