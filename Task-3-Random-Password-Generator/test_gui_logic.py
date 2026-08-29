import importlib.util, pathlib, sys

# Load the GUI module
module_path = pathlib.Path('password_generator_gui.py').resolve()
spec = importlib.util.spec_from_file_location('gui_module', module_path)
gui = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gui)

def test_generate(length, selections, exclude=False):
    pool = gui.build_char_pool(selections, exclude)
    pwd = gui.generate_password(length, pool)
    # Checks
    if len(pwd) != length:
        print('FAIL: length mismatch')
        return False
    # Ensure each selected type present
    for typ, chars in pool.items():
        if not any(c in chars for c in pwd):
            print(f'FAIL: missing type {typ}')
            return False
    # Ensure no chars outside pool
    allowed = set(''.join(pool.values()))
    if any(c not in allowed for c in pwd):
        print('FAIL: contains disallowed character')
        return False
    return True

# Test cases
all_pass = True
# 1. Minimum length, uppercase+lowercase
sel1 = {'uppercase': True, 'lowercase': True, 'digits': False, 'symbols': False}
all_pass &= test_generate(8, sel1)
# 2. All types, length 12
sel2 = {'uppercase': True, 'lowercase': True, 'digits': True, 'symbols': True}
all_pass &= test_generate(12, sel2)
# 3. Uppercase + digits, length 10
sel3 = {'uppercase': True, 'lowercase': False, 'digits': True, 'symbols': False}
all_pass &= test_generate(10, sel3)
# 4. Ambiguous exclusion enabled, all types, length 12
all_pass &= test_generate(12, sel2, exclude=True)
print('ALL PASS' if all_pass else 'SOME FAIL')
