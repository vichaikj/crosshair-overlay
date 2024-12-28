# Crosshair overlay
Green overlay that can be customize (only if you have python installed)

# Requirements
You will need Python installed on your machine

    python -m venv venv     (optional)
    venv\Scripts\activate   (optional)
    
    pip install -r requirements.txt
    
    python /path/to/repo/crosshair.py


# Building as an Executable
    pip install pyinstaller
    python -m PyInstaller --icon=/path/to/repo/crosshair.ico --onefile --noconsole /path/to/repo/crosshair.py
