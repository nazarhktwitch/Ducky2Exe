# Ducky2Python Converter

A GUI application that converts DuckyScript to Python code and creates executable files. This tool allows you to take DuckyScript payloads and convert them into standalone Python programs or executables.

## Quick Start ⚡

Don't want to install Python and requirements? Download the ready-to-use executable:
[Download Latest Release](https://github.com/nazarhktwitch/Ducky2Exe/releases)

## Features

- 🖥️ User-friendly GUI interface
- 🔄 Real-time conversion of DuckyScript to Python
- 📦 Export as Python script (.py) or executable (.exe)
- ⌨️ Supports extensive keyboard commands
- 🔒 Lock key state detection and control
- 🎲 Random character generation
- ⏱️ Delay and timing controls
- 🔁 Loop and function support
- 💾 Variable and constant handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Ducky2Exe.git
cd Ducky2Exe
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python Ducky2Exe.py
```

2. Paste your DuckyScript code into the input field
3. Click "Convert to Python" to generate Python code
4. Click "Download exe" to create an executable

## Supported Commands

### Basic Keys
- All standard keyboard keys
- Function keys (F1-F12)
- Special keys (CTRL, ALT, SHIFT, GUI/WINDOWS)
- Media and volume controls

### Special Commands
- DELAY - Add timing delays
- STRING/STRINGLN - Text input
- REM/REM_BLOCK - Comments
- REPEAT - Command repetition
- FUNCTION - Custom functions
- IF/ELSE/WHILE - Control structures
- Variables and constants

### Advanced Features
- Lock key monitoring (CAPSLOCK, NUMLOCK, SCROLLLOCK)
- Random character generation
- Key holding and releasing
- Button and LED controls
- Attack mode configuration

## Example

```ducky
REM Open Notepad and type a message
DELAY 500
GUI r
DELAY 100
STRING notepad
ENTER
DELAY 1000
STRING Hello from Ducky2Python!
ENTER
STRING This script was converted using Ducky2Python Converter.
```

## Requirements

- Python 3.7+
- PySide6
- PyAutoGUI
- keyboard
- cx_Freeze (for executable creation)

## Building from Source

Build executable using PyInstaller:
```bash
pyinstaller --noconfirm --onefile --windowed --icon="icon.png" --name="Ducky2Python" --add-data="icon.png;." --hidden-import=PySide6 --hidden-import=pyautogui --hidden-import=keyboard --collect-all=PySide6 --collect-all=pyautogui --collect-all=keyboard --clean Ducky2Exe.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/yourusername/Ducky2Exe/blob/main/LICENSE) file for details.

## Contributing

Feel free to submit issues, fork the repository and create pull requests for any improvements.

## Acknowledgments

- Thanks to the Hak5 team for the DuckyScript specification
- Special thanks to all users