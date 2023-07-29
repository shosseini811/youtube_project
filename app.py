from pytube import YouTube
from datetime import datetime

def download_video_with_timestamp(url, output_path):
    try:
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
    except Exception as e:
        print("Error:", str(e))

# Usage
video_url = "https://www.youtube.com/watch?v=dmskVaSwEnM"
output_directory = "./youtube_project/videos"
download_video_with_timestamp(video_url, output_directory)
