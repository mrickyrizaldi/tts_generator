import argparse
from gcp_client_tts import save_tts_to_file

# Mapping bahasa → voice Despina
VOICE_MAP = {
    "en-US": "en-US-Chirp3-HD-Despina",
    "id-ID": "id-ID-Chirp3-HD-Despina",
}

def main():
    parser = argparse.ArgumentParser(description="Google Cloud TTS Converter")
    parser.add_argument("input_file", help="File teks input")
    parser.add_argument("output_file", help="File output audio (misal: output.wav)")
    parser.add_argument("--lang", default="id-ID", choices=VOICE_MAP.keys(),
                        help="Kode bahasa (default: id-ID)")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="Kecepatan bicara (default: 1.0)")
    args = parser.parse_args()

    # baca isi teks
    with open(args.input_file, "r", encoding="utf-8") as f:
        isi_teks = f.read()

    # tentukan voice otomatis
    voice_name = VOICE_MAP.get(args.lang)

    # konversi ke TTS
    save_tts_to_file(
        text=isi_teks,
        output_file=args.output_file,
        language_code=args.lang,
        voice_name=voice_name,
        speaking_rate=args.speed,
    )

if __name__ == "__main__":
    main()
