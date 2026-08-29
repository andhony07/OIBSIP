"""
OASIS Infobyte Python Internship — Task 1
Voice Assistant — Phase 4: Graphical User Interface (GUI)

A modern, responsive Tkinter desktop GUI that seamlessly reuses the verified
backend functionality, thread safety, and TTS fixes from voice_assistant.py.
"""

import os
import queue
import sys
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional

import speech_recognition as sr

# Reuse verified backend logic from voice_assistant.py
import voice_assistant


class VoiceAssistantGUI:
    """Tkinter Desktop GUI for OASIS Voice Assistant."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("OASIS Voice Assistant")
        self.root.geometry("850x680")
        self.root.minsize(750, 550)

        # Apply dark modern color palette
        self.bg_color = "#1e1e2e"          # Dark slate background
        self.card_bg = "#252538"           # Card container background
        self.text_color = "#cdd6f4"        # Main text color
        self.accent_blue = "#89b4fa"       # Primary blue accent
        self.accent_green = "#a6e3a1"      # Success / Assistant response
        self.accent_orange = "#fab387"     # Warning / User text
        self.accent_red = "#f38ba8"        # Error / Stop button
        self.accent_purple = "#cba6f7"     # Speaking state badge
        self.muted_text = "#a6adc8"        # Secondary text color

        self.root.configure(bg=self.bg_color)

        # Thread safety & state variables
        self.msg_queue: queue.Queue = queue.Queue()
        self.is_listening: bool = False
        self.listening_thread: Optional[threading.Thread] = None

        # Load custom commands
        self.custom_commands = voice_assistant.load_custom_commands()

        # Initialize speech recognition hardware
        self.recognizer = sr.Recognizer()
        try:
            self.mic = sr.Microphone()
            self.mic_status_str = "Microphone: Ready (Hardware Detected)"
        except Exception as e:
            self.mic = None
            self.mic_status_str = "Microphone: Unavailable (Fallback to Text Input)"
            print(f"[Warning] Microphone initialization failed: {e}")

        # Build GUI layout
        self._build_styles()
        self._build_header()
        self._build_conversation_area()
        self._build_input_area()
        self._build_control_panel()
        self._build_footer()

        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start periodic queue processor (runs on main thread every 100ms)
        self.root.after(100, self._process_queue)

        # Log initial welcome message
        self._append_system_msg("Voice Assistant GUI initialized.")
        self._append_assistant_msg("Hello! Voice Assistant is ready. Click 'Start Listening' or type a command below.")

    def _build_styles(self) -> None:
        """Configures custom ttk styles."""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background=self.bg_color, foreground=self.text_color)
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Card.TFrame", background=self.card_bg)

    def _build_header(self) -> None:
        """Builds top header banner with title and status badge."""
        header_frame = tk.Frame(self.root, bg=self.card_bg, pady=12, padx=20)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame,
            text="OASIS Voice Assistant",
            font=("Segoe UI", 18, "bold"),
            bg=self.card_bg,
            fg=self.accent_blue
        )
        title_label.pack(side=tk.LEFT)

        subtitle_label = tk.Label(
            header_frame,
            text=" | Phase 4 Desktop Edition",
            font=("Segoe UI", 11),
            bg=self.card_bg,
            fg=self.muted_text
        )
        subtitle_label.pack(side=tk.LEFT, padx=(4, 0), pady=(4, 0))

        # Status badge indicator
        self.status_label = tk.Label(
            header_frame,
            text="Status: Ready",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_green,
            fg="#11111b",
            padx=12,
            pady=4
        )
        self.status_label.pack(side=tk.RIGHT)

    def _build_conversation_area(self) -> None:
        """Builds scrollable conversation log view."""
        conv_frame = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=10)
        conv_frame.pack(fill=tk.BOTH, expand=True)

        lbl = tk.Label(conv_frame, text="Conversation History", font=("Segoe UI", 11, "bold"), bg=self.bg_color, fg=self.muted_text)
        lbl.pack(anchor="w", pady=5)

        self.chat_area = scrolledtext.ScrolledText(
            conv_frame,
            font=("Consolas", 10),
            bg=self.card_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            selectbackground=self.accent_blue,
            selectforeground="#11111b",
            wrap=tk.WORD,
            bd=0,
            padx=12,
            pady=12
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        # Configure text formatting tags
        self.chat_area.tag_config("user", foreground=self.accent_orange, font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("assistant", foreground=self.accent_green, font=("Segoe UI", 11, "bold"))
        self.chat_area.tag_config("system", foreground=self.muted_text, font=("Segoe UI", 9, "italic"))
        self.chat_area.tag_config("text_body", foreground=self.text_color, font=("Segoe UI", 10))

    def _build_input_area(self) -> None:
        """Builds manual text entry field and Send button for fallback input."""
        input_frame = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=5)
        input_frame.pack(fill=tk.X)

        self.entry_var = tk.StringVar()
        self.entry_field = tk.Entry(
            input_frame,
            textvariable=self.entry_var,
            font=("Segoe UI", 11),
            bg=self.card_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            bd=1,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.card_bg,
            highlightcolor=self.accent_blue
        )
        self.entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 10))
        self.entry_field.bind("<Return>", lambda event: self._on_send_text_command())

        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=("Segoe UI", 10, "bold"),
            bg=self.accent_blue,
            fg="#11111b",
            activebackground=self.accent_purple,
            activeforeground="#11111b",
            bd=0,
            padx=18,
            pady=6,
            command=self._on_send_text_command,
            cursor="hand2"
        )
        send_btn.pack(side=tk.RIGHT)

    def _build_control_panel(self) -> None:
        """Builds action buttons: Start Listening, Stop Assistant, Clear Conversation."""
        control_frame = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=10)
        control_frame.pack(fill=tk.X)

        self.start_btn = tk.Button(
            control_frame,
            text="🎙  Start Listening",
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_green,
            fg="#11111b",
            activebackground=self.accent_blue,
            activeforeground="#11111b",
            bd=0,
            padx=16,
            pady=8,
            command=self.start_listening,
            cursor="hand2"
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_btn = tk.Button(
            control_frame,
            text="⏹  Stop Assistant",
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_red,
            fg="#11111b",
            activebackground=self.accent_orange,
            activeforeground="#11111b",
            bd=0,
            padx=16,
            pady=8,
            command=self.stop_assistant,
            state=tk.NORMAL,
            cursor="hand2"
        )
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))

        clear_btn = tk.Button(
            control_frame,
            text="🗑  Clear Conversation",
            font=("Segoe UI", 10),
            bg=self.card_bg,
            fg=self.text_color,
            activebackground=self.muted_text,
            activeforeground="#11111b",
            bd=0,
            padx=14,
            pady=8,
            command=self.clear_conversation,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.RIGHT)

    def _build_footer(self) -> None:
        """Builds bottom status bar displaying microphone hardware status."""
        footer_frame = tk.Frame(self.root, bg=self.card_bg, pady=4, padx=15)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        mic_lbl = tk.Label(footer_frame, text=self.mic_status_str, font=("Segoe UI", 9), bg=self.card_bg, fg=self.muted_text)
        mic_lbl.pack(side=tk.LEFT)

        info_lbl = tk.Label(footer_frame, text="OASIS Infobyte Task 1", font=("Segoe UI", 9), bg=self.card_bg, fg=self.muted_text)
        info_lbl.pack(side=tk.RIGHT)

    # --- UI Logging Helper Methods ---

    def set_status(self, text: str, color_hex: str = "#a6e3a1") -> None:
        """Updates the status badge indicator label."""
        self.status_label.config(text=f"Status: {text}", bg=color_hex)

    def _append_user_msg(self, text: str) -> None:
        """Appends user query to conversation text area."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "\nYou: ", "user")
        self.chat_area.insert(tk.END, f"{text}\n", "text_body")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def _append_assistant_msg(self, text: str) -> None:
        """Appends assistant response to conversation text area."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "\nAssistant: ", "assistant")
        self.chat_area.insert(tk.END, f"{text}\n", "text_body")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def _append_system_msg(self, text: str) -> None:
        """Appends system notification to conversation text area."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"\n[System] {text}\n", "system")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def clear_conversation(self) -> None:
        """Clears all entries from the conversation text area."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.config(state=tk.DISABLED)
        self._append_system_msg("Conversation history cleared.")

    # --- Thread-Safe Event Queue Processing ---

    def _process_queue(self) -> None:
        """
        Periodically checks the thread-safe queue for messages posted from background threads.
        Executes widget updates strictly on the main Tkinter thread.
        """
        try:
            while True:
                msg_type, payload = self.msg_queue.get_nowait()
                if msg_type == "user_msg":
                    self._append_user_msg(payload)
                elif msg_type == "assistant_msg":
                    self._append_assistant_msg(payload)
                elif msg_type == "system_msg":
                    self._append_system_msg(payload)
                elif msg_type == "status":
                    status_str, color = payload
                    self.set_status(status_str, color)
                elif msg_type == "speak":
                    # Execute thread-safe speak call
                    voice_assistant.speak(payload)
                elif msg_type == "reset_buttons":
                    self.start_btn.config(state=tk.NORMAL)
        except queue.Empty:
            pass

        # Re-schedule queue check after 100ms
        self.root.after(100, self._process_queue)

    # --- Command Handling & Background Listening ---

    def _on_send_text_command(self) -> None:
        """Processes text command submitted from the entry field."""
        cmd = self.entry_var.get().strip()
        if not cmd:
            return

        self.entry_var.set("")
        self._append_user_msg(cmd)
        threading.Thread(target=self._process_command_thread, args=(cmd,), daemon=True).start()

    def _process_command_thread(self, command: str) -> None:
        """Processes command in a background thread to prevent UI freezing."""
        self.msg_queue.put(("status", ("Processing...", self.accent_orange)))

        # Process command using verified backend
        keep_running = voice_assistant.handle_command(
            command,
            custom_commands=self.custom_commands,
            recognizer=self.recognizer,
            mic=self.mic
        )

        if not keep_running:
            self.msg_queue.put(("status", ("Stopped", self.accent_red)))
            self.is_listening = False
            self.msg_queue.put(("reset_buttons", None))
        else:
            if not self.is_listening:
                self.msg_queue.put(("status", ("Ready", self.accent_green)))

    def start_listening(self) -> None:
        """Starts background microphone listening thread loop."""
        if self.is_listening:
            return

        if self.mic is None:
            messagebox.showwarning("Microphone Unavailable", "Microphone hardware was not detected. Please use the text entry field to type commands.")
            return

        self.is_listening = True
        self.start_btn.config(state=tk.DISABLED)
        self.set_status("Listening...", self.accent_blue)
        self._append_system_msg("Listening loop started. Speak into your microphone.")

        self.listening_thread = threading.Thread(target=self._listening_loop, daemon=True)
        self.listening_thread.start()

    def _listening_loop(self) -> None:
        """Continuous background listening loop."""
        while self.is_listening:
            self.msg_queue.put(("status", ("Listening...", self.accent_blue)))
            cmd = voice_assistant.listen(self.recognizer, self.mic)

            if not self.is_listening:
                break

            if cmd:
                self.msg_queue.put(("user_msg", cmd))
                self.msg_queue.put(("status", ("Processing...", self.accent_orange)))
                keep_running = voice_assistant.handle_command(
                    cmd,
                    custom_commands=self.custom_commands,
                    recognizer=self.recognizer,
                    mic=self.mic
                )

                if not keep_running:
                    self.is_listening = False
                    self.msg_queue.put(("status", ("Stopped", self.accent_red)))
                    self.msg_queue.put(("reset_buttons", None))
                    break

        if not self.is_listening:
            self.msg_queue.put(("status", ("Ready", self.accent_green)))
            self.msg_queue.put(("reset_buttons", None))

    def stop_assistant(self) -> None:
        """Stops microphone listening loop gracefully."""
        if self.is_listening:
            self.is_listening = False
            self.set_status("Stopped", self.accent_red)
            self._append_system_msg("Listening loop stopped.")
            self.start_btn.config(state=tk.NORMAL)
        else:
            self.set_status("Ready", self.accent_green)

    def on_closing(self) -> None:
        """Handles clean application shutdown on window close."""
        self.is_listening = False
        try:
            self.root.destroy()
        except Exception:
            pass
        sys.exit(0)


def main() -> None:
    """Entry point for running the Voice Assistant Desktop GUI."""
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
