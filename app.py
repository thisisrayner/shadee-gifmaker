import streamlit as st
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

if st.button("Download and Prepare Clip"):
    # Additional guardrail before downloading
    if not url:
        st.error("Please enter a YouTube URL.")
    elif end_time <= start_time or (end_time - start_time) > 30:
        st.error("Invalid clip time range.")
    else:
        try:
            with st.spinner("Fetching video..."):
                yt = YouTube(url)

                # Filter only streams matching resolution
                stream = yt.streams.filter(res=resolution, file_extension='mp4').first()
                if not stream:
                    st.error(f"No available stream at {resolution}. Try another resolution.")
                else:
                    # Download the video
                    video_file = "video.mp4"
                    stream.download(filename=video_file)
                    st.success(f"Video downloaded as {video_file}. Ready for clipping.")
        except Exception as e:
            st.error(f"Error downloading video: {e}")
