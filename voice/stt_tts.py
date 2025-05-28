from fastapi import APIRouter, File, UploadFile, Form
import whisper
import tempfile
import os
from gtts import gTTS

router = APIRouter()
model = whisper.load_model("base")

@router.post("/stt")
def speech_to_text(audio: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(audio.file.read())
        temp.flush()
        result = model.transcribe(temp.name)
    os.remove(temp.name)
    return {"text": result["text"]}

@router.post("/tts")
def text_to_speech(text: str = Form(...)):
    tts = gTTS(text)
    output_path = "/tmp/response.mp3"
    tts.save(output_path)
    return {"audio_file": output_path}