# 📜 Spooky Pack 2 Prank Viruses Project README

**Version 2.0** | **Last Updated: August 21, 2025** | **BGGG**

---

## 🚀 Project Overview

Welcome to **Spooky Pack 2**! 🎃 This is a collection of **20 harmless, humorous, and spooky prank programs** designed for Windows systems, created for fun and experimentation. Each "virus" simulates creepy effects like glitching screens, melting icons, and eerie sounds, all while ensuring **no data loss or permanent system changes**. The project includes an **interactive launcher** (`launcher.py`) that allows you to run any or all of the 20 viruses concurrently, with a help system providing full documentation and usage instructions.

The launcher supports simultaneous execution of multiple viruses, and each virus includes clear removal methods to ensure ease of use.

**Key Features**:
- 🖥️ **Interactive GUI Launcher**: Select and run viruses (1–20), view help, or exit cleanly via a `tkinter` interface.
- 👻 **20 Unique Pranks**: Each virus has distinct behaviors, visual effects (e.g., glitches, melting, skulls), and sounds (e.g., whispers, screams).
- 📚 **Integrated Documentation**: Access full details and removal instructions via the help option (7).
- 🔄 **Concurrent Execution**: Run all 20 viruses at once on your experimental PC, with process management for clean termination.
- 🛡️ **Safe and Ethical**: No system harm.
- 🛠️ **Verbose Instructions**: Detailed setup, usage, and troubleshooting for all skill levels.

**Disclaimer**: This project is for **entertainment and educational purposes only** 🎃

---

## 📋 Table of Contents

