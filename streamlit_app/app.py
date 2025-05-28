import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import requests
import os
import tempfile

st.title("🎙️ Real-Time Finance Voice Agent")

# Define media constraints without ClientSettings
media_constraints = {"audio": True, "video": False}

# Audio Processor Class
class AudioProcessor:
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Convert to bytes and store
        self.frames.append(frame.to_ndarray().tobytes())
        return frame

# Start WebRTC
audio_ctx = st.empty()
processor = AudioProcessor()

webrtc_ctx = webrtc_streamer(
    key="speech",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=lambda: processor,
    media_stream_constraints=media_constraints,
    async_processing=True
)

# Process when button is clicked
if st.button("🔍 Transcribe and Query"):
    if processor.frames:
        # Save temporary audio file
        temp_path = tempfile.mktemp(suffix=".wav")
        with open(temp_path, "wb") as f:
            for frame in processor.frames:
                f.write(frame)

        # Transcribe
        with open(temp_path, "rb") as audio_file:
            st.info("Transcribing audio...")
            st.audio(audio_file)
            res = requests.post("http://localhost:8000/stt", files={"audio": audio_file})

        os.remove(temp_path)

        if res.ok:
            text = res.json()["text"]
            st.success("Transcription:")
            st.write(text)

            # Query backend
            st.info("Querying LLM...")
            payload = {
                "query": text,
                "context": [],
                "query_type": "market_brief"
            }
            res2 = requests.post("http://localhost:8000/answer", json=payload)
            if res2.ok:
                answer = res2.json()["answer"]
                st.success("Answer:")
                st.write(answer)

                # Get TTS audio file
                tts_res = requests.post("http://localhost:8000/tts", data={"text": answer})
                if tts_res.ok:
                    audio_file = tts_res.json()["audio_file"]
                    st.audio(audio_file, format='audio/mp3')
                else:
                    st.error("TTS failed.")
            else:
                st.error("LLM answer generation failed.")
        else:
            st.error("Speech-to-text transcription failed.")
    else:
        st.warning("No audio input received.")
