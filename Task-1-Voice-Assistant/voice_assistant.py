"""
OASIS Infobyte Python Internship — Task 1
Voice Assistant — Phase 2: Advanced Tier

Upgraded Python Voice Assistant featuring:
1. Phase 1 core functionality (Time, Date, Web Search, Greetings, Graceful Error Handling).
2. Natural Language Intent Parsing (Rule/Pattern-based without heavy NLP transformers).
3. Voice-Controlled Email sending via smtplib with env variable credentials.
4. Non-blocking Timed Reminders with audible pyttsx3 alerts.
5. Live Weather lookup via free OpenWeatherMap API with env key.
6. General Knowledge Question Answering (Local KB + Wikipedia API fallback).
7. Custom Voice Commands via safe custom_commands.json configuration.
8. Complete security compliance (no hardcoded secrets or unsafe shell executions).
"""

import datetime
import json
import os
import re
import smtplib
import sys
import threading
import time
import urllib.parse
import webbrowser
from email.mime.text import MIMEText
from typing import Any, Callable, Dict, Optional, Tuple

import requests
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Initialize TTS Engine persistent instance safely
try:
    _tts_engine = pyttsx3.init()
    _tts_engine.setProperty("rate", 175)
    _tts_engine.setProperty("volume", 1.0)
except Exception as e:
    _tts_engine = None
    print(f"[Warning] Failed to initialize pyttsx3 engine: {e}")

_tts_lock = threading.Lock()


def speak(text: str) -> None:
    """
    Speaks the given text using text-to-speech and prints it to standard output.
    Thread-safe implementation for background reminder notifications.
    """
    print(f"Assistant: {text}")
    global _tts_engine, _tts_lock
    if _tts_engine is not None:
        with _tts_lock:
            try:
                _tts_engine.say(text)
                _tts_engine.runAndWait()
            except Exception as err:
                print(f"[TTS Error] Could not speak response: {err}")


def listen(recognizer: sr.Recognizer, mic: sr.Microphone) -> Optional[str]:
    """
    Captures spoken audio from the microphone and converts it to text.
    Handles speech recognition errors gracefully.
    """
    try:
        with mic as source:
            print("\nListening... Speak into your microphone.")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.strip()
    except sr.WaitTimeoutError:
        speak("Listening timed out. Please try speaking again.")
        return None
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand. Please repeat.")
        return None
    except sr.RequestError as e:
        speak("I'm having trouble connecting to the speech recognition service.")
        print(f"[Debug] Speech recognition service error: {e}")
        return None
    except Exception as e:
        speak("An unexpected error occurred while accessing the microphone.")
        print(f"[Debug] Listening error: {e}")
        return None


# --- Phase 1 Utility Functions ---

def get_current_time() -> str:
    """Gets the current system time formatted in human-readable 12-hour format."""
    now = datetime.datetime.now()
    formatted_time = now.strftime("%I:%M %p").lstrip("0")
    return f"The current time is {formatted_time}."


def get_current_date() -> str:
    """Gets the current system date formatted in human-readable format."""
    now = datetime.datetime.now()
    formatted_date = now.strftime("%B %d, %Y").replace(" 0", " ")
    return f"Today's date is {formatted_date}."


def web_search(query: str) -> str:
    """Extracts search query from command, formats search URL, opens default web browser."""
    clean_query = query.strip()
    if not clean_query:
        return "What would you like me to search for?"

    encoded_query = urllib.parse.quote_plus(clean_query)
    url = f"https://www.google.com/search?q={encoded_query}"
    
    try:
        webbrowser.open(url)
        return f"Searching the web for {clean_query}."
    except Exception as e:
        print(f"[Debug] Browser open error: {e}")
        return f"Searching the web for {clean_query}."


# --- Phase 2 Advanced Features ---

