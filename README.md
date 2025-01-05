# MM2 Structure Generator

![image](https://github.com/user-attachments/assets/15d45ad3-c1fa-463e-aefa-a0fb0997b3f4)
## Description

The **MM2 Structure Generator** is a utility designed to assist users in creating a predefined folder structure and configuration files for vehicle assets in the game **Midtown Madness 2**. It simplifies the tedious process of organising files, ensuring a consistent structure for developers and modders.

## Features

- Automatically generates folders for vehicle assets, including subfolders for tuning, geometry, textures, and more.
- Creates essential configuration files such as `.info`, `.asNode`, `.mmMirror`, and others required for vehicle customization.
- Supports the creation of CSV files for opponent and player audio car data.
- GUI-based application developed with PyQt5.

## Prerequisites

To build the application, ensure the following dependencies are installed:

- Python 3.9 or later
- PyQt5
- PyInstaller

You can install the dependencies with:

```powershell
pip install PyQt5
pip install pyinstaller
```

## How to Use

1. Launch the application.
2. Enter the required details:
   - **Base Vehicle Name**: The name of the vehicle.
   - **Description**: A brief description of the vehicle.
   - **Variations (Colours)**: A list of colours separated by a `|` (e.g., `Red|Blue|Green`).
3. Click **OK** to generate the folder structure and configuration files.
4. A success message will appear, showing the paths of the generated files and folders.

## Building the Application

To create a standalone executable for Windows:

1. Open a terminal and navigate to the directory containing `mm2basestruc.py`.

2. Use the following PyInstaller command:

   ```powershell
   pyinstaller --noconfirm --onedir --console --icon ".\vpgen.ico" --name "MM2 Structure Generator" --hide-console "hide-late"  ".\mm2basestruc.py"
   ```

   - `--noconfirm`: Prevents confirmation prompts.
   - `--onedir`: Packages the entire application into a _internal directory and executable.
   - `--hide-console`: Minimizes the console window and hides it.
   - `--icon=.\vpgen.ico`: Sets a custom icon for the application.

3. The resulting executable will be located in the `dist` folder.

## Notes

- If you encounter issues with missing DLLs, ensure that the required Qt5 platform plugins and binaries are bundled correctly.
- To resolve icon issues (e.g., missing taskbar icon), ensure the `setWindowIcon` method is properly configured in the application.

## License

This project is distributed under the MIT License. See `LICENSE` for details.

---

Feel free to modify and adapt this project to suit your specific needs.

