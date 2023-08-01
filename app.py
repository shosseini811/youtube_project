from pytube import YouTube
from datetime import datetime
from moviepy.editor import *
import whisper
import os

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

        print("Video downloaded successfully!")

        # Convert the downloaded video to mp3
        audio_file_path = f"{output_path}/{yt.title}_{timestamp}.mp3"
        video_clip = VideoFileClip(output_file_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_file_path)
        audio_clip.close()
        video_clip.close()

        print("Video converted to mp3 successfully!")
        return audio_file_path
    except Exception as e:
        print("Error:", str(e))
        return None

def transcribe_audio(audio_file_path, model_path):

    import whisper

    # Load the Whisper model
    # model = torch.load("./large-v2.pt")

    model = whisper.load_model(model_path)

    # Transcribe audio
    result = model.transcribe(audio_file_path)

    # Save the recognized text to a text file
    text_file_path = os.path.splitext(audio_file_path)[0] + ".txt"
    with open(text_file_path, "w") as text_file:
        text_file.write(result['text'])

    print(f"Transcript saved to: {text_file_path}")

# Usage
video_url = "https://www.youtube.com/watch?v=rcEGVuwt62Q"
output_directory = "./videos"
audio_file_path = download_video_with_timestamp(video_url, output_directory)

if audio_file_path is not None:
    transcribe_audio(audio_file_path, "tiny.en")