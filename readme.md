# Google Cloud TTS Converter

Proyek ini berguna untuk mengubah banyak file teks (`.txt`) menjadi file audio (`.wav`) menggunakan **Google Cloud Text-to-Speech (TTS)** dengan voice **Despina (Chirp3-HD)**.
Mendukung bahasa **Indonesia (`id-ID`)** dan **Inggris (`en-US`)** dengan output otomatis dipisahkan berdasarkan folder.

---

## Struktur Folder

```
project_root/
│
├── gcp_client_tts.py         # modul utama TTS (fungsi inti)
├── main_tts_batch.py         # script batch converter (multi file)
├── gcp_credential/           # folder berisi credential GCP
│   └── service_account.json
│
├── input/                    # folder input teks
│   ├── en/                   # teks bahasa Inggris
│   │   ├── grammar.txt
│   │   └── speaking.txt
│   └── id/                   # teks bahasa Indonesia
│       ├── grammar.txt
│       └── speaking.txt
│
└── output/                   # hasil audio
    ├── en/
    │   ├── grammar.wav
    │   └── speaking.wav
    └── id/
        ├── grammar.wav
        └── speaking.wav
```

---

## Instalasi

1. **Clone repository / copy project**

   ```bash
   git clone <url-repo>
   cd project_root
   ```

2. **Install dependencies**

   ```bash
   pip install google-cloud-texttospeech soundfile
   ```

3. **Siapkan Credential GCP**

   * Buat **Service Account** di [Google Cloud Console](https://console.cloud.google.com/).
   * Aktifkan **Text-to-Speech API**.
   * Download file `service_account.json`.
   * Simpan di folder:

     ```
     project_root/gcp_credential/service_account.json
     ```

---

## Cara Pakai

### 1. Convert semua teks bahasa Inggris

```bash
python main_tts_batch.py input/en --lang en-US
```

> Semua file `.txt` di `input/en/` akan dikonversi menjadi `.wav` di `output/en/`.

### 2. Convert semua teks bahasa Indonesia

```bash
python main_tts_batch.py input/id --lang id-ID
```

> Semua file `.txt` di `input/id/` akan dikonversi menjadi `.wav` di `output/id/`.

### 3. Atur kecepatan bicara

```bash
python main_tts_batch.py input/en --lang en-US --speed 0.9
```

> Suara akan lebih lambat sedikit (default `1.0`).

---

## Voice yang Digunakan

* **Indonesia (id-ID)** → `id-ID-Chirp3-HD-Despina`
* **English (en-US)** → `en-US-Chirp3-HD-Despina`

> Voice default sudah otomatis **Despina**, jadi Anda hanya perlu mengganti `--lang` (`id-ID` atau `en-US`).

---

## Catatan

* Semua file `.txt` dalam folder input akan dikonversi.
* Nama output akan sama dengan nama file input, tetapi dengan ekstensi `.wav`.
* Jika folder `output/en` atau `output/id` belum ada, akan dibuat otomatis.

## Author
Muhammad Ricky Rizaldi
