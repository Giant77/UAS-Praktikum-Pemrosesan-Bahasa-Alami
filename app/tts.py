import os 
import uuid 
import tempfile 
import subprocess 
 
#  Define Variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
 
# path ke folder utilitas TTS 
COQUI_DIR = os.path.join(BASE_DIR, "coqui_utils") 
 
# File model paths for Coqui TTS
COQUI_MODEL_PATH = os.path.join(COQUI_DIR, "checkpoint_1260000-inference.pth")
 
# Config path for Coqui TTS
COQUI_CONFIG_PATH = os.path.join(COQUI_DIR, "config.json")
 
# Speaker name for Coqui TTS
COQUI_SPEAKER = "wibowo"

def transcribe_text_to_speech(text: str) -> str:
    """
    Fungsi untuk mengonversi teks menjadi suara menggunakan TTS engine yang ditentukan.
    Args:
        text (str): Teks yang akan diubah menjadi suara.
    Returns:
        str: Path ke file audio hasil konversi.
    """
    path = _tts_with_coqui(text)
    return path

# === ENGINE 1: Coqui TTS ===
def _tts_with_coqui(text: str) -> str:
    tmp_dir = tempfile.gettempdir()
    output_path = os.path.join(tmp_dir, f"tts_{uuid.uuid4()}.wav")

    # jalankan Coqui TTS dengan subprocess
    cmd = [
        "tts",
        "--text", text,
        "--model_path", COQUI_MODEL_PATH,
        "--config_path", COQUI_CONFIG_PATH,
        "--speaker_idx", COQUI_SPEAKER,
        "--out_path", output_path
    ]
    
    try:
        # Run the subprocess
        subprocess.run(cmd, check=True)

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] TTS subprocess failed: {e}")
        return "[ERROR] Failed to synthesize speech"

    return output_path

# # Test the function
# transcribe_text_to_speech("Halo, apa kabar? Ini adalah contoh teks yang diubah menjadi suara menggunakan Coqui TTS.")