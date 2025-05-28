from fastapi import APIRouter, UploadFile, File
import whisper
import pyttsx3
import tempfile

router = APIRouter()
stt_model = whisper.load_model("base")

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        tmp.write(await file.read())
        tmp.flush()
        result = stt_model.transcribe(tmp.name)
    return {"text": result["text"]}

@router.post("/speak")
def speak_text(text: str):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    return {"status": "spoken"}
