# Tech-to-Speech Module
The tech-to-speech model is a specialized module designed for use within the Telegram Bot to transform textual descriptions of artworks into speech audio files.


## Expected Inputs and Outputs

- Input: Textual description of an art piece
- Output: Audio file in .wav format


## Routes

### 1. Pre-Generated Audio
**Retrieve pre-generated audio based on art index.**

When the requested audio for the description of an image from a Telegram Bot user has been pre-generated, this route will be used. The retrieve function retrieves the audio according to the art index.

We have converted part of the art descriptions in our database to audio using Bark-small, a TTS model by Suno, and saved the pre-generated audio in remote storage.

### 2. On-the-Fly Audio Generation
**Generate audio on-the-fly for descriptions not previously converted to audio.**

When the requested audio for the description of an image from a Telegram Bot user has not been pre-generated, this route will be used.

The description will run through our on-the-fly model using pyttsx3. The generated audio will be more robotic-like than the pre-generated audio, but it can run very fast.


## How to Use
This module is intended to be used within a Telegram Bot. Here's how you can utilize it:

### 1. Pre-Generated Audio Retrieval
Request: Send a request with the art index.
Retrieve: The module will fetch the pre-generated audio from remote storage according to the index.
Send: The audio file will be sent to the user via the Telegram Bot.

### 2. On-the-Fly Audio Generation
Request: Send a request with the description of the art.
Generate: The module will create the audio using the on-the-fly model (pyttsx3) according to the description text.
Send: The generated audio file will be sent to the user via the Telegram Bot.