def load_custom_commands(file_path: str = "custom_commands.json") -> Dict[str, str]:
    """
    Safely loads custom URL commands from a JSON file.
    Only allows HTTP/HTTPS URLs to prevent unsafe shell code execution.
    """
    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            print(f"[Warning] Custom commands file {file_path} does not contain a JSON dictionary.")
            return {}

        safe_commands = {}
        for cmd, target in data.items():
            if isinstance(cmd, str) and isinstance(target, str):
                cmd_clean = cmd.strip().lower()
                target_clean = target.strip()
                if target_clean.startswith("http://") or target_clean.startswith("https://"):
                    safe_commands[cmd_clean] = target_clean
                else:
                    print(f"[Warning] Rejecting unsafe custom command '{cmd}': target is not an HTTP/HTTPS URL.")

        return safe_commands
    except Exception as err:
        print(f"[Warning] Failed to parse custom commands file: {err}")
        return {}


def execute_custom_command(url: str) -> str:
    """Executes a validated custom command by opening the safe URL."""
    try:
        webbrowser.open(url)
        return f"Opening custom command link."
    except Exception as e:
        print(f"[Debug] Failed to open custom command URL: {e}")
        return f"Failed to open custom command link."


def get_weather(city: str) -> str:
    """
    Fetches live weather data for a given city from OpenWeatherMap API using WEATHER_API_KEY.
    """
    if not city or not city.strip():
        return "Please specify a city to check the weather."

    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather API key is not configured. Please set WEATHER_API_KEY in your environment or .env file."

    city_clean = city.strip()
    encoded_city = urllib.parse.quote_plus(city_clean)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            temp = round(data["main"]["temp"])
            description = data["weather"][0]["description"]
            city_name = data.get("name", city_clean)
            return f"The current temperature in {city_name} is {temp} degrees Celsius with {description}."
        elif response.status_code == 404:
            return f"Sorry, I couldn't find weather information for '{city_clean}'."
        else:
            return f"Weather service returned an error for '{city_clean}'."
    except requests.RequestException as e:
        print(f"[Debug] Weather API request failed: {e}")
        return "I'm having trouble connecting to the weather service."


def parse_reminder_args(command: str) -> Optional[Tuple[int, str, str]]:
    """
    Parses duration, time unit, and reminder message from a command string.
    Example: "remind me in 5 minutes to submit my assignment"
    Returns: tuple of (duration_int, unit_str, message_str) or None.
    """
    pattern = r"remind\s+(?:me\s+)?in\s+(\d+)\s*(seconds?|sec|minutes?|min|hours?|hrs?)\s*(?:to|that|about)?\s*(.*)"
    match = re.search(pattern, command, re.IGNORECASE)
    if not match:
        return None

    duration_val = int(match.group(1))
    unit_str = match.group(2).lower()
    message_str = match.group(3).strip()

    if not message_str:
        message_str = "do your scheduled task"

    return duration_val, unit_str, message_str


def _reminder_thread(seconds: int, message: str) -> None:
    """Background thread function that waits for seconds to elapse and speaks alert."""
    time.sleep(seconds)
    speak(f"Reminder alert! It is time to {message}.")


def schedule_reminder(command: str) -> str:
    """
    Schedules a non-blocking background timed reminder.
    """
    parsed = parse_reminder_args(command)
    if not parsed:
        return "Could not understand reminder duration or message. Please say for example: Remind me in 5 minutes to submit my assignment."

    duration, unit, message = parsed
    if duration <= 0:
        return "Reminder duration must be a positive number."

    multiplier = 1
    if "min" in unit:
        multiplier = 60
    elif "hour" in unit or "hr" in unit:
        multiplier = 3600

    total_seconds = duration * multiplier

    t = threading.Thread(target=_reminder_thread, args=(total_seconds, message), daemon=True)
    t.start()

    unit_display = "second" if total_seconds == 1 else unit
    return f"Reminder set for {duration} {unit_display} from now to {message}."


def check_email_credentials() -> Tuple[bool, str]:
    """Verifies if SMTP email credentials are fully configured in environment."""
    email_addr = os.getenv("EMAIL_ADDRESS")
    email_pass = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = os.getenv("SMTP_PORT", "587")

    if not email_addr or not email_pass:
        return False, "Email configuration is incomplete. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in your environment or .env file."
    return True, ""