- [🎯 Project Goals](#-project-goals)
- [📦 Project Structure](#-project-structure)
- [🛠️ Setup Instructions](#-setup-instructions)
- [🚀 Usage Instructions](#-usage-instructions)
- [🧙‍♂️ Virus Descriptions](#-virus-descriptions)
- [🛑 Removal Instructions](#-removal-instructions)
- [⚙️ Technical Details](#-technical-details)
- [🔍 Troubleshooting](#-troubleshooting)
- [📝 License and Disclaimer](#-license-and-disclaimer)
- [🙌 Acknowledgments](#-acknowledgments)

---

## 🎯 Project Goals

The **Spooky Pack 2 Prank Viruses Project** aims to:
- Provide a **fun and educational** way to explore Windows system manipulation using Python, with a focus on visual and audio effects. 🎨🔊
- Create **20 distinct prank programs** that simulate spooky, virus-like behaviors without causing harm. 👻
- Offer an **interactive launcher** to manage and run pranks concurrently, with a user-friendly GUI and detailed documentation. 🖥️
- Ensure **safety and reversibility**, making all effects temporary and easily removable via key combos, shortcuts, or rebooting. 🔄
- Support experimentation, with considerations for resource constraints and robust error handling. 💾

---

## 📦 Project Structure

The project consists of **21 Python scripts** in a single directory:

- **`launcher.py`**: The main interactive launcher script with a GUI for selecting and running viruses, viewing help, or exiting.
- **`virus_1.py` to `virus_20.py`**: Individual scripts for each prank virus, implementing the behaviors and effects described in the documentation.

**Directory Example**:
```
C:\Experiments\SpookyPack2\
├── launcher.py
├── virus_1.py
├── virus_2.py
├── ...
├── virus_20.py
```

**Generated Files**:
- Each virus creates temporary files (e.g., `skull.png`, `ScrollFix.bat`) during execution, which are automatically removed when the virus stops or the system reboots.
- Desktop shortcuts (e.g., `EmojiBanish.exe`, `SoundFix.bat`) are created as removal methods, pointing to a simple exit script.

**Dependencies**:
- **Python 3.x** (tested with Python 3.8+)
- **Libraries**:
  - `tkinter` (included with Python for GUI)
  - `pywin32` (for Windows API interactions)
  - `Pillow` (for image manipulation, e.g., skull icons)
  - `pyperclip` (for clipboard manipulation in Virus 18)
  - `keyboard` (optional for some input detection, may require admin privileges)
- Install dependencies: `pip install pywin32 Pillow pyperclip keyboard`

---

## 🛠️ Setup Instructions

Follow these steps to set up the project on your experimental Windows PC:

1. **Install Python** 🐍:
   - Download and install **Python 3.8 or later** from [python.org](https://www.python.org/downloads/).
   - Ensure Python is added to your system PATH during installation.

2. **Install Dependencies** 📦:
   - Open a command prompt and run:
     ```bash
     pip install pywin32 Pillow pyperclip keyboard
     ```
   - Verify installation: `pip list` should show `pywin32`, `Pillow`, `pyperclip`, and `keyboard`.
   - Note: The `keyboard` library may require admin privileges for some viruses (e.g., Virus 12).

3. **Create Project Directory** 📂:
   - Create a directory for the project, e.g., `C:\Experiments\SpookyPack2`.
   - Save the launcher script (`launcher.py`) and all virus scripts (`virus_1.py` to `virus_20.py`) in this directory.
   - Ensure each virus script matches the code provided earlier for Viruses 1–20.

4. **Verify Scripts** ✅:
   - Confirm all 21 scripts (`launcher.py`, `virus_1.py` to `virus_20.py`) are in the same directory.
   - Check that each script is named correctly (e.g., `virus_10.py` for Creepy Color Shift).

5. **Test Environment** 🧪:
   - On your experimental PC, ensure it has sufficient resources (at least 2 GB RAM, Windows 7 or later).
   - Monitor CPU and memory usage via Task Manager during testing to avoid overloading the system.

6. **Optional: Create Executables** ⚙️:
   - To run viruses as standalone executables, use `pyinstaller`:
     ```bash
     pip install pyinstaller
     pyinstaller --onefile virus_1.py
     ```
   - This creates `virus_1.exe` in the `dist` folder. Repeat for each virus if desired. Update `launcher.py` to reference `.exe` files instead of `.py` if used.

---

## 🚀 Usage Instructions

The launcher provides an interactive GUI to run the prank viruses, view help, or exit. Here’s how to use it:

1. **Launch the Program** 🎬:
   - Navigate to the project directory in a command prompt:
     ```bash
     cd C:\Experiments\SpookyPack2
     ```
   - Run the launcher:
     ```bash
     python launcher.py
     ```
   - A `tkinter` GUI window will appear with an input field and a log area.

2. **Interact with the GUI** 🖱️:
   - **Input Field**: Enter a number (1–20, 7, 99, 100, or 0) and press Enter.
   - **Options**:
     - **1–20**: Start the corresponding virus (e.g., 1 for Shadowy Scroll Sabotage). Each virus runs as a separate process, allowing concurrent execution.
     - **7**: Open a help window with full documentation and this README.
     - **99**: Launch all 20 viruses simultaneously.
     - **100**: Launch all 20 viruses sequentially with a user-defined interval (in seconds).
     - **0**: Terminate all running virus processes and exit the launcher.
   - **Log Area**: Displays feedback, such as which viruses are running (with PIDs), errors (e.g., missing scripts), or termination confirmations.

3. **Running Viruses** 🦠:
   - Enter a number (e.g., 1) to start `virus_1.py`. The virus runs immediately, and the log shows “Started Virus 1: Shadowy Scroll Sabotage (PID: 1234)”.
   - Repeat for other viruses (e.g., 2, 3, etc.) to run multiple viruses simultaneously. All 20 can run at once on your experimental PC.
   - Each virus performs its prank (e.g., scroll bar jitter, creepy notifications, eerie sounds) as described below.

4. **Viewing Help** 📖:
   - Enter 7 to open a scrollable window with the full documentation and README, detailing each virus’s behavior, effects, and removal methods.

5. **Exiting** 🛑:
   - Enter 0 to terminate all running virus processes and close the launcher. The log confirms each process’s termination (e.g., “Terminated process PID: 1234”).
   - If a process doesn’t stop, reboot the PC to clear all effects (all changes are temporary).

6. **Monitoring Performance** 📈:
   - On your PC, monitor system performance in Task Manager (Ctrl+Shift+Esc) while running multiple viruses.
   - If the system slows down, stop some viruses using their removal methods (see below) or reboot.

---

## 🧙‍♂️ Virus Descriptions

Below is the detailed description of each prank virus, including its behavior, visual effects, and purpose, as provided in the original documentation.

### 🦠 Virus 1: Shadowy Scroll Sabotage
- **Description**: Scroll bars become "haunted," moving on their own with eerie visuals. 👻
- **Behavior**: Scroll bars in windows jitter and scroll randomly, as if controlled by an invisible force. A faint, ghostly hum plays.
- **Visual Effects**: Scroll bars flicker with a glitch effect, occasionally forming a skull shape in the scroll track.
- **Purpose**: Creates a spooky, disorienting scrolling experience.

### 🦠 Virus 2: Melting Task Manager
- **Description**: Task Manager appears to melt and display creepy messages. 💧
- **Behavior**: Opening Task Manager shows processes renamed to "GhostProcess" or "SkullTask." The window warps and drips. A low moan plays.
- **Visual Effects**: The Task Manager interface melts, with glitchy skull icons next to process names.
- **Purpose**: Mimics a haunted system monitoring tool.

### 🦠 Virus 3: Eerie Icon Invasion
- **Description**: Desktop icons multiply and form creepy patterns. 📊
- **Behavior**: Duplicate icons appear, arranging into a pentagram or skull shape. A cackle plays when the pattern completes.
- **Visual Effects**: New icons glitch and flicker, with some melting into skull shapes before stabilizing.
- **Purpose**: Creates a chaotic, spooky desktop layout.

### 🦠 Virus 4: Phantom File Flipper
- **Description**: Files appear to flip upside down with spooky effects. 📜
- **Behavior**: File names and icons on the desktop or in Explorer invert, with names like "UpsideDown.txt." A distant scream plays.
- **Visual Effects**: Icons glitch and rotate, with faint skulls appearing in the background.
- **Purpose**: Simulates a disorienting, haunted file system.

### 🦠 Virus 5: Glitchy Graveyard Glow
- **Description**: The screen glows with an eerie light, showing ghostly shapes. 🌫️
- **Behavior**: The display pulses with a green or purple glow, with faint shadows moving across it. A low, eerie chant plays.
- **Visual Effects**: Glitch effects create skull outlines in the glow, with occasional melting distortions.
- **Purpose**: Creates an unsettling, supernatural screen effect.

### 🦠 Virus 6: Cursed Caps Lock
- **Description**: The Caps Lock key triggers creepy effects when pressed. ⌨️
- **Behavior**: Pressing Caps Lock plays a scream and displays a fake "System Cursed" warning. Text typed appears in red.
- **Visual Effects**: The warning pop-up glitches and melts, with a skull flashing briefly.
- **Purpose**: Adds a startling twist to keyboard input.

### 🦠 Virus 7: Haunted Hard Drive Hum
- **Description**: The system mimics a haunted hard drive with creepy sounds. 💾
- **Behavior**: Random disk access sounds (grinding, clicking) play, with a fake "Drive Haunted" error. A ghostly whisper accompanies it.
- **Visual Effects**: File Explorer windows glitch, with skull icons appearing on drive folders.
- **Purpose**: Simulates a haunted storage device.

### 🦠 Virus 8: Skull-Filled Search Bar
- **Description**: The Windows search bar displays creepy results. 🔍
- **Behavior**: Typing in the search bar returns results like "Skull.exe" or "Graveyard.txt." A faint cackle plays.
- **Visual Effects**: Search results glitch and melt, with skull icons next to each suggestion.
- **Purpose**: Turns search into a spooky experience.

### 🦠 Virus 9: Wraithful Window Wanderer
- **Description**: Open windows drift across the screen like ghosts. 🪟
- **Behavior**: Windows move slowly in random directions, with a faint wail playing. They resist attempts to reposition.
- **Visual Effects**: Windows glitch and show melting edges, with translucent skulls appearing briefly.
- **Purpose**: Creates a disorienting, haunted window effect.

### 🦠 Virus 10: Creepy Color Shift
- **Description**: The screen’s colors invert and shift to eerie hues. 🎨
- **Behavior**: Colors flip to negative or neon green/purple, with a fake "Color Curse" warning. A low hum plays.
- **Visual Effects**: The screen glitches, with skull shapes forming in distorted color patches.
- **Purpose**: Mimics a haunted display malfunction.

### 🦠 Virus 11: Phantom Folder Flicker
- **Description**: Folders blink in and out, leaving creepy traces. 📂
- **Behavior**: Folders in File Explorer fade in and out, with names changing to "Lost" or "Doomed." A faint moan plays.
- **Visual Effects**: Folders glitch and melt, with skull silhouettes appearing during fades.
- **Purpose**: Simulates haunted folder behavior.

### 🦠 Virus 12: Eerie Emoji Explosion
- **Description**: Typing triggers creepy emojis across applications. 😱
- **Behavior**: Every keypress adds skull or ghost emojis to text fields. A ghostly giggle plays randomly.
- **Visual Effects**: Emojis glitch and briefly melt before appearing.
- **Purpose**: Adds a spooky twist to text input.

### 🦠 Virus 13: Melting Mouse Mayhem
- **Description**: The mouse pointer leaves a melting trail with spooky effects. 🖱️
- **Behavior**: Moving the mouse creates a dripping trail, with random skull shapes forming. A low wail plays.
- **Visual Effects**: The trail melts and glitches, with skulls fading in and out.
- **Purpose**: Creates a surreal, haunted cursor effect.

### 🦠 Virus 14: Ghostly Glitch Grid
- **Description**: The screen displays a grid of glitchy, creepy patterns. 📈
- **Behavior**: A grid overlay appears, with cells flickering and forming skull shapes. A distorted chant plays.
- **Visual Effects**: The grid glitches and melts, with skulls pulsing in random cells.
- **Purpose**: Mimics a haunted, glitchy interface.

### 🦠 Virus 15: Haunted Notification Nudge
- **Description**: Fake notifications with creepy messages flood the system. 🔔
- **Behavior**: Notifications pop up with messages like "System Possessed" or "Skull Detected." A faint scream plays.
- **Visual Effects**: Notifications glitch and melt, with skull icons in the corners.
- **Purpose**: Simulates intrusive, spooky alerts.

### 🦠 Virus 16: Spooky Shortcut Shuffle
- **Description**: Shortcuts dance and rename themselves creepily. 🔗
- **Behavior**: Desktop shortcuts move in a circular pattern, renaming to "FearLink" or "DoomApp." A cackle plays.
- **Visual Effects**: Shortcuts glitch and show melting skull icons briefly.
- **Purpose**: Creates a chaotic, spooky desktop interaction.

### 🦠 Virus 17: Phantom Power Pulse
- **Description**: The screen mimics a power surge with creepy visuals. ⚡️
- **Behavior**: The display flickers as if losing power, with fake "System Failure" warnings. A low buzz plays.
- **Visual Effects**: Flickers include glitchy skull shapes and melting effects.
- **Purpose**: Simulates a haunted power malfunction.

### 🦠 Virus 18: Creepy Clipboard Curse
- **Description**: Copied text is replaced with spooky phrases. 📋
- **Behavior**: Copying text pastes phrases like "I see you" or "Run." A ghostly whisper plays.
- **Visual Effects**: Pasted text glitches and briefly forms skull shapes.
- **Purpose**: Adds a spooky twist to clipboard operations.

### 🦠 Virus 19: Glitchy Graveyard Game
- **Description**: A fake game overlay appears with creepy challenges. 🎮
- **Behavior**: A pop-up "game" prompts the user to "catch skulls" with the mouse. Skulls appear randomly with eerie sounds.
- **Visual Effects**: Skulls glitch and melt as they move, with a glitchy background.
- **Purpose**: Creates an intrusive, spooky interactive prank.

### 🦠 Virus 20: Spectral Sound Switcher
- **Description**: System sounds are replaced with creepy noises. 🔊
- **Behavior**: Normal Windows sounds (e.g., alerts) become screams, moans, or whispers. Volume fluctuates slightly.
- **Visual Effects**: A glitchy skull flashes when sounds play, with melting effects around it.
- **Purpose**: Disrupts audio with eerie, supernatural sounds.

---

## 🛑 Removal Instructions

Each virus is designed to be **easily reversible** with specific removal methods. Below are the instructions for stopping each virus, plus a universal fallback (rebooting). Use these to stop individual viruses, or enter 0 in the launcher to terminate all running processes.

- **Virus 1**: Press `Ctrl + Shift + S` or run "ScrollFix.bat" from the desktop.
- **Virus 2**: Click a hidden "Restore" button in Task Manager or end "MeltManager.exe" in a secondary Task Manager instance.
- **Virus 3**: Right-click the desktop and select "Purge Icons" from a custom menu or reboot.
- **Virus 4**: Press `Ctrl + Alt + Flip` or run "RightSideUp.exe" from the desktop.
- **Virus 5**: Adjust screen brightness to max and back or run "GlowBanish.bat".
- **Virus 6**: Press Caps Lock five times in a row or end "CursedCaps.exe" in Task Manager.
- **Virus 7**: Open File Explorer and select "Cleanse Drive" from a custom menu or reboot.
- **Virus 8**: Type "CLEAR" in the search bar or run "SearchFix.exe".
- **Virus 9**: Press `Ctrl + Alt + Anchor` or run "WindowLock.bat".
- **Virus 10**: Open Display Settings and select "Restore Colors" from a custom option or reboot.
- **Virus 11**: Right-click a folder and select "Stabilize" from a custom menu or end "FlickerFolder.exe".
- **Virus 12**: Press `Ctrl + Shift + E` or run "EmojiBanish.exe".
- **Virus 13**: Click both mouse buttons simultaneously three times or run "MouseClean.bat".
- **Virus 14**: Press `Ctrl + Alt + Grid` or run "GridBanish.exe".
- **Virus 15**: Click "Dismiss All" on any notification or end "NotifyGhost.exe" in Task Manager.
- **Virus 16**: Right-click a shortcut and select "Freeze" from a custom menu or reboot.
- **Virus 17**: Press `Ctrl + Shift + Power` or run "PowerFix.bat".
- **Virus 18**: Paste "UNCURSE" into any text field or end "ClipCurse.exe" in Task Manager.
- **Virus 19**: Click "Exit Game" in the pop-up or run "GameBanish.exe".
- **Virus 20**: Open Sound Settings and select "Restore Sounds" from a custom option or run "SoundFix.bat".

**Universal Fallback**:
- **Reboot**: Restarting the PC terminates all virus effects, as they are memory-based and do not modify system files. 🔄
- **Launcher Exit**: Enter 0 in the launcher to stop all running virus processes.

**Note**: If a virus doesn’t stop as expected, check Task Manager for processes like `python.exe` or `virus_<number>.exe` and end them manually. Rebooting is always a safe option.

---

## ⚙️ Technical Details

### 🖥️ System Requirements
- **OS**: Windows 7 or later (tested on Windows 10/11).
- **Python**: 3.8 or later.
- **Hardware**: Minimum 2 GB RAM, 1 GHz CPU. Older PCs may experience slowdowns when running all 20 viruses simultaneously.
- **Dependencies**:
  - `tkinter`: For GUI (included with Python).
  - `pywin32`: For Windows API interactions (`pip install pywin32`).
  - `Pillow`: For image manipulation (`pip install Pillow`).
  - `pyperclip`: For clipboard manipulation (`pip install pyperclip`).
  - `keyboard`: For key detection in some viruses (`pip install keyboard`, may require admin privileges).

### 🛠️ Implementation
- **Launcher (`launcher.py`)**:
  - Uses `tkinter` for a GUI with an input field and log area.
  - Launches viruses via `subprocess.Popen`, allowing concurrent execution.
  - Tracks processes in a list for termination on exit (option 0).
  - Displays help with full documentation via a scrollable `tkinter` window.
- **Virus Scripts**:
  - Written in Python, using:
    - `tkinter` for overlays (e.g., pop-ups, grids).
    - `pywin32` for Windows API calls (e.g., desktop, taskbar manipulation).
    - `Pillow` for visual effects (e.g., skull icons, glitches, melting).
    - `pyperclip` for clipboard manipulation (Virus 18).
    - `keyboard` for key detection (Virus 12, optional).
    - `winsound` for eerie sounds (e.g., whispers, screams).
  - Effects are temporary, stored in memory, and do not modify system files.
- **Visual Effects**:
  - **Glitches**: Pixelated lines, static, and color shifts using `tkinter` canvases or `Pillow`.
  - **Melting**: Warping animations via `tkinter` geometry changes or `Pillow` image distortions.
  - **Skulls**: Semi-transparent PNGs rendered as overlays.
- **Concurrency**: Each virus runs in a separate process, allowing simultaneous execution. The launcher manages process IDs for clean termination.

### 🧪 Performance on Older PCs
- Running all 20 viruses may strain your experimental PC due to:
  - Multiple `tkinter` windows (e.g., pop-ups, overlays).
  - Frequent API calls (`pywin32` for desktop/taskbar manipulation).
  - Sound playback (`winsound`) and image rendering (`Pillow`).
- **Mitigation**:
  - Start with 1–5 viruses and monitor performance in Task Manager.
  - Use removal methods or reboot if the system slows down.
  - The launcher logs process IDs for manual termination if needed.

---

## 🔍 Troubleshooting

Here are common issues and solutions for running the project on your experimental PC:

- **Problem**: Launcher fails to start with “No module named <library>”.
  - **Solution**: Install missing dependencies:
    ```bash
    pip install pywin32 Pillow pyperclip keyboard
    ```

- **Problem**: “Error: virus_<number>.py not found” in the log.
  - **Solution**: Ensure all scripts (`virus_1.py` to `virus_20.py`) are in the same directory as `launcher.py`. Verify file names match exactly.

- **Problem**: System slows down or freezes when running multiple viruses.
  - **Solution**:
    - Stop viruses using their removal methods (e.g., key combos, shortcuts).
    - Enter 0 in the launcher to terminate all processes.
    - Reboot the PC to clear all effects.
    - Run fewer viruses (e.g., 1–5) to reduce resource usage.

- **Problem**: A virus doesn’t stop with its key combo or shortcut.
  - **Solution**:
    - Open Task Manager (Ctrl+Shift+Esc), find `python.exe` or `virus_<number>.exe`, and end the process.
    - Reboot the PC to terminate all effects.
    - Check the log for the process ID (PID) and end it manually.

- **Problem**: Visual effects (e.g., skulls, glitches) don’t display correctly.
  - **Solution**:
    - Ensure `Pillow` is installed (`pip install Pillow`).
    - Verify your PC’s graphics driver supports `tkinter` rendering.
    - Reduce the number of running viruses to lower GPU load.

- **Problem**: Sounds (e.g., whispers, screams) don’t play.
  - **Solution**:
    - Check that your PC’s audio is enabled and not muted.
    - Test `winsound` with a simple script:
      ```python
      import winsound
      winsound.Beep(1000, 500)
      ```
    - Ensure no other applications are blocking audio output.

- **Problem**: Launcher GUI is unresponsive.
  - **Solution**:
    - Close the launcher via Task Manager (`python.exe`).
    - Restart the launcher and run fewer viruses.
    - Reboot the PC if needed.

For additional help, refer to the help window (option 7) or contact the script creator (not applicable for this fictional setup).

---

## 📝 License and Disclaimer

**License**: This project is provided under the **MIT License** for educational and experimental use:
```
MIT License

Copyright (c) 2025 BG Gremlin Group

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

**Disclaimer**:
- This project is for **entertainment and educational purposes**
- **No warranty**: The software is provided as-is, with no guarantee of performance or suitability.
- **Safety**: All effects are temporary and reversible. No data loss or system damage will occur if used as intended.

---

## 🙌 Acknowledgments

- **Python Community**: For providing libraries like `tkinter`, `pywin32`, `Pillow`, `pyperclip`, and `keyboard`. 🐍
- **xAI**: For assistance in DevOps and AI-driven development support.
- **Windows APIs**: For enabling creative system manipulations in a safe manner. 🖥️
- **You**: For experimenting with this fun project on your PC! 🎉

---

## 🌟 Final Notes

**Spooky Pack 2** is a playful and creepy collection of 20 prank viruses, perfect for exploring Windows system manipulation in a safe, fun way. With a **user-friendly launcher**, **comprehensive documentation**, and **reversible effects**, it’s ideal for anyone looking to experiment with spooky effects on a test PC. Have fun testing the eerie visuals and sounds, but keep an eye on performance and use the removal methods to keep things under control.

**Happy Haunting!** 👻

### Background Gremlin Group
***Creating Unique Tools for Unique Individuals***
