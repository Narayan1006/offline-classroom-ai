# 🎓 Siksha Saathi – Offline AI Teaching Assistant

Siksha Saathi is an **offline-first AI classroom assistant** designed for students and teachers in **low or no internet environments**.  
It converts recorded classroom videos into **structured lessons** and allows students to **chat with AI strictly based on that lesson**.

---

## 🚀 Key Features

- 🎥 Upload recorded classroom video
- 🔊 Automatic audio extraction (offline)
- 🧠 Offline speech-to-text transcription
- 🏷️ Topic extraction from lecture
- 💬 Lesson-restricted AI chat (no hallucination)
- 📝 Built-in Notes & Tasks
- 🖥️ Fully offline desktop application (Windows)

---

## 📦 Download (Windows EXE)

👉 **Download Siksha Saathi (Windows):**  
🔗 **[Google Drive Link Here]**  
*(Replace this with your Drive link)*

> ⚠️ EXE size is large (~350 MB) because it bundles:
> - Python runtime  
> - PySide6 UI framework  
> - Offline AI dependencies  
> - FFmpeg  

This is expected for **offline AI applications**.

---

## 🧠 AI Engine (Offline)

Siksha Saathi uses **Ollama** to run Large Language Models **locally**.

### Required Software
You must install **Ollama** separately.

🔗 Download Ollama:  
https://ollama.com/download

---

## 📥 Required AI Model

After installing Ollama, open **Command Prompt / PowerShell** and run:

```bash
ollama pull mistral
