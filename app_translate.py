import os
import logging
from datetime import datetime
from pytube import YouTube
from moviepy.editor import *
from google.cloud import translate_v2 as translate
import whisper

# Set the path to your API key JSON file
api_key_path = 'probable-willow-320123-38305d06825d.json'

# Set the environment variable with the API key path
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key_path

# Set up logging
logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO)


def translate_text(text, target_language):
    
    # Create an instance of the Translator class
    translate_client = translate.Client()

    # Use the translate() method to translate the text
    translation = translate_client.translate(text, target_language=target_language)

    return translation['translatedText']

def download_video_with_timestamp(url, output_path):
    try:
        # Download the YouTube video
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()

        # Get the current date and time to create a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create the output file name with the timestamp
        output_filename = f"{yt.title}_{timestamp}.mp4"
        output_file_path = f"{output_path}/{output_filename}"

        # Download the video using pytube
        video.download(output_path, filename=output_filename)

        logging.info("Video downloaded successfully!")

        # Convert the downloaded video to mp3
        audio_file_path = f"{output_path}/{yt.title}_{timestamp}.mp3"
        video_clip = VideoFileClip(output_file_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_file_path)
        audio_clip.close()
        video_clip.close()

        logging.info("Video converted to mp3 successfully!")
        return audio_file_path
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return None

# Function to transcribe audio
def transcribe_audio(audio_file_path, model_path, target_language):
    # Load the whisper model
    model = whisper.load_model(model_path)

    # Transcribe audio
    result = model.transcribe(audio_file_path)

    # Translate the transcript
    translated_text = translate_text(result['text'], target_language)

    # Save the recognized text and its translation to text files
    text_file_path = os.path.splitext(audio_file_path)[0] + ".txt"
    translated_text_file_path = os.path.splitext(audio_file_path)[0] + "_translated.txt"
    
    with open(text_file_path, "w") as text_file:
        text_file.write(result['text'])
    
    with open(translated_text_file_path, "w") as translated_text_file:
        translated_text_file.write(translated_text)

    logging.info(f"Transcript saved to: {text_file_path}")

# Usage
video_url = "https://www.youtube.com/watch?v=rcEGVuwt62Q"
output_directory = "./videos"
audio_file_path = download_video_with_timestamp(video_url, output_directory)
target_language = "fr"  # Translate to French

if audio_file_path is not None:
    # Perform the transcription and translation
    transcribe_audio(audio_file_path, model_path='large', target_language=target_language)
