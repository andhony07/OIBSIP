# OASIS Infobyte Voice Assistant — Phase 2 (Advanced Tier)

An intelligent, clean, and extensible Python Voice Assistant upgraded from Phase 1 (Beginner Tier) to Phase 2 (Advanced Tier). It features Natural Language Intent Understanding, Voice Email Sending, Non-blocking Timed Reminders, Live Weather Integration, General Knowledge QA, and Custom Command execution.

---

## Key Features

### Phase 1 (Beginner Tier — Preserved)
- **Microphone Voice Input**: Listens for user audio input via `SpeechRecognition` & PyAudio.
- **Text-to-Speech (TTS)**: Offline Windows SAPI5 audio synthesis via `pyttsx3`.
- **Predefined Greetings**: Responds to *"Hello"*, *"Hi"*, *"Hey"*.
- **Current Time & Date**: Dynamic human-readable datetime retrieval.
- **Web Search**: Opens default web browser for Google Search requests.
- **Error & Exception Handling**: Graceful recovery from speech recognition timeouts and unrecognized audio.
- **Clean Exit**: Exits execution loop cleanly on *"exit"*, *"quit"*, *"goodbye"*, *"stop"*.

### Phase 2 (Advanced Tier — Upgraded)
- **Natural Language Understanding (NLU)**: Pattern-based intent engine that parses natural conversational phrasing (e.g., *"Could you tell me what the weather is like in Chennai?"*, *"What time do we have right now?"*, *"Remind me in 5 minutes to submit my assignment"*).
- **Voice-Controlled Email**: Interactive email composition flow via `smtplib`. Reads SMTP credentials securely from environment variables.
- **Non-Blocking Timed Reminders**: Background thread timer (`threading.Thread`) that speaks an audible alert when the timer expires without blocking main loop execution.
- **Live Weather Updates**: Live weather data retrieval via OpenWeatherMap API using `WEATHER_API_KEY`.
- **General Knowledge QA**: Responds to factual queries (*"Who created Python?"*, *"What is Python?"*, *"What is the capital of France?"*) using a local KB with Wikipedia API fallback.
- **Custom Voice Commands**: Executes user-defined safe HTTP/HTTPS link triggers configured in `custom_commands.json`.

---

## Project Structure

```text
E:\Oasis Internship\Voice Assistant\
├── .env.example              # Template for environment variables
├── .gitignore                # Excludes secrets (.env) and Python bytecode
├── README.md                 # Full documentation
├── custom_commands.json      # Safe custom URL triggers
├── implementation_report.md  # Detailed Phase 2 technical verification report
├── requirements.txt          # Third-party dependencies
├── test_voice_assistant.py   # Unit & logic test suite
└── voice_assistant.py        # Core application entry point
```

---

## Installation & Setup

### Prerequisites
- Windows 10 or 11.
- Python 3.10+ installed and on `PATH`.
- Active working microphone and Internet connection.

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

Edit `.env` to configure your credentials securely:
```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

WEATHER_API_KEY=your_openweathermap_api_key
```

> **Security Note**: Never commit your `.env` file. It is explicitly ignored in `.gitignore`.

---

## How to Run

Execute the main voice assistant script:
```powershell
python voice_assistant.py
```

Run logic & unit tests:
```powershell
python -m unittest test_voice_assistant.py
```

---

## Supported Voice Commands & Natural Language Examples

| Category | Conversational Spoken Example | Response / Action |
|---|---|---|
| **Greetings** | *"Could you say hello to me?"*, *"Hello"* | Speaks: *"Hello! How can I help you?"* |
| **Current Time** | *"What time do we have right now?"*, *"Current time"* | Speaks dynamic system time |
| **Current Date** | *"Could you tell me today's date?"*, *"Tell me the date"* | Speaks dynamic system date |
| **Web Search** | *"Please search the internet for Python tutorials"* | Speaks confirmation & opens search in browser |
| **Live Weather** | *"Could you tell me what the weather is like in Chennai?"* | Speaks live temp & weather condition from API |
| **Timed Reminder** | *"Remind me in 5 minutes to submit my assignment"* | Schedules timer & speaks audible alert on expiry |
| **Voice Email** | *"I need to send an email"* | Prompts for recipient, subject, body & sends via SMTP |
| **General Knowledge** | *"Who created Python?"*, *"What is the capital of France?"* | Speaks factual answer |
| **Custom Commands** | *"open github"*, *"open youtube"* | Opens configured safe HTTP/HTTPS URL |
| **Exit** | *"exit"*, *"quit"*, *"goodbye"*, *"stop"* | Speaks farewell & exits cleanly |

---

## Custom Commands Configuration (`custom_commands.json`)

Configure custom voice commands by mapping spoken trigger phrases to safe web links:
```json
{
    "open github": "https://github.com",
    "open youtube": "https://youtube.com",
    "open python documentation": "https://docs.python.org/3/"
}
```

> **Security Guardrail**: Custom commands are strictly restricted to opening `http://` or `https://` URLs. Arbitrary shell commands or Python code execution are rejected.

---

## Security & Privacy Disclosures

- **Microphone Access**: Microphone stream audio is captured only during active listening calls.
- **Speech-to-Text Processing**: Spoken audio snippets are transmitted over HTTPS to Google's public Speech Recognition service.
- **Text-to-Speech Synthesis**: Speech output generation via `pyttsx3` is performed completely offline on Windows.
- **Credential Storage**: Passwords and API keys are read exclusively from environment variables (`.env`). No secrets are hardcoded or persisted in logs.
- **No Data Retention**: Voice recordings and command logs are never saved to disk.
- **Custom Command Safety**: Non-HTTP/HTTPS targets in `custom_commands.json` are rejected at runtime.

---

## Known Limitations

- **Internet Dependency**: Speech recognition, live weather, and Wikipedia QA fallback require an active network connection.
- **Environment Credentials**: If `WEATHER_API_KEY` or SMTP credentials are missing, the assistant speaks a clear missing-configuration message rather than attempting network calls.
