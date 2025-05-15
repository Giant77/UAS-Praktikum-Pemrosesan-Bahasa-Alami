import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uvicorn
from g2p_id import G2P

from stt import transcribe_speech_to_text
from llm import generate_response
from tts import transcribe_text_to_speech

g2p = G2P()
app = FastAPI(title="Voice AI Assistant API")

@app.get("/")
def read_root():
    return {"message": "Voice AI Assistant API is running"}

@app.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):
    """
    Process voice chat workflow:
    1. Receive audio file from frontend
    2. Convert speech to text using Whisper
    3. Generate response using Gemini
    4. Convert response to speech
    5. Return audio file
    """
    # 1. Read uploaded file
    contents = await file.read()
    if not contents:
        return {"error": "Empty file"}
    
    # 2. Speech to text
    transcript = transcribe_speech_to_text(contents, file_ext=os.path.splitext(file.filename)[1])
    
    print(f"[INFO] Transcribed: {transcript}")
    
    # 3. Generate response from LLM
    response_text = generate_response(transcript)
    if response_text.startswith("[ERROR]"):
        return {"error": response_text}
    
    print(f"[INFO] LLM Response: {response_text}")
    
    # 4. Text to speech
    # send g2p results for 'phonetized' text
    audio_path = transcribe_text_to_speech(g2p(response_text))
    if not audio_path or audio_path.startswith("[ERROR]"):
        return {"error": f"Failed to generate speech: {audio_path}"}
    
    # 5. Return audio file
    return FileResponse(
    path=audio_path,
    media_type="audio/wav",
    filename="response.wav"
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)