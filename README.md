# 🎤 Chintu Voice Assistant

Chintu is a simple Python-based voice assistant inspired by Jarvis.  
It listens for a wake word (**"Chintu"**) and responds to commands like telling the time, fetching news, opening websites, playing music, or simulating calls.  
The assistant speaks back using text-to-speech and can be extended with more features.

---

## ✨ Features
- Wake word detection: **"Chintu"**
- Responds with **"Bolo Sir ji"** when activated
- Commands supported:
  - **`open <website>`** → Opens websites (Google, YouTube, GitHub, Facebook, or any URL)
  - **`time batao`** → Speaks the current time
  - **`news batao`** → Reads out the latest headlines (via NewsAPI)
  - **`call <name>`** → Simulates making a call
  - **`music <song name>`** → Plays music by searching YouTube
  - **`bye`** → Stops the assistant

---

## 🛠 Requirements
- Python 3.8+
- Libraries:
  ```bash
  python -m pip install SpeechRecognition
  python -m pip install pyttsx3
  python -m pip install pyaudio
  python -m pip install requests
