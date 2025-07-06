import streamlit as st

st.title("YouTube to GIF Converter")

st.markdown(
    """
    **Instructions:**  
    - Paste a YouTube link  
    - Choose start and end times (max 30 seconds apart)  
    - Choose resolution (up to 480p)  
    """
)

# User inputs
url = st.text_input("YouTube Link", help="Example: https://www.youtube.com/watch?v=...")
start_time = st.number_input("Start Time (seconds)", min_value=0, step=1, help="Clip start time in seconds")
end_time = st.number_input("End Time (seconds)", min_value=0, step=1, help="Clip end time in seconds")
resolution = st.selectbox("Resolution", ["360p", "480p"], help="Max allowed: 480p")

# Guardrail check: ensure start < end and ≤30 seconds
if end_time and start_time:
    clip_length = end_time - start_time
    if clip_length <= 0:
        st.error("End time must be greater than start time.")
    elif clip_length > 30:
        st.error("Clip length exceeds 30 seconds limit.")
