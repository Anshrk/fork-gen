import whisper
import subprocess
import os

def convert_video_to_audio(video_path, audio_path="audio.wav"):
    # Extract audio from the video
    subprocess.run(['ffmpeg', '-i', video_path, '-ac', '1', '-ar', '16000', audio_path, '-y'])
    return audio_path

def transcribe_audio_with_whisper(audio_path, model_name="base"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result

# Main function to get transcript and timestamps
def get_video_transcript_and_key_moments_whisper(video_path):
    audio_path = convert_video_to_audio(video_path)
    
    # Transcribe audio using Whisper
    result = transcribe_audio_with_whisper(audio_path)
    
    # Display the transcription with timestamps
    print("Transcript with Key Timestamps:")
    for segment in result["segments"]:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        print(f"{text} - Start: {start_time}s, End: {end_time}s")
    
    # Cleanup
    os.remove(audio_path)
    return result

# Usage
video_path = "videos/output.mp4"
transcription_result = get_video_transcript_and_key_moments_whisper(video_path)
