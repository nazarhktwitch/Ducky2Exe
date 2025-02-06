# Installation Guide

## Prerequisites

- Python 3.7+
- Git

## Steps

1. Clone the repository:
```bash
git clone https://github.com/nazarhktwitch/Ducky2Exe.git
cd Ducky2Exe
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python Ducky2Exe.py
```

## Building from Source

Build executable using PyInstaller:
```bash
pyinstaller --noconfirm --onefile --windowed --icon="icon.png" --name="Ducky2Python" --add-data="icon.png;." --hidden-import=PySide6 --hidden-import=pyautogui --hidden-import=keyboard --collect-all=PySide6 --collect-all=pyautogui --collect-all=keyboard --clean Ducky2Exe.py
```

## Quick Start ⚡

Don't want to install Python and requirements? Download the ready-to-use executable:
[Download Latest Release](https://github.com/nazarhktwitch/Ducky2Exe/releases)