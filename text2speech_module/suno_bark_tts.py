import transformers import BarkModel
from transformers import AutoProcessor
import torch
import scipy
import numpy as np

model = BarkModel.from_pretrained("suno/bark-small")
processor = AutoProcessor.from_pretrained("suno/bark-small")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = model.to(device)


# Function to split the text into chunks
def split_text(text, chunk_size=100):
    # Split by spaces to keep words intact
    words = text.split(' ')
    chunks = []
    current_chunk = ''
    for word in words:
        # If adding the next word exceeds the chunk size, save the current chunk
        if len(current_chunk) + len(word) > chunk_size:
            chunks.append(current_chunk)
            current_chunk = word
        else:
            current_chunk += ' ' + word
    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def suno_bark_tts(text_prompt: str, index: int):
    # Split the text into chunks
    text_chunks = split_text(text_prompt)

    # ['pt', 'tf', 'np', 'jax']
    voice_preset = "pt"

    # List to store the audio outputs for each chunk
    audio_chunks = []

    # Process each chunk separately
    for chunk in text_chunks:
        inputs = processor(chunk, voice_preset=voice_preset)
        speech_output = model.generate(**inputs.to(device))
        audio_chunks.append(speech_output[0].cpu().numpy())

    # Concatenate the audio chunks
    final_audio = np.concatenate(audio_chunks)

    # Create the filename, combining the folder path and the index
    filename = f"{index}.wav"

    # Save the concatenated audio to the file in the specified Google Drive folder
    sampling_rate = model.generation_config.sample_rate
    scipy.io.wavfile.write(filename, rate=sampling_rate, data=final_audio)
    return f"Audio file '{filename}' generated successfully."