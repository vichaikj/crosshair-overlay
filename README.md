# Crosshair overlay
Display a green crosshair overlay

# If you just want the crosshair
A **crosshair.exe** file is available in the **build** folder.
It will look like this: </p>
![image](https://github.com/user-attachments/assets/abae42b8-3f12-4e5d-8c6f-1b2ed96e448c)


# If you already have python installed
You can open the crosshair.py file and update this dict & value as you want.

    SELECTED_OPTION = 2
    options = {
        1: {"line_length": 12, "hole_size": 6, "thickness": 3, "transparency": 0.8},
        2: {"line_length": 16, "hole_size": 8, "thickness": 4, "transparency": 0.8},
    }

Then:

    python -m venv venv     (optional)
    venv\Scripts\activate   (optional)
    
    pip install -r requirements.txt
    
    python /path/to/repo/crosshair.py


# Building as an Executable
If you want to convert the python file into a .exe file:

    pip install pyinstaller
    python -m PyInstaller --icon=/path/to/repo/crosshair.ico --onefile --noconsole /path/to/repo/crosshair.py
