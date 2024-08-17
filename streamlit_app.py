import streamlit as st
import pandas as pd
import math
from pathlib import Path
from pydub import AudioSegment
import os
import io
import subprocess
from openai import OpenAI

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Transcripción de Audio',
    # page_icon=':pen:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

def split_audio_file(input_file, max_size_mb=20 * 1024 * 1024):
   # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Get the file extension

    ext = "mp3"
    
    # Calculate the number of chunks needed
    file_size = input_file.size
    num_chunks = math.ceil(file_size / (max_size_mb * 1024 * 1024))
    
    # Calculate the duration of each chunk
    chunk_length_ms = len(audio) // num_chunks
    files = []
    # Split and export the audio chunks
    for i in range(num_chunks):
        start_time = i * chunk_length_ms
        end_time = (i + 1) * chunk_length_ms if i < num_chunks - 1 else len(audio)
        
        chunk = audio[start_time:end_time]
        output_filename = f"{input_file.name}_part{i+1}.{ext}"
        chunk.export(output_filename, format=ext)
        files.append(output_filename)
        print(f"Exported {output_filename}")

    print(f"Audio file split into {num_chunks} parts.")
    return files


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: Transcripción de Audio

Solo tienes que poner tu [apikey de openai](https://openai.com) y luego puedes seleccionar cualquier archivo.
Creado por Arturo Rebolledo.
'''

# Add some spacing
''
''
key = st.text_input(label="Open AI ApiKey")

"## Sube Tu Archivo"

client = OpenAI(api_key=key)

audio = st.file_uploader(type="mp3", label="Archivo De Audio")

if audio:
    audio.name
    st.audio(audio)
    audio_chunks = split_audio_file(audio)

    # Saving the chunks to verify the output
    for chunk in audio_chunks:
        audio_file = open(chunk, "rb")
        audio_bytes = audio_file.read()

        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="text")
        
        st.markdown(transcript)

        os.remove(chunk)


