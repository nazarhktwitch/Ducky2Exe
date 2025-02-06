# Build by NazarHK (nazarhktwitch)

# Install requirements first if needed
pip install -r requirements.txt
pip install pyinstaller

# Main PyInstaller command
pyinstaller --noconfirm --onefile --windowed `
    --icon="icon.png" `
    --name="Ducky2Python" `
    --add-data="icon.png;." `
    --hidden-import=PySide6 `
    --hidden-import=pyautogui `
    --hidden-import=keyboard `
    --collect-all=PySide6 `
    --collect-all=pyautogui `
    --collect-all=keyboard `
    --exclude-module=PyQt5 `
    --exclude-module=PyQt6 `
    --exclude-module=PySide2 `
    --clean `
    --log-level=WARN `
    Ducky2Exe.py