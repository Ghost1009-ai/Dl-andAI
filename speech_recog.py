import streamlit as st
import requests
import sounddevice as sd
import numpy as np
import wave
import tempfile
import io

# Define API URL and headers
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
headers = {"Authorization": "Bearer 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"}

# Function to send audio to Hugging Face API
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

# Function to record audio using the microphone
def record_audio(duration=10, fs=16000):
    st.write("Recording... Please speak into your microphone.")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    st.write("Recording complete.")
    
    # Save the audio to a temporary WAV file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    with wave.open(temp_file, 'wb') as wf:
        wf.setnchannels(1)  # Mono audio
        wf.setsampwidth(2)  # 16-bit samples
        wf.setframerate(fs)
        wf.writeframes(audio_data.tobytes())
    
    return temp_file.name

# Streamlit UI setup
st.title("Automatic Speech Recognition")

st.write("Press the button below to start recording your voice or upload an audio file:")

# Option to upload audio file from local system
uploaded_file = st.file_uploader("Browse for file", type=["wav", "mp3", "flac"])

if uploaded_file is not None:
    # If a file is uploaded, save it temporarily
    temp_uploaded_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    # Process the uploaded file
    st.write(f"Uploaded file: {uploaded_file.name}")
    st.audio(uploaded_file, format="audio/wav")  # Display the uploaded audio
    result = query(temp_uploaded_file.name)
    
    # Display transcription
    if 'text' in result:
        st.subheader("Transcription:")
        st.write(result['text'])
    else:
        st.write("Sorry, the transcription failed. Please try again.")

elif st.button("Record from browser"):
    # If the user chooses to record audio, call the record_audio function
    audio_file = record_audio()

    # Display recorded audio and send it for transcription
    with open(audio_file, 'rb') as f:
        st.audio(f.read(), format='audio/wav')  # Play the recorded audio
    st.write("Sending the audio to Whisper API for transcription...")
    result = query(audio_file)

    # Display the transcribed text
    if 'text' in result:
        st.subheader("Transcription:")
        st.write(result['text'])
    else:
        st.write("Sorry, the transcription failed. Please try again.")