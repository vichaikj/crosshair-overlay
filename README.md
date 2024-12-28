# Crosshair overlay
Display a green crosshair overlay

# Requirements
You will first need to:
* have Python installed on your machine
* open crosshair.py and replace the .ico path with your path

Then:

    python -m venv venv     (optional)
    venv\Scripts\activate   (optional)
    
    pip install -r requirements.txt
    
    python /path/to/repo/crosshair.py


# Building as an Executable
    pip install pyinstaller
    python -m PyInstaller --icon=/path/to/repo/crosshair.ico --onefile --noconsole /path/to/repo/crosshair.py
