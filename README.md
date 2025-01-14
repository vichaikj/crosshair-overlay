# Crosshair overlay
Display a green crosshair overlay

# If you just want the crosshair
A **crosshair.exe** is available in the **build** file.
It will look like this: </p>
![image](https://github.com/user-attachments/assets/abae42b8-3f12-4e5d-8c6f-1b2ed96e448c)

**Note**: **crosshair.exe** and **crosshair.ico** must be in the same folder


# Requirements (if you have Python and want to customize the crosshair)
Open crosshair.py and those values as you like:

    line_length = 12  # Dimensions of the "plus" sign (pixels in each direction from center)
    hole_size = 6  # Size of the "hole" at the center (in pixels)
    thickness = 3  # Line thickness
    transparency = 0.8  # Transparency (percent)
    outline_thickness = thickness + 2  # Outline is slightly thicker than the main crosshair

Then:

    python -m venv venv     (optional)
    venv\Scripts\activate   (optional)
    
    pip install -r requirements.txt
    
    python /path/to/repo/crosshair.py


# Building as an Executable
If you want to convert the python file into a .exe file:

    pip install pyinstaller
    python -m PyInstaller --icon=/path/to/repo/crosshair.ico --onefile --noconsole /path/to/repo/crosshair.py
