# Crosshair overlay
Display a crosshair overlay with preset selectable sizes and colors

# If you just want the crosshair
A **crosshair.exe** file is available in the **build** folder.
It will look like this: </p>
<img width="156" height="43" alt="Screenshot 2025-12-04 013557" src="https://github.com/user-attachments/assets/8fdb52dc-f0f8-41a1-a484-0a1635763e02" />
<p>
<img width="221" height="84" alt="image" src="https://github.com/user-attachments/assets/eb9468ce-77c0-478f-92f3-46f338ee4eb0" />
<p>
<img width="201" height="95" alt="image" src="https://github.com/user-attachments/assets/bd9130bd-5db3-4ac2-ab00-22f71e00cb17" />




# Crosshair customization (Python needed)
All the code lies in `crosshair.py`.
Additional options (crosshair size / color) can be added in `sizes` and `colors` dicts.

    # Size definitions
    sizes = {
        "small": {"line_length": 8, "hole_size": 4, "thickness": 2, "transparency": 0.8},
        "medium": {"line_length": 12, "hole_size": 6, "thickness": 3, "transparency": 0.8},
        "large": {"line_length": 16, "hole_size": 8, "thickness": 4, "transparency": 0.8},

        # EXAMPLE NEW VALUE
        "very_large": {"line_length": 20, "hole_size": 10, "thickness": 5, "transparency": 0.8},
    }

    # Color definitions
    colors = {
        "green": (0, 255, 0),
        "red": (255, 0, 0),
        "blue": (0, 150, 255),
        "white": (255, 255, 255),
    }

Then, create your virtual env, install the requirements and execute the python script:

    python -m venv venv
    venv\Scripts\activate

    pip install -r requirements.txt

    python /path/to/repo/crosshair.py


# Building as an Executable
If you want to convert the python file into a .exe file:

    pip install pyinstaller
    python -m PyInstaller --icon=/path/to/repo/crosshair.ico --onefile --noconsole --add-data "/path/to/repo/crosshair.ico;." /path/to/repo/crosshair.py
