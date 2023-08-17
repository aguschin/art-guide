# Tech-to-Speech Module
The tech-to-speech model is designed to transform textual descriptions of artworks into speech audio files. It offers a unique way to experience art by listening to an audio description of the piece.

...

## Expected Inputs and Outputs

- Input: Textual description of an art piece
- Output: Audio file in .wav format

...

## Routes

There are two main routes in this module:

### 1. Pre-Generated Descriptions

When the requested description of an image from a Telegram Bot user has been pre-generated, this route will be used. The retrieve function retrieves the audio according to the art index.

- How It Works: We have converted part of the art descriptions in our database to audio using Bark-small, a TTS model by Suno, and saved them in remote storage.

### 2. On-the-Fly Generation

When the requested description of an image from a Telegram Bot user has not been pre-generated before, but the description of the art can be found in our database, this route will be used.

- How It Works: The description will run through our on-the-fly model using pyttsx3. The generated audio will be more robotic-like than the first route, but it can run very fast.
