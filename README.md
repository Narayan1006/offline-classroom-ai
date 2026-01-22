# 🎓 Siksha Saathi – Offline AI Teaching Assistant

Siksha Saathi is an **offline-first AI classroom assistant** that converts recorded classroom videos into **structured lessons** and allows students to **ask questions strictly from that lesson**, even without internet access.

This project is designed for **low-connectivity environments**, rural education, and offline learning use cases.

---

## 🚀 Features

- 🎥 Upload recorded classroom videos
- 🔊 Extract audio from video (offline)
- 🧠 Offline speech-to-text transcription
- 🏷️ Automatic topic extraction
- 💬 AI chat restricted to lesson content (no hallucination)
- 📝 Notes and Tasks management
- 🖥️ Desktop application (Windows)

---

## 🧠 Offline AI Architecture

Siksha Saathi uses **local LLM inference** via **Ollama**, ensuring:
- No internet dependency during usage
- Privacy-safe AI responses
- Deterministic answers from lesson content only

---

## 🛠 Tech Stack

- **Frontend:** PySide6 (Qt)
- **Backend:** Python
- **AI Runtime:** Ollama (local LLM)
- **Speech-to-Text:** Offline Whisper
- **Video Processing:** FFmpeg
- **Packaging:** PyInstaller

---

## 📦 Windows Application

A pre-built Windows executable is provided via Google Drive.

👉 **Download EXE:**  
🔗 *(Link provided in submission / release notes)*

> The EXE size is large because it bundles:
> - Python runtime
> - UI framework
> - Offline AI dependencies
> - FFmpeg

This is expected for offline-first AI applications.

---

## ⚙️ Setup for Developers

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/siksha-saathi.git
cd siksha-saathi