def send_email_flow(recognizer: Optional[sr.Recognizer] = None, mic: Optional[sr.Microphone] = None, test_inputs: Optional[Dict[str, str]] = None) -> None:
    """
    Executes interactive voice-controlled email flow using smtplib.
    Supports automated testing via test_inputs dictionary without blocking.
    """
    configured, msg = check_email_credentials()
    if not configured:
        speak(msg)
        return

    email_addr = os.getenv("EMAIL_ADDRESS")
    email_pass = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    # Obtain recipient
    if test_inputs:
        recipient = test_inputs.get("recipient")
    else:
        speak("Who should I send the email to?")
        recipient = listen(recognizer, mic) if (recognizer and mic) else None

    if not recipient:
        speak("Email canceled. Recipient was not provided.")
        return

    # Obtain subject
    if test_inputs:
        subject = test_inputs.get("subject")
    else:
        speak("What is the subject of the email?")
        subject = listen(recognizer, mic) if (recognizer and mic) else None

    if not subject:
        subject = "No Subject"

    # Obtain body
    if test_inputs:
        body = test_inputs.get("body")
    else:
        speak("What is the message?")
        body = listen(recognizer, mic) if (recognizer and mic) else None

    if not body:
        speak("Email canceled. Message body was not provided.")
        return

    speak("Sending email...")
    try:
        msg_obj = MIMEText(body)
        msg_obj["Subject"] = subject
        msg_obj["From"] = email_addr
        msg_obj["To"] = recipient

        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(email_addr, email_pass)
            server.send_message(msg_obj)

        speak(f"Email sent successfully to {recipient}.")
    except Exception as err:
        print(f"[Debug] SMTP send error: {err}")
        speak("Failed to send email. Please check your SMTP settings and network connection.")


def answer_question(query: str) -> str:
    """
    Answers general knowledge questions using a lightweight local KB + Wikipedia API summary fallback.
    """
    q_clean = query.lower().strip()

    # Local Knowledge Base for immediate lightweight responses
    local_kb = {
        "who created python": "Guido van Rossum created Python in 1991.",
        "who made python": "Guido van Rossum created Python in 1991.",
        "what is python": "Python is a popular, high-level, interpreted programming language known for readability and versatility.",
        "capital of france": "The capital of France is Paris.",
        "capital of india": "The capital of India is New Delhi.",
        "capital of USA": "The capital of the United States is Washington, D.C.",
        "capital of united states": "The capital of the United States is Washington, D.C.",
        "speed of light": "The speed of light in vacuum is approximately 299,792,458 meters per second.",
    }

    for key, answer in local_kb.items():
        if key in q_clean:
            return answer

    # Fallback to Wikipedia API search for general queries
    search_term = re.sub(r"^(what is|who is|tell me about|what is the|who created)\s+", "", q_clean).strip()
    if not search_term:
        search_term = q_clean

    try:
        encoded_term = urllib.parse.quote_plus(search_term)
        wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_term}"
        res = requests.get(wiki_url, timeout=4)
        if res.status_code == 200:
            data = res.json()
            extract = data.get("extract")
            if extract:
                # Limit summary to 2 sentences for concise voice output
                sentences = extract.split(". ")
                concise_answer = ". ".join(sentences[:2])
                if not concise_answer.endswith("."):
                    concise_answer += "."
                return concise_answer
    except Exception as e:
        print(f"[Debug] Wikipedia lookup failed: {e}")

    return f"I'm sorry, I don't have an answer for '{query}' right now."


# --- Natural Language Intent Parser ---

