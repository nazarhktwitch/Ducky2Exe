# Overview

## Ducky2Python Converter

Ducky2Python Converter is a GUI application that converts DuckyScript to Python code and creates executable files. This tool allows you to take DuckyScript payloads and convert them into standalone Python programs or executables.

## Features

- User-friendly GUI interface
- Real-time conversion of DuckyScript to Python
- Export as Python script (.py) or executable (.exe)
- Supports extensive keyboard commands
- Lock key state detection and control
- Random character generation
- Delay and timing controls
- Loop and function support
- Variable and constant handling

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