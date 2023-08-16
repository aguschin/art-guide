from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
import pandas as pd

def text_to_speech(input_csv, output_wav):
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

    # Load the input text from the CSV file
    input_data = pd.read_csv(input_csv)
    texts = input_data["text"]

    # Initialize an empty list to store generated speeches
    generated_speeches = []

    for text in texts:
        inputs = processor(text=text, return_tensors="pt")

        # Load xvector containing speaker's voice characteristics from a dataset
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
        generated_speeches.append(speech.numpy())

    # Write each generated speech to a separate sound file
    for i, speech in enumerate(generated_speeches):
        output_filename = f"{output_wav}_{i}.wav"
        sf.write(output_filename, speech, samplerate=16000)

# Example usage
input_csv = "text.csv"  # Replace with your input CSV file
output_wav = "speech_output"  # Replace with the desired output file name (without extension)
text_to_speech(input_csv, output_wav)
