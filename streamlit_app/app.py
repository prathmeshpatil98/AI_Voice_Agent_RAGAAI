import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import requests
import os
import tempfile
import time
from datetime import datetime

st.title("🎙️ Real Time Finance Voice Agent")

# --- Sidebar ---
st.sidebar.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png", width=80)
st.sidebar.title("RagaAI Voice Agent")
st.sidebar.markdown("""
**Instructions:**
- Click the microphone to start speaking your query.
- Wait for the agent to transcribe and answer.
- Listen to the spoken response or read the answer below.
""")

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

# --- Session State for Conversation History ---
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# --- Enhanced Header with Gradient and Logo ---
st.markdown('''
<style>
.header-gradient {
    background: linear-gradient(90deg, #2e86de 0%, #48c6ef 100%);
    padding: 2.5em 1em 1.5em 1em;
    border-radius: 18px;
    margin-bottom: 1.5em;
    box-shadow: 0 4px 24px rgba(44, 62, 80, 0.13);
    color: #fff;
    text-align: center;
}
.agent-avatar {
    width: 56px; height: 56px; border-radius: 50%; border: 3px solid #2e86de; margin-right: 1em; box-shadow: 0 2px 8px #2e86de33;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 #2e86de44; }
    70% { box-shadow: 0 0 0 10px #2e86de11; }
    100% { box-shadow: 0 0 0 0 #2e86de44; }
}
.fab-mic {
    position: fixed; bottom: 40px; right: 40px; z-index: 9999;
    background: #2e86de; color: #fff; border-radius: 50%; width: 70px; height: 70px;
    display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 24px #2e86de44;
    cursor: pointer; transition: background 0.2s;
}
.fab-mic:hover { background: #48c6ef; }
.chat-scroll { max-height: 420px; overflow-y: auto; margin-bottom: 1em; }
.timestamp { font-size: 0.8em; color: #888; margin-top: 0.2em; }
</style>
''', unsafe_allow_html=True)
st.markdown('''<div class="header-gradient">
    <img src="https://img.icons8.com/color/96/000000/artificial-intelligence.png" style="width:60px;vertical-align:middle;">
    <span style="font-size:2.2rem;font-weight:700;margin-left:0.5em;vertical-align:middle;">RagaAI Voice Agent</span>
    <div style="font-size:1.1rem;font-weight:400;margin-top:0.5em;">Your real-time finance assistant. Ask anything by voice!</div>
</div>''', unsafe_allow_html=True)

# --- Floating Microphone Button ---
st.markdown('''<div class="fab-mic" onclick="window.scrollTo(0,document.body.scrollHeight);">
    <img src="https://img.icons8.com/fluency/96/microphone.png" width="38"/>
</div>''', unsafe_allow_html=True)

# --- Chat History Display ---
st.markdown('<div class="chat-scroll">', unsafe_allow_html=True)
for msg in st.session_state['chat_history']:
    if msg['role'] == 'user':
        st.markdown(f'''<div class="user-bubble" style="display:flex;align-items:center;justify-content:flex-end;">
            <span style="margin-right:0.7em;"></span>
            <div>
                <div>{msg['content']}</div>
                <div class="timestamp">{msg['time']}</div>
            </div>
            <img src="https://img.icons8.com/fluency/48/user-male-circle.png" style="width:38px;border-radius:50%;margin-left:0.7em;"/>
        </div>''', unsafe_allow_html=True)
    else:
        st.markdown(f'''<div class="agent-bubble" style="display:flex;align-items:center;">
            <img src="https://img.icons8.com/color/48/robot-2.png" class="agent-avatar"/>
            <div>
                <div>{msg['content']}</div>
                <div class="timestamp">{msg['time']}</div>
            </div>
        </div>''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Main Steps ---
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Step 1: Record your question")
audio_ctx = st.empty()
processor = AudioProcessor()
webrtc_ctx = webrtc_streamer(
    key="speech",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=lambda: processor,
    media_stream_constraints=media_constraints,
    async_processing=True
)

st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Step 2: Get your answer")

# --- Advanced Button with Spinner ---
if st.button("🔍 Transcribe and Query", use_container_width=True):
    if processor.frames:
        with st.spinner('Transcribing your audio...'):
            temp_path = tempfile.mktemp(suffix=".wav")
            with open(temp_path, "wb") as f:
                for frame in processor.frames:
                    f.write(frame)
            with open(temp_path, "rb") as audio_file:
                st.audio(audio_file)
                res = requests.post("http://localhost:8000/stt", files={"audio": audio_file})
            os.remove(temp_path)
        if res.ok:
            text = res.json()["text"]
            st.session_state['chat_history'].append({
                'role': 'user',
                'content': text,
                'time': datetime.now().strftime('%H:%M')
            })
            st.success("Transcription complete!")
            st.experimental_rerun()
            # Query backend
            with st.spinner('Querying the LLM agent...'):
                payload = {
                    "query": text,
                    "context": [],
                    "query_type": "market_brief"
                }
                res2 = requests.post("http://localhost:8000/answer", json=payload)
            if res2.ok:
                answer = res2.json()["answer"]
                st.session_state['chat_history'].append({
                    'role': 'agent',
                    'content': answer,
                    'time': datetime.now().strftime('%H:%M')
                })
                st.success("Agent has responded!")
                st.experimental_rerun()
                # Get TTS audio file
                with st.spinner('Synthesizing voice response...'):
                    tts_res = requests.post("http://localhost:8000/tts", data={"text": answer})
                if tts_res.ok:
                    audio_file = tts_res.json()["audio_file"]
                    st.audio(audio_file, format='audio/mp3')
                    st.caption("🔊 Listen to the agent's answer above.")
                else:
                    st.error("TTS failed.")
            else:
                st.error("LLM answer generation failed.")
        else:
            st.error("Speech-to-text transcription failed.")
    else:
        st.warning("No audio input received.")

# --- Footer ---
st.markdown("""
---
<div style='text-align:center; color:#888;'>
    <small>Powered by <b>RagaAI</b> | <a href='https://github.com/your-repo' target='_blank'>GitHub</a></small>
</div>
""", unsafe_allow_html=True)
