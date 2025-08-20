# gcp_client_tts.py
# pip install google-cloud-texttospeech soundfile

import os
import io
import json
from pathlib import Path
import soundfile as sf
from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPIError


# === KONFIGURASI KREDENSIAL & CLIENT ===
# 1. Cek dari environment variable dulu
service_account_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

if service_account_file and Path(service_account_file).exists():
    SERVICE_ACCOUNT_FILE = Path(service_account_file)
else:
    # 2. Kalau tidak ada, cari di folder project/gcp_credential
    CREDENTIALS_DIR = Path(__file__).parent / "gcp_credential"
    SERVICE_ACCOUNT_FILE = next(CREDENTIALS_DIR.glob("*.json"), None)

if not SERVICE_ACCOUNT_FILE or not SERVICE_ACCOUNT_FILE.exists():
    raise FileNotFoundError(
        f"Service Account JSON tidak ditemukan.\n"
        f"Set environment variable GOOGLE_APPLICATION_CREDENTIALS atau taruh file di: {Path(__file__).parent/'gcp_credential'}"
    )

# Set env supaya dipakai google-cloud library
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(SERVICE_ACCOUNT_FILE)

with open(SERVICE_ACCOUNT_FILE, "r", encoding="utf-8") as f:
    PROJECT_ID = json.load(f).get("project_id")
if not PROJECT_ID:
    raise ValueError("Atribut 'project_id' tidak ditemukan di file Service Account.")

tts_client = texttospeech.TextToSpeechClient()


# === FUNGSI UTAMA TTS ===
def gcp_text_to_speech(text, language_code="id-ID", voice_name=None, speaking_rate=1.0):
    """
    Mengubah teks menjadi audio menggunakan Google Cloud Text-to-Speech.

    Returns:
        bytes: Data audio hasil TTS dalam format LINEAR16.
    """
    if not text:
        return b""

    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice_params = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name or f"{language_code}-Wavenet-A",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate=speaking_rate,
        )
        resp = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice_params, audio_config=audio_config
        )
        return resp.audio_content

    except GoogleAPIError as e:
        print(f"[ERROR TTS] {e}")
        return b""
    except Exception as e:
        print(f"[ERROR Tak Terduga] {e}")
        return b""


# === HELPER UNTUK SIMPAN KE FILE ===
def save_tts_to_file(
    text: str,
    output_file: str,
    language_code: str = "id-ID",
    voice_name: str = "id-ID-Standard-A",
    speaking_rate: float = 1.0,
):
    """
    Konversi teks ke audio menggunakan Google Cloud TTS dan simpan ke file .wav
    """
    audio_content = gcp_text_to_speech(
        text=text,
        language_code=language_code,
        voice_name=voice_name,
        speaking_rate=speaking_rate,
    )

    if not audio_content:
        print("Tidak ada audio yang dihasilkan dari GCP TTS.")
        return False

    try:
        buffer = io.BytesIO(audio_content)
        data, samplerate = sf.read(buffer, dtype="int16")
        sf.write(output_file, data, samplerate)
        print(f"Audio berhasil disimpan ke {output_file}")
        return True
    except Exception as e:
        print(f"Gagal menyimpan audio: {e}")
        return False


# === SHORTCUT UNTUK VOICE DESPINA (Chirp3-HD) ===
def save_tts_en(text: str, output_file: str, speed: float = 1.0):
    return save_tts_to_file(
        text=text,
        output_file=output_file,
        language_code="en-US",
        voice_name="en-US-Chirp3-HD-Despina",
        speaking_rate=speed,
    )


def save_tts_id(text: str, output_file: str, speed: float = 1.0):
    return save_tts_to_file(
        text=text,
        output_file=output_file,
        language_code="id-ID",
        voice_name="id-ID-Chirp3-HD-Despina",
        speaking_rate=speed,
    )


# Contoh Pemanggilan CLI
if __name__ == "__main__":
    teks = "Halo dunia, ini adalah contoh TTS Google Cloud dengan suara Despina."
    save_tts_id(teks, "contoh_id.wav")
    save_tts_en("Hello world, this is Google Cloud TTS with Despina voice.", "contoh_en.wav")