def parse_intent(command: str, custom_commands: Dict[str, str]) -> Tuple[str, Dict[str, Any]]:
    """
    Parses conversational natural language text into intent and payload parameters.

    Returns:
        tuple of (intent_name, params_dict)
    """
    cmd_lower = command.lower().strip()

    # 1. Exit Intent
    exit_words = ["exit", "quit", "goodbye", "stop", "bye"]
    if any(cmd_lower == w or cmd_lower.startswith(f"{w} ") for w in exit_words):
        return "exit", {}

    # 2. Custom Commands Intent (exact or phrase match)
    for custom_key, custom_url in custom_commands.items():
        if custom_key in cmd_lower:
            return "custom_command", {"url": custom_url}

    # 3. Reminder Intent
    if "remind" in cmd_lower:
        return "reminder", {"command": command}

    # 4. Email Intent
    if "email" in cmd_lower or "send an email" in cmd_lower or "send email" in cmd_lower:
        return "email", {}

    # 5. Weather Intent
    weather_triggers = ["weather", "temperature", "forecast"]
    if any(wt in cmd_lower for wt in weather_triggers):
        city = ""
        city_match = re.search(r"\b(?:in|for|at)\b\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?)", cmd_lower)
        if city_match:
            city = city_match.group(1).replace("today", "").replace("now", "").strip()
        else:
            words = cmd_lower.split()
            if len(words) > 1:
                city = words[-1]
        return "weather", {"city": city}

    # 6. Time Intent
    time_triggers = ["what time", "tell me the time", "current time", "time right now", "time is it"]
    if any(tt in cmd_lower for tt in time_triggers):
        return "time", {}

    # 7. Date Intent
    date_triggers = ["what is today's date", "what's today's date", "tell me the date", "today's date", "current date"]
    if any(dt in cmd_lower for dt in date_triggers):
        return "date", {}

    # 8. Web Search Intent
    if "search" in cmd_lower:
        topic = ""
        search_match = re.search(r"search\s+(?:for\s+|the\s+web\s+for\s+|the\s+internet\s+for\s+)?(.*)", cmd_lower)
        if search_match:
            topic = search_match.group(1).strip()
        return "web_search", {"topic": topic if topic else cmd_lower}

    # 9. General Knowledge Intent
    gk_triggers = ["who created", "who made", "what is", "who is", "capital of", "speed of"]
    if any(gk in cmd_lower for gk in gk_triggers):
        return "general_knowledge", {"query": command}

    # 10. Greetings Intent
    greetings = ["hello", "hi", "hey"]
    if any(cmd_lower == g or cmd_lower.startswith(f"{g} ") or f" {g} " in f" {cmd_lower} " for g in greetings):
        return "greeting", {}

    return "unknown", {}


def handle_command(command: str, custom_commands: Optional[Dict[str, str]] = None, recognizer: Optional[sr.Recognizer] = None, mic: Optional[sr.Microphone] = None) -> bool:
    """
    Parses natural language commands and executes corresponding actions.

    Returns:
        bool: True to continue loop, False to exit.
    """
    if not command:
        return True

    if custom_commands is None:
        custom_commands = load_custom_commands()

    intent, params = parse_intent(command, custom_commands)

    if intent == "exit":
        speak("Goodbye! Have a great day.")
        return False
    elif intent == "greeting":
        speak("Hello! How can I help you?")
        return True
    elif intent == "time":
        speak(get_current_time())
        return True
    elif intent == "date":
        speak(get_current_date())
        return True
    elif intent == "web_search":
        speak(web_search(params.get("topic", "")))
        return True
    elif intent == "weather":
        speak(get_weather(params.get("city", "")))
        return True
    elif intent == "reminder":
        speak(schedule_reminder(params.get("command", "")))
        return True
    elif intent == "email":
        send_email_flow(recognizer, mic)
        return True
    elif intent == "custom_command":
        speak(execute_custom_command(params.get("url", "")))
        return True
    elif intent == "general_knowledge":
        speak(answer_question(params.get("query", "")))
        return True
    else:
        speak("Sorry, I didn't understand that command. Please try again.")
        return True


def main() -> None:
    """Main entry point for running the voice assistant interactive loop."""
    speak("Initializing Voice Assistant Phase 2...")
    custom_cmds = load_custom_commands()
    if custom_cmds:
        print(f"Loaded {len(custom_cmds)} custom command(s).")

    try:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
    except Exception as err:
        speak("Error initializing microphone or speech recognition service.")
        print(f"[Fatal Error] {err}")
        print("Please check that PyAudio and a working microphone are installed.")
        sys.exit(1)

    speak("Voice Assistant Phase 2 is ready. How can I help you?")

    keep_running = True
    while keep_running:
        command = listen(recognizer, mic)
        if command is not None:
            keep_running = handle_command(command, custom_cmds, recognizer, mic)

    print("Voice Assistant terminated cleanly.")


if __name__ == "__main__":
    main()
