from transformers import pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn") # 
from youtube_transcript_api import YouTubeTranscriptApi 
video_id = "H3d2yIHk8b4" # youtube video id
transcript = YouTubeTranscriptApi.get_transcript(video_id) # get the transcript
transcript_text = " ".join([entry['text'] for entry in transcript]) # get the transcript text
transcript_text
summary = summarizer(transcript_text, max_length=100, min_length=5, do_sample=False)[0]['summary_text']
print(summary)