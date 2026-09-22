# 🎙️ Voice Assistant

A feature-rich, modular Python-based desktop voice assistant developed as part of the **OASIS Infobyte Python Programming Internship (Task 1)**.

The assistant provides a seamless dual-interface experience, supporting both interactive **Command Line Interface (CLI)** execution and a modern, responsive **Desktop Graphical User Interface (GUI)** built with Tkinter. It leverages speech recognition, text-to-speech (TTS) synthesis, natural-language intent parsing, and safe AST expression evaluation to deliver an intelligent hands-free computing assistant.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
  - [Conversation](#conversation)
  - [Voice \& Speech](#voice--speech)
  - [Date \& Time](#date--time)
  - [Calculator](#calculator)
  - [Web Navigation \& Search](#web-navigation--search)
  - [System Information](#system-information)
  - [Productivity](#productivity)
  - [Education \& Knowledge](#education--knowledge)
  - [Desktop Automation](#desktop-automation)
  - [Custom Commands](#custom-commands)
  - [Graphical User Interface (GUI)](#graphical-user-interface-gui)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Installation \& Setup](#-installation--setup)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
- [Usage](#-usage)
  - [Running the GUI Interface](#running-the-gui-interface)
  - [Running the CLI Interface](#running-the-cli-interface)
- [Configuration](#-configuration)
  - [Environment Variables (.env)](#environment-variables-env)
  - [Custom Commands (custom_commands.json)](#custom-commands-custom_commandsjson)
- [Testing](#-testing)
- [License \& Acknowledgments](#-license--acknowledgments)

---

## 📌 Project Overview

The **Voice Assistant** project was designed to demonstrate clean software architecture, modular design, and robust user interaction models in Python.

### Key Highlights:
* **Speech Recognition & TTS**: Captures audio input from the user's microphone using PyAudio and Google Speech Recognition, while providing spoken responses via `pyttsx3`.
* **Dual Interface**: Operates either as a terminal CLI application or a multi-threaded Tkinter Desktop GUI.
* **Intent-Driven Routing**: Uses regex-based pattern matching in `intent_parser.py` and modular action dispatching in `command_router.py` to route queries to specialized handler functions.
* **Safety & Security**: Employs Python's Abstract Syntax Tree (`ast`) module for arithmetic calculations to strictly prevent arbitrary code execution (`eval` is NOT used). Desktop launching is restricted via configured whitelists.

---

## ⚡ Features

### Conversation
* **Greetings & Small Talk**: Responds to conversational greetings like *"Hello"*, *"Hi"*, *"Good morning"*, and *"How are you?"*.
* **Help System**: Outlines supported command formats and capabilities when asked *"Help"* or *"What can you do?"*.
* **Exit Handling**: Gracefully shuts down audio threads and closes the application on commands like *"Exit"*, *"Quit"*, *"Bye"*, or *"Stop"*.

### Voice & Speech
* **Microphone Input Capture**: Continuously listens for voice input with automatic energy threshold adjustment for background noise.
* **Online Speech Recognition**: Converts speech to text using Google Web Speech API integration.
* **Text-to-Speech (TTS) Engine**: Offline TTS voice output using `pyttsx3` with configurable speech rate and volume.
* **Repeat Response**: Repeats the last spoken or generated response upon request.
* **Background Reminders**: Spoken audio alerts for scheduled reminders even while performing other tasks.

### Date & Time
* **Current Time**: Reports local time in 12-hour or 24-hour formats (e.g., *"What time is it?"*).
* **Current Date**: Announces the day, date, month, and year (e.g., *"What is today's date?"*).

### Calculator
* **Natural-Language Arithmetic**: Evaluates basic math expressions from spoken or typed queries:
  * *"Calculate 25 times 8"* $\rightarrow$ `200`
  * *"Calculate 150 divided by 3"* $\rightarrow$ `50`
  * *"What is 45 plus 12?"* $\rightarrow$ `57`
* **AST-Safe Evaluation**: Parses mathematical operations safely using Python's `ast` module. **Arbitrary Python code execution is strictly prohibited.**

### Web Navigation & Search
* **Web Search**: Opens default browser with Google search results (e.g., *"Search web for Python tutorials"*).
* **YouTube Search**: Searches and launches YouTube videos (e.g., *"Search YouTube for lofi music"*).
* **Website Launcher**: Directly opens popular websites (e.g., *"Open Google"*, *"Open GitHub"*, *"Open StackOverflow"*).

### System Information
* **Battery Status**: Displays and speaks current battery percentage and charging state (via `psutil`).
* **RAM Usage**: Reports total, available, and percentage of memory utilized.
* **CPU Metrics**: Reports CPU utilization percentage and core counts.
* **OS & System Metrics**: Provides OS details, system architecture, and hostname information.

### Productivity
* **Reminders**: Sets timed alerts and background notifications (e.g., *"Remind me in 5 minutes to take a break"*).
* **Quick Notes**: Creates, appends, and reads back saved text notes.
* **Email Assistance**: Interactive email drafting helper for standard email structures.

### Education & Knowledge
* **Concept Explanations**: Provides quick explanations of technical concepts, science topics, and programming terminology.
* **Programming Assistance**: Answers syntax and coding queries for Python and software engineering.
* **Wikipedia / General Knowledge**: Integrated fallback querying Wikipedia for quick summaries on general knowledge queries.

### Desktop Automation
* **Application Launching**: Opens system applications (e.g., Notepad, Calculator, Browser).
* **Folder Launching**: Quick access to system folders (Downloads, Documents, Pictures).
* **Whitelist Protection**: Restricts app and folder launching to pre-approved items to prevent unauthorized system file access.

### Custom Commands
* **JSON Configuration**: Custom user-defined trigger phrases and responses stored in `custom_commands.json`.
* **Dynamic Loading**: Extends assistant capabilities without modifying Python source code.

### Graphical User Interface (GUI)
* **Tkinter Interface**: Clean, modern desktop application interface.
* **Live Conversation History**: Scrollable chat view displaying user queries and assistant responses.
* **Status Indicators**: Visual status bar showing state (*Listening*, *Processing*, *Speaking*, *Idle*).
* **Interactive Controls**:
  * 🎙️ **Start Listening**: Begins voice capture.
  * ⏹️ **Stop Assistant**: Cancels ongoing TTS or voice capture.
  * 🧹 **Clear Conversation**: Resets the chat log view.
  * ✉️ **Manual Text Input & Send Button**: Allows full assistant control via typing without a microphone.

---

## 🏗️ Architecture

The application follows a clean modular architecture separating voice input/output, intent parsing, command routing, and action execution.

```mermaid
flowchart TD
    subgraph Input Layer
        A[Microphone Audio] -->|Speech Recognition| C[Text Query]
        B[GUI Text Box] --> C
    end

    subgraph Core Processing
        C --> D[Intent Parser]
        D -->|Identified Intent & Entities| E[Command Router]
    end

    subgraph Execution & Action Handlers
        E --> F[Actions Engine]
        F --> F1[Conversation Actions]
        F --> F2[System Info Actions]
        F --> F3[Web & Search Actions]
        F --> F4[Calculator & AST Actions]
        F --> F5[Productivity & Notes Actions]
        F --> F6[Custom Commands JSON]
    end

    subgraph Output Layer
        F --> G[Response Synthesizer]
        G --> H[TTS Engine - Audio Output]
        G --> I[GUI Chat Log & Status Bar]
    end