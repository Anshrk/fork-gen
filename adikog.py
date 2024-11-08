from moviepy.editor import *
from moviepy.video.tools.drawing import color_gradient
from PIL import ImageFont, ImageDraw, Image

def generate_video_template(title, description, output_file="video_template.mp4"):
    # Settings
    duration = 10  # Duration in seconds
    video_size = (1280, 720)  # Resolution
    bg_color = (30, 30, 30)  # Background color (dark gray)
    text_color = 'white'  # Text color
    font_path = "arial.ttf"  # Path to font file; adjust as needed

    # Generate Background Clip
    def make_background_clip(size, color):
        return ColorClip(size, color=color, duration=duration)

    # Create text images for title and description
    def make_text_image(text, size, font_size):
        font = ImageFont.truetype(font_path, font_size)
        image = Image.new('RGB', size, bg_color)
        draw = ImageDraw.Draw(image)
        w, h = draw.textsize(text, font=font)
        position = ((size[0] - w) // 2, (size[1] - h) // 2)
        draw.text(position, text, fill=text_color, font=font)
        return ImageClip(image).set_duration(duration)

    # Create title and description clips
    title_clip = make_text_image(title, video_size, font_size=70).set_position(("center", "top")).set_start(1)
    description_clip = make_text_image(description, video_size, font_size=40).set_position(("center", "center")).set_start(3)

    # Background and overlay clips
    background_clip = make_background_clip(video_size, bg_color)
    video = CompositeVideoClip([background_clip, title_clip, description_clip])

    # Write the final video file
    video.write_videofile(output_file, fps=24)

# Usage
generate_video_template("Sample Title", "This is a sample description for the video template.")
