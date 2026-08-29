import string
import secrets
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

# Constants for character sets
UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
DIGITS = string.digits
SYMBOLS = string.punctuation

# Ambiguous characters to exclude when option is enabled
AMBIGUOUS = {
    '0', 'O', 'o', '1', 'l', 'I', '|', '5', 'S', '2', 'Z'
}

def filter_ambiguous(chars: str) -> str:
    """Remove ambiguous characters from a character string."""
    return ''.join(ch for ch in chars if ch not in AMBIGUOUS)

def build_char_pool(selections: dict, exclude_ambiguous: bool) -> dict:
    """Return a dict mapping selection name to its character pool string.
    selections: dict with keys 'uppercase', 'lowercase', 'digits', 'symbols' set to bool.
    """
    pool = {}
    if selections.get('uppercase'):
        chars = UPPERCASE
        if exclude_ambiguous:
            chars = filter_ambiguous(chars)
        pool['uppercase'] = chars
    if selections.get('lowercase'):
        chars = LOWERCASE
        if exclude_ambiguous:
            chars = filter_ambiguous(chars)
        pool['lowercase'] = chars
    if selections.get('digits'):
        chars = DIGITS
        if exclude_ambiguous:
            chars = filter_ambiguous(chars)
        pool['digits'] = chars
    if selections.get('symbols'):
        chars = SYMBOLS
        if exclude_ambiguous:
            chars = filter_ambiguous(chars)
        pool['symbols'] = chars
    return pool

def generate_password(length: int, char_pool: dict) -> str:
    """Generate a password of given length guaranteeing at least one character from each selected type.
    char_pool: dict mapping type name to string of allowed characters.
    """
    # Ensure each selected type contributes at least one character
    password_chars = []
    for chars in char_pool.values():
        if not chars:
            raise ValueError("Character pool for a selected type became empty after ambiguous exclusion.")
        password_chars.append(secrets.choice(chars))
    # Fill the rest using the combined pool
    all_allowed = ''.join(char_pool.values())
    remaining = length - len(password_chars)
    for _ in range(remaining):
        password_chars.append(secrets.choice(all_allowed))
    # Shuffle securely using SystemRandom
    sysrand = secrets.SystemRandom()
    sysrand.shuffle(password_chars)
    return ''.join(password_chars)

def assess_strength(password: str, selections: dict) -> str:
    """Simple strength assessment based on length and variety of character types used."""
    length_score = len(password) // 8  # 1 point per 8 chars
    variety_score = sum(selections.values())  # number of selected types
    score = length_score + variety_score
    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"

class PasswordGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Random Password Generator – Advanced Tier")
        master.resizable(False, False)
        self.history = []  # Store last 5 passwords
        # Password length control
        length_frame = ttk.LabelFrame(master, text="Password Length")
        length_frame.grid(column=0, row=0, padx=10, pady=5, sticky="ew")
        self.length_var = tk.IntVar(value=12)
        self.length_spin = ttk.Spinbox(length_frame, from_=8, to=64, textvariable=self.length_var, width=5, command=self.update_length_label)
        self.length_spin.grid(column=0, row=0, padx=5, pady=5)
        self.length_label = ttk.Label(length_frame, text=f"Length: {self.length_var.get()}")
        self.length_label.grid(column=1, row=0, padx=5, pady=5)
        # Character type checkboxes
        charset_frame = ttk.LabelFrame(master, text="Character Types")
        charset_frame.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=False)
        self.symbols_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(charset_frame, text="Uppercase Letters", variable=self.upper_var).grid(column=0, row=0, sticky="w")
        ttk.Checkbutton(charset_frame, text="Lowercase Letters", variable=self.lower_var).grid(column=0, row=1, sticky="w")
        ttk.Checkbutton(charset_frame, text="Numbers", variable=self.digits_var).grid(column=0, row=2, sticky="w")
        ttk.Checkbutton(charset_frame, text="Symbols", variable=self.symbols_var).grid(column=0, row=3, sticky="w")
        # Ambiguous exclusion checkbox
        self.exclude_ambiguous_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(master, text="Exclude ambiguous characters", variable=self.exclude_ambiguous_var).grid(column=0, row=2, padx=10, pady=5, sticky="w")
        # Generate button
        self.generate_button = ttk.Button(master, text="Generate Password", command=self.on_generate)
        self.generate_button.grid(column=0, row=3, padx=10, pady=5, sticky="ew")
        # Password display and copy button
        pwd_frame = ttk.Frame(master)
        pwd_frame.grid(column=0, row=4, padx=10, pady=5, sticky="ew")
        ttk.Label(pwd_frame, text="Generated Password:").grid(column=0, row=0, sticky="w")
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(pwd_frame, textvariable=self.password_var, width=30, state="readonly")
        self.password_entry.grid(column=1, row=0, sticky="e")
        self.copy_button = ttk.Button(pwd_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(column=2, row=0, padx=5)
        # Strength indicator
        strength_frame = ttk.Frame(master)
        strength_frame.grid(column=0, row=5, padx=10, pady=5, sticky="ew")
        ttk.Label(strength_frame, text="Strength:").grid(column=0, row=0, sticky="w")
        self.strength_var = tk.StringVar(value="")
        self.strength_label = ttk.Label(strength_frame, textvariable=self.strength_var, foreground="blue")
        self.strength_label.grid(column=1, row=0, sticky="w")
        # History listbox
        history_frame = ttk.LabelFrame(master, text="Last 5 Passwords (Session)")
        history_frame.grid(column=0, row=6, padx=10, pady=5, sticky="ew")
        self.history_listbox = tk.Listbox(history_frame, height=5, width=45)
        self.history_listbox.pack(padx=5, pady=5)
        self.update_history_display(initial=True)

    def update_length_label(self):
        self.length_label.config(text=f"Length: {self.length_var.get()}")

    def get_selections(self) -> dict:
        return {
            'uppercase': self.upper_var.get(),
            'lowercase': self.lower_var.get(),
            'digits': self.digits_var.get(),
            'symbols': self.symbols_var.get()
        }

    def validate(self, length: int, selections: dict) -> bool:
        if length < 8:
            messagebox.showerror("Invalid Length", "Password length must be at least 8.")
            return False
        if sum(selections.values()) < 2:
            messagebox.showerror("Selection Error", "Select at least two character types.")
            return False
        pool = build_char_pool(selections, self.exclude_ambiguous_var.get())
        for typ, chars in pool.items():
            if not chars:
                messagebox.showerror("Character Set Empty", f"After excluding ambiguous characters, the set for {typ} became empty.")
                return False
        return True

    def on_generate(self):
        length = self.length_var.get()
        selections = self.get_selections()
        if not self.validate(length, selections):
            return
        try:
            char_pool = build_char_pool(selections, self.exclude_ambiguous_var.get())
            pwd = generate_password(length, char_pool)
        except Exception as e:
            messagebox.showerror("Generation Error", str(e))
            return
        self.password_var.set(pwd)
        self.strength_var.set(assess_strength(pwd, selections))
        # Automatic clipboard copy
        try:
            pyperclip.copy(pwd)
        except Exception as e:
            messagebox.showwarning("Clipboard Error", f"Failed to copy to clipboard: {e}")
        # Update history
        self.history.insert(0, pwd)
        if len(self.history) > 5:
            self.history = self.history[:5]
        self.update_history_display()

    def copy_to_clipboard(self):
        pwd = self.password_var.get()
        if not pwd:
            messagebox.showinfo("No Password", "Generate a password first.")
            return
        try:
            pyperclip.copy(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard.")
        except Exception as e:
            messagebox.showerror("Clipboard Error", str(e))

    def update_history_display(self, initial=False):
        self.history_listbox.delete(0, tk.END)
        if not self.history:
            self.history_listbox.insert(tk.END, "No passwords generated yet.")
        else:
            for pwd in self.history:
                self.history_listbox.insert(tk.END, pwd)

def main():
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
