# Usage Guide

## Running the Application

1. Run the application:
```bash
python Ducky2Exe.py
```

2. Paste your DuckyScript code into the input field
3. Click "Convert to Python" to generate Python code
4. Click "Download exe" to create an executable

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

## Advanced Usage

### Lock Key Monitoring

Monitor and control lock key states (CAPSLOCK, NUMLOCK, SCROLLLOCK) using commands like `WAIT_FOR_CAPS_ON`, `WAIT_FOR_NUM_OFF`, etc.

### Random Character Generation

Generate random characters using commands like `RANDOM_LOWERCASE_LETTER`, `RANDOM_NUMBER`, etc.

### Key Holding and Releasing

Hold and release keys using `HOLD` and `RELEASE` commands.

### Button and LED Controls

Control buttons and LEDs using commands like `BUTTON_DEF`, `LED_R`, etc.

### Attack Mode Configuration

Configure attack modes using `ATTACKMODE`, `SAVE_ATTACKMODE`, and `RESTORE_ATTACKMODE` commands.