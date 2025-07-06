import streamlit as st
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip
import os

st.set_page_config(page_title="YouTube to GIF Converter", layout="centered")
st.title("YouTube to GIF Converter")

st.markdown(
    """
    **Instructions:**  
    1. Paste a YouTube link  
    2. Choose start and end times (max 30 seconds apart)  
    3. Choose resolution (up to 480p)  
    4. Click the button to generate your GIF
    """
)

# Input fields
url = st.text_input("YouTube Link", help="Example: https://www.youtube.com/watch?v=...")
start_time = st.number_input("Start Time (seconds)", min_value=0, step=1, help="Clip start time in seconds")
end_time = st.number_input("End Time (seconds)", min_value=0, step=1, help="Clip end time in seconds")
resolution = st.selectbox("Resolution", ["360p", "480p"], help="Maximum allowed: 480p")

# Validate clip length
clip_length = end_time - start_time
if end_time and start_time:
    if clip_length <= 0:
        st.error("End time must be greater than start time.")
    elif clip_length > 30:
        st.error("Clip length exceeds 30 seconds limit.")

# Download and process button
if st.button("Download and Create GIF"):
    if not url:
        st.error("Please enter a YouTube URL.")
    elif clip_length <= 0 or clip_length > 30:
        st.error("Invalid clip duration. Must be >0 and ≤30 seconds.")
    else:
        try:
            with st.spinner("Downloading video from YouTube..."):
                # Define yt-dlp options
                ydl_opts = {
                    'format': f'bestvideo[height<={resolution[:-1]}]+bestaudio/best[height<={resolution[:-1]}]/best',
                    'outtmpl': 'video.mp4',
                    'quiet': True,
                    'noplaylist': True
                }

                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

            st.success("Video downloaded successfully!")

            with st.spinner("Processing clip and creating GIF..."):
                clip = VideoFileClip('video.mp4').subclip(start_time, end_time)
                clip = clip.resize(width=480 if resolution == "480p" else 360)
                clip.write_gif('output.gif', fps=10)

            st.success("GIF created successfully!")
            st.image('output.gif')
            with open('output.gif', 'rb') as f:
                st.download_button("Download GIF", f, file_name="clip.gif")

            # Clean up
            os.remove('video.mp4')
            os.remove('output.gif')

        except Exception as e:
            st.error(f"Error: {e}")
