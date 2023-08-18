# Tech-to-Speech Module
The tech-to-speech model is a specialized module designed for use within the Telegram Bot to transform textual descriptions of artworks into speech audio files.


## Routes

### 1. Pre-Generated Audio
#### Retrieve pre-generated audio based on art index. ####

When the requested audio for the description of an image from a Telegram Bot user has been pre-generated, this route will be used. The retrieve function retrieves the audio according to the art index.

We have converted part of the art descriptions in our database to audio using Bark-small, a TTS model by Suno AI, and saved the pre-generated audio in remote storage.

### 2. On-the-Fly Audio Generation
#### Generate audio on-the-fly for descriptions not previously converted to audio. ####

When the requested audio for the description of an image from a Telegram Bot user has not been pre-generated, this route will be used.

The description will run through our on-the-fly model using pyttsx3. The generated audio will be more robotic-like than the pre-generated audio, but it can run very fast.


## How to Use
This module is intended to be used within a Telegram Bot. Here's how you can utilize it:

### 1. Pre-Generated Audio Retrieval
- Retrieve: Fetch the pre-generated audio from remote storage using the art index.
- Input: Index of the art piece
- Output: Audio file in .wav format sent to the user via the Telegram Bot.

### 2. On-the-Fly Audio Generation
- Generate: Create the audio using the on-the-fly model (pyttsx3) based on the description of the art.
- Input: Textual description of an art piece
- Output: Audio file in .wav format sent to the user via the Telegram Bot.


## Future Work
The Tech-to-Speech module is open to contributions, and there are several areas where enhancements could be made:
1. Audio Retrieval Script: A script to facilitate the retrieval of pre-generated audio from remote storage could streamline the process and enhance the user experience.
2. Model Fine-Tuning: Fine-tuning the underlying TTS models could ensure better and more consistent audio quality.
3. Support for Additional Formats: Exploring support for additional audio formats could enable a broader range of devices and platforms to access the audio files.
4. Performance Optimization: Continuous work to optimize performance, especially for on-the-fly generation, could ensure faster response times and lower resource consumption.
5. Add more languages: Adding TTS support for multiple languages could allow expansion to non-English-based arts and users.