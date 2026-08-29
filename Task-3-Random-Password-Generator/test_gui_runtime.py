import pyperclip
import tkinter as tk
import password_generator_gui as gui

def run_tests():
    # Test normal generation
    selections = {'uppercase': True, 'lowercase': True, 'digits': False, 'symbols': False}
    pool = gui.build_char_pool(selections, exclude_ambiguous=False)
    pwd = gui.generate_password(12, pool)
    print('Generated password:', pwd)
    # Clipboard copy and verify
    pyperclip.copy(pwd)
    retrieved = pyperclip.paste()
    print('Clipboard match:', retrieved == pwd)
    # Strength assessment
    strength = gui.assess_strength(pwd, selections)
    print('Strength:', strength)
    # Ambiguous exclusion test
    selections_all = {'uppercase': True, 'lowercase': True, 'digits': True, 'symbols': True}
    pool_excl = gui.build_char_pool(selections_all, exclude_ambiguous=True)
    pwd2 = gui.generate_password(16, pool_excl)
    print('Generated with ambiguous exclusion:', pwd2)
    # Verify no ambiguous chars
    ambiguous = set('0O1l')
    has_ambiguous = any(c in ambiguous for c in pwd2)
    print('No ambiguous chars:', not has_ambiguous)
    # History simulation (manual)
    app = gui.PasswordGeneratorGUI(tk.Tk())
    # simulate adding passwords to history
    for i in range(6):
        app.history.insert(0, f'pwd{i}')
        if len(app.history) > 5:
            app.history = app.history[:5]
    print('History length (should be 5):', len(app.history))
    print('History entries:', app.history)

if __name__ == '__main__':
    run_tests()
