# Ducky2Exe
This project allows you to convert Duckyscript (scripts for USB Rubber Ducky) into Python code that uses the pyautogui library to simulate key presses and then compile it into an .exe executable file using the PyInstaller library.

⚠️ Recommended: Download the .exe Version
If you prefer not to go through the setup process, you can download the precompiled .exe version of the program from the Releases Page.

## Features
Convert Duckyscript to Python: Converts Duckyscript commands into equivalent Python code using the pyautogui library to simulate key presses.
Create an Executable: After converting to Python, the script can be compiled into an .exe executable file using PyInstaller.
Simple GUI: The program provides a graphical interface for selecting a Duckyscript file, generating Python code, and compiling it into an .exe file.

## Installation

Clone or download the repository:

Download or clone the project from GitHub:

git clone https://github.com/nazarhktwitch/Ducky2Exe

cd Ducky2Exe

## Install dependencies:

Make sure you have Python 3.x installed. Then install the required libraries:

pip install -r requirements.txt

The requirements.txt file includes the following dependencies:

pyautogui — for simulating key presses.
PySide6 — for creating the graphical interface.
PyInstaller — for compiling the Python script into an executable file.

If you don't have PySide6, you can install it using:

pip install pyside6

Install cx_Freeze (if not already installed):

pip install cx_Freeze

## Usage

Run the application:

After installing the dependencies, you can start the application by running:

python Ducky2Exe.py

## How it works:

Select Duckyscript file: Click the "Select Duckyscript File" button to choose your Duckyscript file.

Convert to Python: The script will be converted into Python code, which you can save.

Compile to .exe: Afterward, you can compile the Python code into an .exe executable file.

## Graphical Interface:

The GUI has buttons for file selection, Python code generation, and compilation. You will also find a link to the project's GitHub repository in the bottom-right corner.

## Example Duckyscript (input.txt):

DELAY 1000
STRING Hello, world!
ENTER

Generated Python code:

import pyautogui
import time

time.sleep(1)
pyautogui.write('Hello, world!')
pyautogui.press('enter')
Compiling to .exe
Once the Python code is generated, you can compile it into an .exe executable file using cx_Freeze. Simply select the file and click "Compile to .exe."

## Requirements
Python 3.x
PyInstaller (for compiling)
pyautogui (for simulating key presses)
PySide6 (for graphical interface)
## Notes
The Ducky2Exe.py script currently does not handle more complex Duckyscript commands or commands with parameters. These features may be added in the future.
Make sure you have administrator rights if you are compiling executable files on Windows.
## License
This project is licensed under the MIT License. See the LICENSE file for more details.

Author: NazarHK
GitHub: https://github.com/nazarhktwitch
Discord: https://discord.gg/ZuA8jVjNvv
