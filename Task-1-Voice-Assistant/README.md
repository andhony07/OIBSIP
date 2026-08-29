# OASIS Infobyte Voice Assistant — Phase 4 (GUI & Advanced Edition)

An intelligent, clean, and extensible Python Voice Assistant featuring both a modern Tkinter Desktop Graphical User Interface (`voice_assistant_gui.py`) and a command-line interface (`voice_assistant.py`).

---

## Key Features

### Desktop GUI Features (Phase 4)
- **Modern Dark Theme**: Dark slate container (`#1e1e2e`), card panels, and styled typography.
- **Dynamic Status Indicator**: Real-time status badge (`Ready`, `Listening...`, `Processing...`, `Speaking...`, `Stopped`, `Error`).
- **Formatted Conversation Log**: Color-coded, scrollable history distinguishing User queries, Assistant responses, and System notifications.
- **Dual Input Modes**:
  - **Voice Input**: `Start Listening` button launches non-blocking background speech recognition thread.
  - **Text Input**: Entry field + `Send` button for manual text command fallback.
- **Control Action Buttons**: `Start Listening`, `Stop Assistant`, `Clear Conversation`.
- **Thread-Safe Architecture**: Tkinter main thread handles widget updates safely via queue dispatch; background threads process speech recognition and reminder alerts.

### Core Assistant Features (Phase 1 & Phase 2)
- **Natural Language Understanding (NLU)**: Pattern-based intent engine for conversational requests (*"Could you tell me what the weather is like in Chennai?"*, *"What time do we have right now?"*).
- **Voice-Controlled Email**: Interactive email composition flow via `smtplib` using `.env` credentials.
- **Non-Blocking Timed Reminders**: Background thread timer (`threading.Thread`) that speaks audible alerts upon expiration.
- **Live Weather Updates**: Live weather data retrieval via OpenWeatherMap API using `WEATHER_API_KEY`.
- **General Knowledge QA**: Factual queries (*"Who created Python?"*, *"What is Python?"*, *"What is the capital of France?"*) via local KB with Wikipedia REST API fallback.
- **Custom Voice Commands**: Safe HTTP/HTTPS URL triggers configured in `custom_commands.json`.
- **Microphone & TTS**: Speech input via `SpeechRecognition` & PyAudio; thread-safe offline TTS output via `pyttsx3` (Windows SAPI5 backend).

---

## Project Structure

```text
E:\Oasis Internship\Voice Assistant\
├── .env.example              # Template for environment variables
├── .gitignore                # Excludes secrets (.env) and Python bytecode
├── README.md                 # Full documentation
├── custom_commands.json      # Safe custom URL triggers
├── implementation_report.md  # Detailed technical execution report
├── requirements.txt          # Third-party dependencies
├── test_voice_assistant.py   # Unit & logic test suite
├── voice_assistant.py        # CLI application entry point & backend logic
└── voice_assistant_gui.py    # Desktop GUI application entry point
```

---

## Installation & Setup

### Prerequisites
- Windows 10 or 11.
- Python 3.10+ installed and on `PATH`.
- Working microphone and Internet connection.

### Step 1: Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

Required packages:
- `SpeechRecognition`
- `pyttsx3`
- `PyAudio`
- `python-dotenv`
- `requests`

### Step 2: Environment Configuration
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```

Configure environment credentials in `.env`:
```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

WEATHER_API_KEY=your_openweathermap_api_key
```

---

## How to Run

### Option A: Run Desktop GUI (Recommended)
```powershell
python voice_assistant_gui.py
```

### Option B: Run Command-Line Interface (CLI)
```powershell
python voice_assistant.py
```

### Option C: Run Automated Unit Tests
```powershell
python -m unittest test_voice_assistant.py
```

---

## Security & Privacy Disclosures

- **Microphone Access**: Microphone audio stream is active only during active listening intervals.
- **Speech-to-Text Processing**: Spoken audio snippets are transmitted over HTTPS to Google's public Speech Recognition service.
- **Text-to-Speech Synthesis**: Speech output generation via `pyttsx3` is performed completely offline on Windows.
- **Credential Security**: Credentials are read strictly from environment variables (`.env`). `.env` is ignored by Git.
- **No Data Retention**: Voice recordings and command logs are never saved to disk.
- **Custom Command Safety**: Non-HTTP/HTTPS targets in `custom_commands.json` are rejected at runtime.
