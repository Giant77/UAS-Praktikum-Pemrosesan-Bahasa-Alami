# Daftar Isi

1. [Voice Chatbot UAS – STT, Gemini LLM, TTS Integration](#voice-chatbot-uas--stt-gemini-llm-tts-integration)
2. [Fitur Utama](#-fitur-utama)
3. [Struktur Proyek](#-struktur-proyek)
4. [Instalasi dan Menjalankan Proyek](#-instalasi-dan-menjalankan-proyek)
    - [Clone repository & setup local environment](#1-clone-repository--setup-local-environment)
    - [Setup project](#2-setup-project)
    - [Implementasi model TTS, dan STT](#3-implementasi-model-tts-dan-stt)
        - [STT](#stt)
        - [TTS](#tts)
    - [Jalankan Backend (FastAPI)](#4-jalankan-backend-fastapi)
    - [Setup dan jalankan Frontend (Streamlit)](#4-setup-dan-jalankan-frontend-streamlit)
5. [Konfigurasi API Key Gemini](#-konfigurasi-api-key-gemini)
6. [Catatan](#-catatan)
7. [Dibuat Untuk](#-dibuat-untuk)
8. [Demo Video](#demo-video)

# Voice Chatbot UAS – STT, Gemini LLM, TTS Integration

Proyek UAS ini merupakan aplikasi chatbot berbasis suara yang memungkinkan pengguna berbicara langsung melalui antarmuka web. Sistem akan mengenali suara pengguna, mengubahnya menjadi teks (Speech-to-Text), memprosesnya menggunakan model bahasa besar (Gemini API), lalu mengubah hasil jawabannya kembali menjadi suara (Text-to-Speech).

## 📌 Fitur Utama

-   🎙️ Speech-to-Text (STT) menggunakan `whisper.cpp` dari OpenAI.
-   🧠 LLM Integration menggunakan Google Gemini API untuk menghasilkan respons dalam Bahasa Indonesia.
-   🔊 Text-to-Speech (TTS) menggunakan model Coqui TTS (Indonesian TTS).
-   🧪 Antarmuka pengguna interaktif berbasis `Gradio` untuk pengujian langsung dari browser.

## 🗂️ Struktur Proyek

```
root
│
├── app/
│   ├── main.py                             # Endpoint utama FastAPI
│   ├── llm.py                              # Integrasi Gemini API
│   ├── stt.py                              # Transkripsi suara (whisper.cpp)
│   ├── tts.py                              # TTS dengan Coqui
│   ├── coqui_utils/                        # Model dan config Coqui TTS
│   └── whisper.cpp/                        # Hasil clone whisper.cpp
│       ├── model/                          # Folder model pada repository whisper.cpp
│       └── build/bin/Release               # Whisper interface untuk menjalankan model
│
├── gradio_app/
│   └── app.py                              # Frontend dengan Gradio
│
├── .env                                    # Menyimpan Gemini API Key
├── .env.example                            # Template .env
└── requirements.txt                        # Daftar dependensi library Python
```

## ⚙️ Instalasi dan Menjalankan Proyek

### 1. Clone repository & setup local environment

-   Clone repository
    Buka terminal, dan jalankan

```bash
git clone https://github.com/Giant77/UAS-Praktikum-Pemrosesan-Bahasa-Alami.git
cd UAS-Praktikum-Pemrosesan-Bahasa-Alami
```

-   Setup local environment
    Copy file env.example, Kemudian masukkan API key anda. Untuk detail pembuatan API key,
    silahkan merujuk pada bagian [berikut](#-konfigurasi-api-key-gemini)

```bash
cp .env.example .env
```

### 2. Setup project

-   Buat dan aktifkan virtual environment (opsional)

```bash
python3 -m venv venv       # Aktivasi venv
```

```bash
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

-   install library yang dibutuhkan

```bash
# Install dependencies
pip install -r requirements.txt
```

### 3. Implementasi model TTS, dan STT

#### STT

```bash
cd app
```

```bash
git clone https://github.com/ggerganov/whisper.cpp.git
```

Masuk ke direktori project _whisper.cpp_ dan install model yang diinginkan
menggunakan script yang tersedia, ataupun secara manual. Namun, pastikan model
berada pada direktori models, sesuai struktur proyek yang dicantumkan.

```bash
cd whisper.cpp
bash ./models/download-ggml-model.sh large-v3-turbo
```

Build project agar dapat dijalankan, silahkan merujuk repository whisper.cpp
untuk error & instruksi lebih lanjut dalam tahapan membangun project.

```bash
cmake --build build --config Release
```

#### TTS

Buat folder "coqui_utils" di direktori app.

```bash
mkdir coqui_utils
```

Navigasi repo [coqui_tts](https://github.com/Wikidepia/indonesian-tts), dan cari bagian
release(disarankan versi 1.2 atau lebih baru) untuk download 3 file yang diperlukan berikut:

-   checkpoint 1260000-inference.pth – file model utama.
-   config.json – file konfigurasi model yang menyimpan parameter dan pengaturan pelatihan.
-   speakers.pth – file daftar speaker yang tersedia untuk digunakan dalam sintesis suara.

Kemudian pada file confiq.json cari, dan gantikan baris dengan key "speakers_file",
dan ubah seperti referensi berikut, ataupun menyesuaikan dengan direktori yang dibuat.

```
    "speakers_file": "./coqui_utils/speakers.pth",
```

### 4. Jalankan Backend (FastAPI)

-   Jalankan server

**note:** pastikan anda telah berada di folder app (backend) project

Untuk debugging dan pengembangan lebih lanjut, jalankan command berikut

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Jika hanya ingin menjalankan project tanpa auto-reload server, cukup jalankan

```bash
python main.py
```

### 5. Setup dan jalankan Frontend (Gradio)

```bash
cd gradio_app
```

-   Buka terminal baru:
    note: Pastikan sudah berada di direktori gradio_app (frontend) project

Untuk menjalankan frontend, cukup jalankan

```bash
python app.py
```

---

## 🔐 Konfigurasi API Key Gemini

1. Buka [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Klik **Create API Key**.
3. Copy API key dan simpan ke dalam file `.env` di root project dengan format:

```env
GEMINI_API_KEY=YourSecretGeminiAPIKey
```

## 📚 Catatan

-   Semua file audio menggunakan format `.wav`.
-   Untuk menghasilkan fonem seperti `dəˈnɡan`, teks dari Gemini harus dikonversi ke fonetik.
-   Disarankan menggunakan model Whisper: `ggml-large-v3-turbo`.
-   Gunakan speaker: `wibowo` dari model Coqui v1.2.

## 👨‍💻 Dibuat Untuk

Proyek UAS mata kuliah _Pemrosesan Bahasa Alami_ — Semester Genap 2024/2025.

## Demo video

Link: [Youtube](https://youtu.be/H_ODTop6cpI)  
Etc.: [Linkedln](https://www.linkedin.com/feed/?shareActive=true&view=management)
