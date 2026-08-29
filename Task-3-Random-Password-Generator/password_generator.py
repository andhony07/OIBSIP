import random
import string
from typing import List, Dict

def get_password_length() -> int:
    """Prompt user for password length (minimum 8)."""
    while True:
        user_input = input("Enter password length (minimum 8): ").strip()
        if not user_input.isdigit():
            print("Invalid input. Please enter a whole number.")
            continue
        length = int(user_input)
        if length < 8:
            print("Password length must be at least 8 characters.")
            continue
        return length

def get_character_types() -> Dict[int, str]:
    """Prompt user to select character types. Returns a dict mapping choice number to character set."""
    type_map = {
        1: string.ascii_uppercase,
        2: string.ascii_lowercase,
        3: string.digits,
        4: string.punctuation,
    }
    while True:
        print("\nSelect character types:")
        print("1. Uppercase letters")
        print("2. Lowercase letters")
        print("3. Numbers")
        print("4. Symbols")
        selections = input("Enter your choices separated by spaces (example: 1 2 3 4): ").strip()
        if not selections:
            print("You must select at least two character types.")
            continue
        parts = selections.split()
        try:
            choices = {int(p) for p in parts}
        except ValueError:
            print("Invalid selection. Please enter numbers 1-4 separated by spaces.")
            continue
        if any(c not in type_map for c in choices):
            print("Invalid selection. Choices must be between 1 and 4.")
            continue
        if len(choices) < 2:
            print("Select at least two character types.")
            continue
        return {c: type_map[c] for c in sorted(choices)}

def generate_password(length: int, selected_types: Dict[int, str]) -> str:
    """Generate a password of given length ensuring at least one of each selected type."""
    # Ensure each selected type appears at least once
    password_chars: List[str] = []
    for chars in selected_types.values():
        password_chars.append(random.choice(chars))
    # Fill the rest of the password
    all_allowed = "".join(selected_types.values())
    remaining = length - len(password_chars)
    if remaining > 0:
        password_chars.extend(random.choice(all_allowed) for _ in range(remaining))
    # Shuffle to avoid predictable placement
    random.shuffle(password_chars)
    return "".join(password_chars)

def prompt_yes_no(message: str) -> bool:
    """Prompt user with a yes/no question, returning True for yes."""
    while True:
        answer = input(message).strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please answer with 'y' or 'n'.")

def main() -> None:
    print("=" * 40)
    print("   Random Password Generator – Beginner Tier")
    print("=" * 40)
    while True:
        length = get_password_length()
        selected = get_character_types()
        password = generate_password(length, selected)
        print(f"\nGenerated Password: {password}\n")
        if not prompt_yes_no("Generate another password? (y/n): "):
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
