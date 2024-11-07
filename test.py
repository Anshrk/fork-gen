import os
import subprocess

def extract_keyframes_ffmpeg(video_path, output_dir, threshold=0.3):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # FFmpeg command to extract key frames with scene detection
    ffmpeg_cmd = [
        'ffmpeg', 
        '-i', video_path,
        '-vf', f"select='gt(scene,{threshold})'",
        '-vsync', 'vfr',
        os.path.join(output_dir, 'keyframe_%04d.jpg')
    ]
    
    # Run the FFmpeg command
    subprocess.run(ffmpeg_cmd)
    print(f"Keyframes saved in {output_dir}")

# Usage
video_path = 'videos/output.mp4'  # Path to your input video file
output_dir = 'keyframes_output'  # Directory where keyframes will be saved
threshold = 0.3  # Adjust the threshold for scene changes (0.3 is a good starting point)

extract_keyframes_ffmpeg(video_path, output_dir, threshold)
