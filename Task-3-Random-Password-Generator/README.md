# Random Password Generator

A Python-based **Random Password Generator** developed as **Task 3 of the OASIS Infobyte Python Programming Internship**.

The project started as a command-line password generator and was extended into a graphical application with configurable password generation, strength analysis, clipboard support, ambiguous-character exclusion, and session history.

---

## Project Overview

The Random Password Generator creates strong, customizable passwords based on the user's selected requirements.

The project was developed in multiple phases:

### Phase 1 — Command-Line Version

The initial version provides:

- Password length selection
- Character-set selection
- Random password generation
- Customizable password composition

### Phase 2 — Advanced GUI Version

The application was extended with a Tkinter-based graphical interface providing:

- Password length control
- Uppercase character selection
- Lowercase character selection
- Digit selection
- Special character selection
- Secure password generation
- Password strength indication
- Ambiguous-character exclusion
- Clipboard support
- Recent password history

### Phase 3 — Testing & Quality Assurance

The final phase focused on:

- GUI logic testing
- GUI runtime testing
- Feature verification
- Regression testing
- Documentation
- Submission preparation

---

## Features

### Password Generation

Generate customizable passwords based on:

- Password length
- Uppercase letters
- Lowercase letters
- Numbers
- Special characters

The generator uses Python's `secrets` module for password generation.

### Password Strength

The GUI provides a password strength indicator based on the generated password characteristics.

### Ambiguous Character Exclusion

The application can exclude visually confusing characters when generating passwords.

This can be useful when passwords need to be manually read or entered.

### Clipboard Support

Generated passwords can be copied directly to the system clipboard from the GUI.

### Password History

The application maintains a limited session history of recently generated passwords.

### Graphical User Interface

The advanced version provides a Tkinter GUI for configuring and generating passwords without using the command line.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Tkinter | Graphical user interface |
| `secrets` | Secure random password generation |
| `string` | Character-set handling |
| Pyperclip | Clipboard integration |
| unittest | Automated testing |

---

## Project Structure

```text
Task-3-Random-Password-Generator/
│
├── password_generator.py
│   # Command-line password generator
│
├── password_generator_gui.py
│   # Tkinter graphical password generator
│
├── implementation_report.md
│   # Implementation and verification report
│
├── requirements.txt
│   # Python dependencies
│
├── test_gui_logic.py
│   # GUI logic tests
│
├── test_gui_runtime.py
│   # GUI runtime tests
│
└── README.md
    # Project documentation