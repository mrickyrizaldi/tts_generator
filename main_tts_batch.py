import argparse
import os
import time
from pathlib import Path
from gcp_client_tts import save_tts_to_file

# Mapping bahasa → voice Despina
VOICE_MAP = {
    "en-US": "en-US-Chirp3-HD-Despina",
    "id-ID": "id-ID-Chirp3-HD-Despina",
}

def process_folder(input_folder: Path, lang: str, speed: float):
    if lang not in VOICE_MAP:
        raise ValueError(f"Bahasa {lang} tidak tersedia. Pilih dari: {list(VOICE_MAP.keys())}")

    voice_name = VOICE_MAP[lang]

    # folder output otomatis
    lang_folder = Path("output") / lang.split("-")[0]  # "id" atau "en"
    lang_folder.mkdir(parents=True, exist_ok=True)

    for txt_file in input_folder.glob("*.txt"):
        with open(txt_file, "r", encoding="utf-8") as f:
            isi_teks = f.read()

        output_file = lang_folder / (txt_file.stem + ".wav")

        print(f"Convert: {txt_file} → {output_file}")

        save_tts_to_file(
            text=isi_teks,
            output_file=str(output_file),
            language_code=lang,
            voice_name=voice_name,
            speaking_rate=speed,
        )
        time.sleep(1) // delay agar ada jeda setelah 1 file

def main():
    parser = argparse.ArgumentParser(description="Google Cloud TTS Batch Converter")
    parser.add_argument("input_folder", help="Folder input teks (misal: input/en atau input/id)")
    parser.add_argument("--lang", required=True, choices=VOICE_MAP.keys(),
                        help="Kode bahasa (id-ID atau en-US)")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="Kecepatan bicara (default: 1.0)")
    args = parser.parse_args()

    input_folder = Path(args.input_folder)
    if not input_folder.exists():
        print(f"[ERROR] Folder {input_folder} tidak ditemukan")
        return

    process_folder(input_folder, args.lang, args.speed)

if __name__ == "__main__":
    main()
