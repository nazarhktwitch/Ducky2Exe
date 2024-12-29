import sys
import subprocess
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel
import os

class Ducky2ExeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ducky2Python Converter")
        self.setGeometry(100, 100, 800, 600)

        # Создание виджетов
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

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.text_input)
        layout.addWidget(self.text_output)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def convert_to_python(self):
        ducky_script = self.text_input.toPlainText()

        if not ducky_script.strip():
            self.status_label.setText("Status: Please enter DuckyScript")
            return

        # Преобразуем DuckyScript в Python
        self.status_label.setText("Status: Converting...")
        python_script = self.parse_ducky_script(ducky_script)
        self.text_output.setPlainText(python_script)

        self.status_label.setText("Status: Python script generated")

    def parse_ducky_script(self, ducky_script):
        # Здесь будет парсер для DuckyScript. Пример, адаптированный с .js.
        python_script = "# Converted DuckyScript to Python using ducky2python!\n"
        python_script += "import pyautogui\n"
        python_script += "import time\n"

        # Делаем DuckyScript строками и удаляем лишние пробелы
        lines = ducky_script.splitlines()
        default_delay = 0
        commands = []

        # Первая строка может быть DEFAULT для задержки по умолчанию
        if lines[0].startswith("DEFAULT"):
            default_delay = int(lines[0][7:].strip()) / 1000  # в Python время указывается в секундах
            lines = lines[1:]  # Убираем первую строку с DEFAULT

        # Словарь для перевода команд DuckyScript в pyautogui
        ducky_to_pyautogui = {
            "WINDOWS": "win", "GUI": "win", "APP": "optionleft", "MENU": "optionleft", "SHIFT": "shift",
            "ALT": "alt", "CONTROL": "ctrl", "CTRL": "ctrl", "DOWNARROW": "down", "DOWN": "down",
            "LEFTARROW": "left", "LEFT": "left", "RIGHTARROW": "right", "RIGHT": "right", "UPARROW": "up",
            "UP": "up", "BREAK": "pause", "PAUSE": "pause", "CAPSLOCK": "capslock", "DELETE": "delete",
            "END": "end", "ESC": "esc", "ESCAPE": "esc", "HOME": "home", "INSERT": "insert", "NUMLOCK": "numlock",
            "PAGEUP": "pageup", "PAGEDOWN": "pagedown", "PRINTSCREEN": "printscreen", "SCROLLLOCK": "scrolllock",
            "SPACE": "space", "TAB": "tab", "ENTER": "enter", "F1": "f1", "F2": "f2", "F3": "f3", "F4": "f4",
            "F5": "f5", "F6": "f6", "F7": "f7", "F8": "f8", "F9": "f9", "F10": "f10", "F11": "f11", "F12": "f12",
            "a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G", "h": "H", "i": "I", "j": "J",
            "k": "K", "l": "L", "m": "M", "n": "N", "o": "O", "p": "P", "q": "Q", "r": "R", "s": "S", "t": "T",
            "u": "U", "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "0": "0", "!": "!", "\"": "\"", "#": "#", "$": "$",
            "%": "%", "&": "&", "\'": "\'", "(": "(", ")": ")", "*": "*", "+": "+", ",": ",", "-": "-", ".": ".",
            "/": "/", ":": ":", ";": ";", "<": "<", "=": "=", ">": ">", "?": "?", "@": "@", "[": "[", "]": "]",
            "^": "^", "_": "_", "`": "`", "{": "{", "|": "|", "}": "}", "~": "~"
        }

        # Обработка каждой строки в DuckyScript
        for line in lines:
            line = line.strip()

            # Преобразуем команды в Python
            if line.startswith("REM"):
                # Преобразуем комментарии
                commands.append(f"# {line[4:]}")
            elif line.startswith("DELAY"):
                # Преобразуем задержки
                delay_time = int(line[6:].strip()) / 1000
                commands.append(f"time.sleep({delay_time})")
            elif line.startswith("STRING"):
                # Преобразуем строки
                text = line[7:].strip()
                commands.append(f"pyautogui.typewrite('{text}', interval=0.02)")
            elif line.startswith("REPEAT"):
                # Преобразуем повторения
                repetitions = int(line[7:].strip())
                commands.append(f"# Repeat {repetitions} times")
                for _ in range(repetitions):
                    commands.append(commands[-2])  # Повторяем предыдущую строку
            else:
                # Преобразуем горячие клавиши
                keys = line.split()
                pyautogui_keys = [ducky_to_pyautogui.get(key, "UNDEFINED_KEY") for key in keys]
                commands.append(f"pyautogui.hotkey({', '.join([repr(k) for k in pyautogui_keys])})")

            # Добавляем стандартную задержку, если она установлена
            if default_delay > 0:
                commands.append(f"time.sleep({default_delay})")

        # Собираем итоговый Python-скрипт
        python_script = "\n".join(commands)
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

            # Генерация .exe файла с помощью cx_Freeze
            self.generate_exe(output_file)

    def generate_exe(self, python_script_path):
        try:
            # Генерация setup.py для cx_Freeze
            setup_content = f"""
# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable

# Путь к вашему Python скрипту
script = '{python_script_path}'

# Настройка cx_Freeze
setup(
    name="Ducky2PythonApp",
    version="1.0",
    description="DuckyScript to Python converter",
    executables=[Executable(script, targetName="Ducky2PythonApp.exe")]
)
"""

            setup_file = "setup.py"
            with open(setup_file, 'w') as file:
                file.write(setup_content)

            # Запуск cx_Freeze через subprocess
            self.status_label.setText("Status: Generating .exe file...")
            subprocess.run([sys.executable, setup_file], check=True)

            # Удаляем временный setup.py
            os.remove(setup_file)

            self.status_label.setText("Status: .exe file generated successfully!")

        except Exception as e:
            self.status_label.setText(f"Status: Error generating .exe: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ducky2ExeApp()
    window.show()
    sys.exit(app.exec())
