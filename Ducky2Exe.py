# Version: 1.1, thanks all for using my code!
# Changes? Icon, some optimizations, more keys and a more pretty interface
# If I miss any keys make issue with it please

import os
import subprocess
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

class Ducky2ExeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ducky2Python Converter")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icon.png")) # You can change the icon to your own

        # Create widgets
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Paste DuckyScript here")

        self.text_output = QTextEdit(self)
        self.text_output.setPlaceholderText("Generated Python script will appear here")
        self.text_output.setReadOnly(True)

        self.convert_button = QPushButton("Convert to Python", self)
        self.convert_button.clicked.connect(self.convert_to_python)

        self.download_button = QPushButton("Download exe", self)
        self.download_button.clicked.connect(self.download_exe)

        self.status_label = QLabel("Status: Ready", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("DuckyScript Input:"))
        input_layout.addWidget(self.text_input)

        output_layout = QVBoxLayout()
        output_layout.addWidget(QLabel("Python Script Output:"))
        output_layout.addWidget(self.text_output)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.download_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def convert_to_python(self):
        # Get the DuckyScript from the input text area
        ducky_script = self.get_ducky_script()
        if not ducky_script:
            return

        # Update the status label to indicate conversion is in progress
        self.status_label.setText("Status: Converting...")

        # Parse the DuckyScript and convert it to a Python script
        python_script = self.parse_ducky_script(ducky_script)

        # Display the generated Python script in the output text area
        self.display_python_script(python_script)

        # Update the status label to indicate the conversion is complete
        self.status_label.setText("Status: Python script generated")

    def get_ducky_script(self):
        ducky_script = self.text_input.toPlainText()
        if not ducky_script.strip():
            self.status_label.setText("Status: Please enter DuckyScript")
            return None
        return ducky_script

    def display_python_script(self, python_script):
        self.text_output.setPlainText(python_script)

    def parse_ducky_script(self, ducky_script):
        # This is the parser for DuckyScript. Example adapted from .js
        python_script = "# Converted DuckyScript to Python using ducky2python!\n"
        python_script += "import pyautogui\n"
        python_script += "import time\n"
        python_script += "import random\n"
        python_script += "import string\n"
        python_script += "import keyboard\n"  # For lock key states
        
        # Add minimum delay check
        def validate_delay(delay_ms):
            return max(20, int(delay_ms))

        # Add variable tracking
        variables = {}
        functions = {}
        current_indent = 0
        
        def get_indent():
            return "    " * current_indent

        def handle_variable(var_line):
            # Extract variable name and value
            parts = var_line.split("=", 1)
            if len(parts) != 2:
                return f"# Invalid variable declaration: {var_line}"
            var_name = parts[0].strip().replace("$", "_var_")
            var_value = parts[1].strip()
            variables[var_name] = var_value
            return f"{var_name} = {var_value}"

        def replace_variables(text):
            # Replace $variables with their Python equivalents
            for var in variables:
                text = text.replace(f"${var[5:]}", var)
            return text

        # Add internal variables
        internal_vars = {
            "_JITTER_ENABLED": False,
            "_JITTER_MAX": 20,
            "_CAPSLOCK_ON": "keyboard.is_pressed('caps lock')",
            "_NUMLOCK_ON": "keyboard.is_pressed('num lock')",
            "_SCROLLLOCK_ON": "keyboard.is_pressed('scroll lock')",
            "_BUTTON_ENABLED": True,
            "_BUTTON_TIMEOUT": 1000,
            "_EXFIL_MODE_ENABLED": False,
        }

        # Add jitter functionality
        def add_jitter():
            if internal_vars["_JITTER_ENABLED"]:
                return f"time.sleep(random.uniform(0, {internal_vars['_JITTER_MAX']}/1000))"
            return ""

        # Split DuckyScript into lines and remove extra spaces
        lines = ducky_script.splitlines()
        default_delay = 0
        commands = []

        # First line might be DEFAULT for default delay
        if lines[0].startswith("DEFAULT"):
            default_delay = int(lines[0][7:].strip()) / 1000  # In Python time is in seconds
            lines = lines[1:]  # Remove first line with DEFAULT

        # Dictionary for translating DuckyScript commands to pyautogui
        ducky_to_pyautogui = {
            "ALT": "alt",                  # ALT key
            "CTRL": "ctrl",                # CTRL key
            "SHIFT": "shift",              # SHIFT key
            "GUI": "win",                  # Windows key
            "WINDOWS": "win",              # Windows key
            "ENTER": "enter",              # Enter key
            "MENU": "menu",                # Menu key
            "APP": "menu",                 # Menu key
            "DELETE": "delete",            # Delete key
            "HOME": "home",                # Home key
            "INSERT": "insert",            # Insert key
            "PAGEUP": "pageup",            # Page Up key
            "PAGEDOWN": "pagedown",        # Page Down key
            "UP": "up",                    # Up arrow key
            "DOWN": "down",                # Down arrow key
            "LEFT": "left",                # Left arrow key
            "RIGHT": "right",              # Right arrow key
            "TAB": "tab",                  # Tab key
            "ESC": "esc",                  # Escape key
            "ESCAPE": "esc",               # Escape key
            "BACKSPACE": "backspace",      # Backspace key
            "CAPSLOCK": "capslock",        # Caps Lock key
            "NUMLOCK": "numlock",          # Num Lock key
            "PRINTSCREEN": "printscreen",  # Print Screen key
            "SCROLLLOCK": "scrolllock",    # Scroll Lock key
            "PAUSE": "pause",              # Pause key
            "BREAK": "pause",              # Pause key
            "F1": "f1",                    # F1 key
            "F2": "f2",                    # F2 key
            "F3": "f3",                    # F3 key
            "F4": "f4",                    # F4 key
            "F5": "f5",                    # F5 key
            "F6": "f6",                    # F6 key
            "F7": "f7",                    # F7 key
            "F8": "f8",                    # F8 key
            "F9": "f9",                    # F9 key
            "F10": "f10",                  # F10 key
            "F11": "f11",                  # F11 key
            "F12": "f12",                  # F12 key
            "SPACE": "space",              # Space key
            "END": "end",                  # End key
            "VOLUMEUP": "volumeup",        # Volume Up key
            "VOLUMEDOWN": "volumedown",    # Volume Down key
            "VOLUMEMUTE": "volumemute",    # Volume Mute key
            "MEDIAPLAY": "playpause",      # Media Play/Pause key
            "MEDIANEXT": "nexttrack",      # Media Next Track
            "MEDIAPREV": "prevtrack",      # Media Previous Track
            "SLEEP": "sleep",              # Sleep key
            "LEFTALT": "altleft",          # Left Alt key
            "RIGHTALT": "altright",        # Right Alt key
            "LEFTCTRL": "ctrlleft",        # Left Control key
            "RIGHTCTRL": "ctrlright",      # Right Control key
            "LEFTSHIFT": "shiftleft",      # Left Shift key
            "RIGHTSHIFT": "shiftright",    # Right Shift key
            "GUI r": "win+r",              # Windows key + r
            "GUI e": "win+e",              # Windows key + e
            "GUI d": "win+d",              # Windows key + d
            "GUI l": "win+l",              # Windows key + l
            "GUI m": "win+m",              # Windows key + m
            "GUI p": "win+p",              # Windows key + p
            "GUI x": "win+x",              # Windows key + x
            "REM_BLOCK": "REM_BLOCK",      # Start of comment block
            "END_REM": "END_REM",          # End of comment block
            "STRINGLN": "STRINGLN",        # String with newline
            "END_STRING": "END_STRING",    # End of STRING block
            "END_STRINGLN": "END_STRINGLN",# End of STRINGLN block
            "INJECT_MOD": "INJECT_MOD",    # Inject modifier key alone
            "CAPSLOCK": "capslock",        # Caps Lock key
            "NUMLOCK": "numlock",          # Num Lock key
            "SCROLLLOCK": "scrolllock",    # Scroll Lock key
            "WAIT_FOR_BUTTON_PRESS": "WAIT_FOR_BUTTON_PRESS",  # Wait for button press
            "BUTTON_DEF": "BUTTON_DEF",    # Define button function
            "END_BUTTON": "END_BUTTON",    # End button function definition
            "DISABLE_BUTTON": "DISABLE_BUTTON",  # Disable button
            "ENABLE_BUTTON": "ENABLE_BUTTON",    # Enable button
            "LED_OFF": "LED_OFF",          # Turn off LED
            "LED_R": "LED_R",              # Turn on red LED
            "LED_G": "LED_G",              # Turn on green LED
            "ATTACKMODE": "ATTACKMODE",    # Set attack mode
            "SAVE_ATTACKMODE": "SAVE_ATTACKMODE",  # Save attack mode
            "RESTORE_ATTACKMODE": "RESTORE_ATTACKMODE",  # Restore attack mode
            "DEFINE": "DEFINE",            # Define a constant
            "VAR": "VAR",                  # Define a variable
            "IF": "IF",                    # If statement
            "ELSE": "ELSE",                # Else statement
            "END_IF": "END_IF",            # End if statement
            "WHILE": "WHILE",              # While loop
            "END_WHILE": "END_WHILE",      # End while loop
            "FUNCTION": "FUNCTION",        # Define a function
            "END_FUNCTION": "END_FUNCTION",# End function definition
            "RETURN": "RETURN",            # Return from function
            "RANDOM_LOWERCASE_LETTER": "RANDOM_LOWERCASE_LETTER",  # Random lowercase letter
            "RANDOM_UPPERCASE_LETTER": "RANDOM_UPPERCASE_LETTER",  # Random uppercase letter
            "RANDOM_LETTER": "RANDOM_LETTER",  # Random letter
            "RANDOM_NUMBER": "RANDOM_NUMBER",  # Random number
            "RANDOM_SPECIAL": "RANDOM_SPECIAL",  # Random special character
            "RANDOM_CHAR": "RANDOM_CHAR",  # Random character
            "RESTART_PAYLOAD": "RESTART_PAYLOAD",  # Restart payload
            "STOP_PAYLOAD": "STOP_PAYLOAD",  # Stop payload
            "RESET": "RESET",              # Reset keystroke buffer
            "HOLD": "HOLD",                # Hold key
            "RELEASE": "RELEASE",          # Release key
            "HIDE_PAYLOAD": "HIDE_PAYLOAD",  # Hide payload
            "RESTORE_PAYLOAD": "RESTORE_PAYLOAD",  # Restore payload
            "WAIT_FOR_CAPS_ON": "WAIT_FOR_CAPS_ON",  # Wait for caps lock on
            "WAIT_FOR_CAPS_OFF": "WAIT_FOR_CAPS_OFF",  # Wait for caps lock off
            "WAIT_FOR_CAPS_CHANGE": "WAIT_FOR_CAPS_CHANGE",  # Wait for caps lock change
            "WAIT_FOR_NUM_ON": "WAIT_FOR_NUM_ON",  # Wait for num lock on
            "WAIT_FOR_NUM_OFF": "WAIT_FOR_NUM_OFF",  # Wait for num lock off
            "WAIT_FOR_NUM_CHANGE": "WAIT_FOR_NUM_CHANGE",  # Wait for num lock change
            "WAIT_FOR_SCROLL_ON": "WAIT_FOR_SCROLL_ON",  # Wait for scroll lock on
            "WAIT_FOR_SCROLL_OFF": "WAIT_FOR_SCROLL_OFF",  # Wait for scroll lock off
            "WAIT_FOR_SCROLL_CHANGE": "WAIT_FOR_SCROLL_CHANGE",  # Wait for scroll lock change
            "SAVE_HOST_KEYBOARD_LOCK_STATE": "SAVE_HOST_KEYBOARD_LOCK_STATE",  # Save lock state
            "RESTORE_HOST_KEYBOARD_LOCK_STATE": "RESTORE_HOST_KEYBOARD_LOCK_STATE",  # Restore lock state
            "EXFIL": "EXFIL",              # Exfiltrate data
            "UPARROW": "up",               # Up arrow key
            "DOWNARROW": "down",           # Down arrow key
            "LEFTARROW": "left",           # Left arrow key
            "RIGHTARROW": "right",         # Right arrow key
            "DEL": "delete",               # Delete key
            "COMMAND": "command",          # Command key (Mac)
            "CONTROL": "ctrl",             # Control key
            "OPTION": "option",            # Option key (Mac)
            "CTRL SHIFT": "ctrl+shift",    # Control + Shift
            "ALT SHIFT": "alt+shift",      # Alt + Shift
            "COMMAND CTRL": "command+ctrl",  # Command + Control
            "COMMAND CTRL SHIFT": "command+ctrl+shift",  # Command + Control + Shift
            "COMMAND OPTION": "command+option",  # Command + Option
            "COMMAND OPTION SHIFT": "command+option+shift",  # Command + Option + Shift
            "CONTROL ALT DELETE": "ctrl+alt+delete"  # Control + Alt + Delete
        }

        in_comment_block = False
        in_string_block = False
        in_stringln_block = False

        # Process each line in DuckyScript
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Convert commands to Python
            if line.startswith("REM"):
                # Convert comments
                commands.append(f"# {line[4:]}")
            elif line.startswith("REM_BLOCK"):
                in_comment_block = True
                commands.append("# " + line[10:].strip())
            elif line.startswith("END_REM"):
                in_comment_block = False
            elif in_comment_block:
                commands.append("# " + line)
            elif line.startswith("DELAY"):
                # Convert delays with minimum validation
                try:
                    delay_time = validate_delay(int(line[6:].strip())) / 1000
                    commands.append(f"time.sleep({delay_time})")
                except ValueError:
                    # Try to handle variable delay
                    var_name = line[6:].strip()
                    if var_name.startswith('$'):
                        commands.append(f"time.sleep(max(0.02, {var_name.replace('$', '_var_')}/1000))")
                    else:
                        commands.append(f"# Invalid delay value: {line[6:].strip()}")
            elif line.startswith("STRINGLN"):
                text = line[9:].strip()
                commands.append(f"pyautogui.typewrite('{text}', interval=0.02)")
                commands.append("pyautogui.press('enter')")
            elif line.startswith("STRING"):
                in_string_block = True
                text = line[7:].strip()
                commands.append(f"pyautogui.typewrite('{text}', interval=0.02)")
            elif line.startswith("END_STRING"):
                in_string_block = False
            elif in_string_block:
                text = line.strip()
                commands.append(f"pyautogui.typewrite('{text}', interval=0.02)")
            elif line.startswith("STRINGLN"):
                in_stringln_block = True
                text = line[9:].strip()
                commands.append(f"pyautogui.typewrite('{text}', interval=0.02)")
                commands.append("pyautogui.press('enter')")
            elif line.startswith("END_STRINGLN"):
                in_stringln_block = False
            elif in_stringln_block:
                text = line.strip()
                commands.append(f"pyautogui.typewrite('{text}', interval=0.02)")
                commands.append("pyautogui.press('enter')")
            elif line.startswith("REPEAT"):
                # Convert repetitions
                repetitions = int(line[7:].strip())
                commands.append(f"# Repeat {repetitions} times")
                if commands:
                    last_command = commands[-1]
                    for _ in range(repetitions):
                        commands.append(last_command)  # Repeat last command
            elif line.startswith("INJECT_MOD"):
                # Inject modifier key alone
                key = line[11:].strip()
                pyautogui_key = ducky_to_pyautogui.get(key)
                if pyautogui_key:
                    commands.append(f"pyautogui.keyDown('{pyautogui_key}')")
                    commands.append(f"pyautogui.keyUp('{pyautogui_key}')")
                else:
                    commands.append(f"# Unrecognized key: {key}")
            elif line.startswith("CAPSLOCK"):
                # Caps Lock key
                commands.append("pyautogui.press('capslock')")
            elif line.startswith("NUMLOCK"):
                # Num Lock key
                commands.append("pyautogui.press('numlock')")
            elif line.startswith("SCROLLLOCK"):
                # Scroll Lock key
                commands.append("pyautogui.press('scrolllock')")
            elif line.startswith("HOLD"):
                # Hold key
                key = line[5:].strip()
                pyautogui_key = ducky_to_pyautogui.get(key)
                if pyautogui_key:
                    commands.append(f"{get_indent()}pyautogui.keyDown('{pyautogui_key}')")
                else:
                    commands.append(f"# Unrecognized key: {key}")
            elif line.startswith("RELEASE"):
                # Release key
                key = line[8:].strip()
                pyautogui_key = ducky_to_pyautogui.get(key)
                if pyautogui_key:
                    commands.append(f"{get_indent()}pyautogui.keyUp('{pyautogui_key}')")
                else:
                    commands.append(f"# Unrecognized key: {key}")
            elif line.startswith("WAIT_FOR_BUTTON_PRESS"):
                # Wait for button press
                commands.append("# Wait for button press")
            elif line.startswith("BUTTON_DEF"):
                # Define button function
                commands.append("# Define button function")
            elif line.startswith("END_BUTTON"):
                # End button function definition
                commands.append("# End button function definition")
            elif line.startswith("DISABLE_BUTTON"):
                # Disable button
                commands.append("# Disable button")
            elif line.startswith("ENABLE_BUTTON"):
                # Enable button
                commands.append("# Enable button")
            elif line.startswith("LED_OFF"):
                # Turn off LED
                commands.append("# Turn off LED")
            elif line.startswith("LED_R"):
                # Turn on red LED
                commands.append("# Turn on red LED")
            elif line.startswith("LED_G"):
                # Turn on green LED
                commands.append("# Turn on green LED")
            elif line.startswith("ATTACKMODE"):
                # Set attack mode
                mode = line[11:].strip()
                commands.append(f"# Set attack mode to {mode}")
            elif line.startswith("SAVE_ATTACKMODE"):
                # Save attack mode
                commands.append("# Save attack mode")
            elif line.startswith("RESTORE_ATTACKMODE"):
                # Restore attack mode
                commands.append("# Restore attack mode")
            elif line.startswith("DEFINE"):
                # Define a constant
                definition = line[7:].strip()
                commands.append(f"# Define constant: {definition}")
            elif line.startswith("VAR"):
                commands.append(get_indent() + handle_variable(line[4:]))
            elif line.startswith("IF"):
                condition = line[3:].strip()
                if condition.endswith("THEN"):
                    condition = condition[:-4].strip()
                condition = replace_variables(condition)
                commands.append(f"{get_indent()}if {condition}:")
                current_indent += 1
            elif line.startswith("ELSE"):
                current_indent -= 1
                if line[4:].strip().startswith("IF"):
                    condition = line[7:].strip()
                    if condition.endswith("THEN"):
                        condition = condition[:-4].strip()
                    condition = replace_variables(condition)
                    commands.append(f"{get_indent()}elif {condition}:")
                else:
                    commands.append(f"{get_indent()}else:")
                current_indent += 1
            elif line.startswith("END_IF"):
                current_indent -= 1
            elif line.startswith("WHILE"):
                condition = line[6:].strip()
                condition = replace_variables(condition)
                commands.append(f"{get_indent()}while {condition}:")
                current_indent += 1
            elif line.startswith("END_WHILE"):
                current_indent -= 1
            elif line.startswith("FUNCTION"):
                func_name = line[9:].strip().split("(")[0]
                commands.append(f"{get_indent()}def {func_name}():")
                functions[func_name] = True
                current_indent += 1
            elif line.startswith("END_FUNCTION"):
                current_indent -= 1
            elif line.startswith("RETURN"):
                value = line[7:].strip()
                value = replace_variables(value)
                commands.append(f"{get_indent()}return {value}")
            elif line.endswith("()") and line.strip()[:-2] in functions:
                # Function call
                commands.append(f"{get_indent()}{line}")
            elif line.startswith("RANDOM_LOWERCASE_LETTER"):
                commands.append(f"{get_indent()}pyautogui.typewrite(random.choice(string.ascii_lowercase))")
            elif line.startswith("RANDOM_UPPERCASE_LETTER"):
                commands.append(f"{get_indent()}pyautogui.typewrite(random.choice(string.ascii_uppercase))")
            elif line.startswith("RANDOM_LETTER"):
                commands.append(f"{get_indent()}pyautogui.typewrite(random.choice(string.ascii_letters))")
            elif line.startswith("RANDOM_NUMBER"):
                commands.append(f"{get_indent()}pyautogui.typewrite(random.choice(string.digits))")
            elif line.startswith("RANDOM_SPECIAL"):
                commands.append(f"{get_indent()}pyautogui.typewrite(random.choice('!@#$%^&*()'))")
            elif line.startswith("RANDOM_CHAR"):
                commands.append(f"{get_indent()}pyautogui.typewrite(random.choice(string.ascii_letters + string.digits + '!@#$%^&*()'))")
            elif line.startswith("RESTART_PAYLOAD"):
                # Restart payload
                commands.append("# Restart payload")
            elif line.startswith("STOP_PAYLOAD"):
                # Stop payload
                commands.append("# Stop payload")
            elif line.startswith("RESET"):
                # Reset keystroke buffer
                commands.append("# Reset keystroke buffer")
            elif line.startswith("HIDE_PAYLOAD"):
                # Hide payload
                commands.append("# Hide payload")
            elif line.startswith("RESTORE_PAYLOAD"):
                # Restore payload
                commands.append("# Restore payload")
            elif line.startswith("WAIT_FOR_CAPS_ON"):
                commands.append(f"{get_indent()}while not keyboard.is_pressed('caps lock'): time.sleep(0.1)")
            elif line.startswith("WAIT_FOR_CAPS_OFF"):
                commands.append(f"{get_indent()}while keyboard.is_pressed('caps lock'): time.sleep(0.1)")
            elif line.startswith("WAIT_FOR_CAPS_CHANGE"):
                commands.append(f"{get_indent()}initial_state = keyboard.is_pressed('caps lock')")
                commands.append(f"{get_indent()}while keyboard.is_pressed('caps lock') == initial_state: time.sleep(0.1)")
            elif line.startswith("WAIT_FOR_NUM_ON"):
                commands.append(f"{get_indent()}while not keyboard.is_pressed('num lock'): time.sleep(0.1)")
            elif line.startswith("WAIT_FOR_NUM_OFF"):
                commands.append(f"{get_indent()}while keyboard.is_pressed('num lock'): time.sleep(0.1)")
            elif line.startswith("WAIT_FOR_NUM_CHANGE"):
                commands.append(f"{get_indent()}initial_state = keyboard.is_pressed('num lock')")
                commands.append(f"{get_indent()}while keyboard.is_pressed('num lock') == initial_state: time.sleep(0.1)")
            elif line.startswith("WAIT_FOR_SCROLL_ON"):
                commands.append(f"{get_indent()}while not keyboard.is_pressed('scroll lock'): time.sleep(0.1)")
            elif line.startswith("WAIT_FOR_SCROLL_OFF"):
                commands.append(f"{get_indent()}while keyboard.is_pressed('scroll lock'): time.sleep(0.1)")
            elif line.startswith("WAIT_FOR_SCROLL_CHANGE"):
                commands.append(f"{get_indent()}initial_state = keyboard.is_pressed('scroll lock')")
                commands.append(f"{get_indent()}while keyboard.is_pressed('scroll lock') == initial_state: time.sleep(0.1)")
            elif line.startswith("SAVE_HOST_KEYBOARD_LOCK_STATE"):
                commands.append(f"{get_indent()}_saved_caps = keyboard.is_pressed('caps lock')")
                commands.append(f"{get_indent()}_saved_num = keyboard.is_pressed('num lock')")
                commands.append(f"{get_indent()}_saved_scroll = keyboard.is_pressed('scroll lock')")
            elif line.startswith("RESTORE_HOST_KEYBOARD_LOCK_STATE"):
                commands.append(f"{get_indent()}if keyboard.is_pressed('caps lock') != _saved_caps: pyautogui.press('caps lock')")
                commands.append(f"{get_indent()}if keyboard.is_pressed('num lock') != _saved_num: pyautogui.press('num lock')")
                commands.append(f"{get_indent()}if keyboard.is_pressed('scroll lock') != _saved_scroll: pyautogui.press('scroll lock')")
            elif line.startswith("EXFIL"):
                # Exfiltrate data
                data = line[6:].strip()
                commands.append(f"# Exfiltrate data: {data}")
            elif line.startswith("CTRL") and len(line.split()) > 1:
                # Handle CTRL combinations like CTRL c, CTRL v, etc.
                key = line.split()[1].lower()
                commands.append(f"pyautogui.hotkey('ctrl', '{key}')")
            elif line.startswith("ALT") and len(line.split()) > 1:
                # Handle ALT combinations
                key = line.split()[1].lower()
                commands.append(f"pyautogui.hotkey('alt', '{key}')")
            elif line.startswith("SHIFT") and len(line.split()) > 1:
                # Handle SHIFT combinations
                key = line.split()[1].lower()
                commands.append(f"pyautogui.hotkey('shift', '{key}')")
            elif line.startswith("GUI") and len(line.split()) > 1:
                # Handle GUI (Windows key) combinations
                key = line.split()[1].lower()
                commands.append(f"pyautogui.hotkey('win', '{key}')")
            else:
                # Convert hotkeys
                keys = line.split()
                pyautogui_keys = []
                for key in keys:
                    if '+' in key:
                        combo_keys = key.split('+')
                        pyautogui_keys.extend([ducky_to_pyautogui.get(k, k) for k in combo_keys])
                    else:
                        pyautogui_key = ducky_to_pyautogui.get(key)
                        if pyautogui_key:
                            pyautogui_keys.append(pyautogui_key)
                        else:
                            commands.append(f"# Unrecognized key: {key}")
                commands.append(f"pyautogui.hotkey({', '.join([repr(k) for k in pyautogui_keys])})")

            # Add standard delay if set
            if default_delay > 0:
                commands.append(f"time.sleep({default_delay})")
            
            i += 1

        # Assemble final Python script
        python_script += "\n".join(commands)
        return python_script

    def download_exe(self):
        python_script = self.text_output.toPlainText()
        if not python_script.strip():
            self.status_label.setText("Status: Please generate Python script first")
            return

        options = QFileDialog.Options()
        output_file, _ = QFileDialog.getSaveFileName(self, "Save Python Script", "", "Python Files (*.py)", options=options)

        if output_file:
            self.status_label.setText("Status: Saving Python script...")

            with open(output_file, 'w') as file:
                file.write(python_script)

            self.status_label.setText(f"Status: Python script saved to {output_file}")

            # Generate .exe file using cx_Freeze
            self.generate_exe(output_file)

    def generate_exe(self, python_script_path):
        try:
            setup_file = self.create_setup_file(python_script_path)
            self.run_cx_freeze(setup_file)
            self.cleanup_setup_file(setup_file)
            self.status_label.setText("Status: .exe file generated successfully!")
        except Exception as e:
            self.status_label.setText(f"Status: Error generating .exe: {e}")

    def create_setup_file(self, python_script_path):
        setup_file = "setup.py"
        setup_content = f"""
# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable

# Path to your Python script
script = '{python_script_path}'

# cx_Freeze configuration
setup(
    name="Ducky2PythonApp",
    version="1.0",
    description="DuckyScript to Python converter",
    executables=[Executable(script, targetName="Ducky2PythonApp.exe")]
)
"""
        self.status_label.setText("Status: Generating .exe file...")
        with open(setup_file, 'w') as file:
            file.write(setup_content)
        try:
            subprocess.run([sys.executable, setup_file, "build"], check=True)
        except subprocess.CalledProcessError as e:
            self.status_label.setText(f"Status: Error generating .exe: {e}")
        return setup_file

    def run_cx_freeze(self, setup_file):
        self.status_label.setText("Status: Generating .exe file...")
        subprocess.run([sys.executable, setup_file, "build"], check=True)

    def cleanup_setup_file(self, setup_file):
        if os.path.exists(setup_file):
            os.remove(setup_file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ducky2ExeApp()
    window.show()
    sys.exit(app.exec())