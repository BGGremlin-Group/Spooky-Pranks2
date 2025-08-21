#!/usr/bin/env python3
"""
# SP2 - launcher V2 - Dependency Auto Installer
"""
import subprocess
import os
import sys
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import threading
import win32com.client
import importlib
import pkg_resources
import time

# Full documentation for Spooky Pack 2 (unchanged)
DOCUMENTATION = """
# Documentation: Spooky Pack 2 - 20 Harmless but Funny and Creepy Windows Viruses

## Overview
This document describes 20 fictional, harmless prank programs designed to simulate creepy and humorous "virus" effects on Windows systems. These programs are purely for entertainment, causing no permanent damage or data loss. Some include visual distortions like screen glitches, melting effects, or skull imagery for a spooky yet playful vibe. Each entry includes a description, behavior, visual effects (if applicable), and a "removal" method to ensure reversibility.

**Note**: These are fictional and intended for consensual pranks on personal test systems. Ethical programming practices are required to ensure no harm to systems or data.

---

## Virus 1: Shadowy Scroll Sabotage
- **Description**: Scroll bars become "haunted," moving on their own with eerie visuals.
- **Behavior**: Scroll bars in windows jitter and scroll randomly, as if controlled by an invisible force. A faint, ghostly hum plays.
- **Visual Effects**: Scroll bars flicker with a glitch effect, occasionally forming a skull shape in the scroll track.
- **Removal**: Press `Ctrl + Shift + S` or run "ScrollFix.bat" from the desktop.

## Virus 2: Melting Task Manager
- **Description**: Task Manager appears to melt and display creepy messages.
- **Behavior**: Opening Task Manager shows processes renamed to "GhostProcess" or "SkullTask." The window warps and drips. A low moan plays.
- **Visual Effects**: The Task Manager interface melts, with glitchy skull icons appearing next to process names.
- **Removal**: Click a hidden "Restore" button in Task Manager or end "MeltManager.exe" in a secondary Task Manager instance.

## Virus 3: Eerie Icon Invasion
- **Description**: Desktop icons multiply and form creepy patterns.
- **Behavior**: Duplicate icons appear, arranging into a pentagram or skull shape. A cackle plays when the pattern completes.
- **Visual Effects**: New icons glitch and flicker, with some melting into skull shapes before stabilizing.
- **Removal**: Right-click the desktop and select "Purge Icons" from a custom menu or reboot.

## Virus 4: Phantom File Flipper
- **Description**: Files appear to flip upside down with spooky effects.
- **Behavior**: File names and icons on the desktop or in Explorer invert, with names like "UpsideDown.txt." A distant scream plays.
- **Visual Effects**: Icons glitch and rotate, with faint skulls appearing in the background.
- **Removal**: Press `Ctrl + Alt + Flip` or run "RightSideUp.exe" from the desktop.

## Virus 5: Glitchy Graveyard Glow
- **Description**: The screen glows with an eerie light, showing ghostly shapes.
- **Behavior**: The display pulses with a green or purple glow, with faint shadows moving across it. A low, eerie chant plays.
- **Visual Effects**: Glitch effects create skull outlines in the glow, with occasional melting distortions.
- **Removal**: Adjust screen brightness to max and back or run "GlowBanish.bat".

## Virus 6: Cursed Caps Lock
- **Description**: The Caps Lock key triggers creepy effects when pressed.
- **Behavior**: Pressing Caps Lock plays a scream and displays a fake "System Cursed" warning. Text typed appears in red.
- **Visual Effects**: The warning pop-up glitches and melts, with a skull flashing briefly.
- **Removal**: Press Caps Lock five times in a row or end "CursedCaps.exe" in Task Manager.

## Virus 7: Haunted Hard Drive Hum
- **Description**: The system mimics a haunted hard drive with creepy sounds.
- **Behavior**: Random disk access sounds (grinding, clicking) play, with a fake "Drive Haunted" error. A ghostly whisper accompanies it.
- **Visual Effects**: File Explorer windows glitch, with skull icons appearing on drive folders.
- **Removal**: Open File Explorer and select "Cleanse Drive" from a custom menu or reboot.

## Virus 8: Skull-Filled Search Bar
- **Description**: The Windows search bar displays creepy results.
- **Behavior**: Typing in the search bar returns results like "Skull.exe" or "Graveyard.txt." A faint cackle plays.
- **Visual Effects**: Search results glitch and melt, with skull icons next to each suggestion.
- **Removal**: Type "CLEAR" in the search bar or run "SearchFix.exe".

## Virus 9: Wraithful Window Wanderer
- **Description**: Open windows drift across the screen like ghosts.
- **Behavior**: Windows move slowly in random directions, with a faint wail playing. They resist attempts to reposition.
- **Visual Effects**: Windows glitch and show melting edges, with translucent skulls appearing briefly.
- **Removal**: Press `Ctrl + Alt + Anchor` or run "WindowLock.bat".

## Virus 10: Creepy Color Shift
- **Description**: The screen’s colors invert and shift to eerie hues.
- **Behavior**: Colors flip to negative or neon green/purple, with a fake "Color Curse" warning. A low hum plays.
- **Visual Effects**: The screen glitches, with skull shapes forming in distorted color patches.
- **Removal**: Open Display Settings and select "Restore Colors" from a custom option or reboot.

## Virus 11: Phantom Folder Flicker
- **Description**: Folders blink in and out, leaving creepy traces.
- **Behavior**: Folders in File Explorer fade in and out, with names changing to "Lost" or "Doomed." A faint moan plays.
- **Visual Effects**: Folders glitch and melt, with skull silhouettes appearing during fades.
- **Removal**: Right-click a folder and select "Stabilize" from a custom menu or end "FlickerFolder.exe".

## Virus 12: Eerie Emoji Explosion
- **Description**: Typing triggers creepy emojis across applications.
- **Behavior**: Every keypress adds skull or ghost emojis to text fields. A ghostly giggle plays randomly.
- **Visual Effects**: Emojis glitch and briefly melt before appearing.
- **Removal**: Press `Ctrl + Shift + E` or run "EmojiBanish.exe".

## Virus 13: Melting Mouse Mayhem
- **Description**: The mouse pointer leaves a melting trail with spooky effects.
- **Behavior**: Moving the mouse creates a dripping trail, with random skull shapes forming. A low wail plays.
- **Visual Effects**: The trail melts and glitches, with skulls fading in and out.
- **Removal**: Click both mouse buttons simultaneously three times or run "MouseClean.bat".

## Virus 14: Ghostly Glitch Grid
- **Description**: The screen displays a grid of glitchy, creepy patterns.
- **Behavior**: A grid overlay appears, with cells flickering and forming skull shapes. A distorted chant plays.
- **Visual Effects**: The grid glitches and melts, with skulls pulsing in random cells.
- **Removal**: Press `Ctrl + Alt + Grid` or run "GridBanish.exe".

## Virus 15: Haunted Notification Nudge
- **Description**: Fake notifications with creepy messages flood the system.
- **Behavior**: Notifications pop up with messages like "System Possessed" or "Skull Detected." A faint scream plays.
- **Visual Effects**: Notifications glitch and melt, with skull icons in the corners.
- **Removal**: Click "Dismiss All" on any notification or end "NotifyGhost.exe" in Task Manager.

## Virus 16: Spooky Shortcut Shuffle
- **Description**: Shortcuts dance and rename themselves creepily.
- **Behavior**: Desktop shortcuts move in a circular pattern, renaming to "FearLink" or "DoomApp." A cackle plays.
- **Visual Effects**: Shortcuts glitch and show melting skull icons briefly.
- **Removal**: Right-click a shortcut and select "Freeze" from a custom menu or reboot.

## Virus 17: Phantom Power Pulse
- **Description**: The screen mimics a power surge with creepy visuals.
- **Behavior**: The display flickers as if losing power, with fake "System Failure" warnings. A low buzz plays.
- **Visual Effects**: Flickers include glitchy skull shapes and melting effects.
- **Removal**: Press `Ctrl + Shift + Power` or run "PowerFix.bat".

## Virus 18: Creepy Clipboard Curse
- **Description**: Copied text is replaced with spooky phrases.
- **Behavior**: Copying text pastes phrases like "I see you" or "Run." A ghostly whisper plays.
- **Visual Effects**: Pasted text glitches and briefly forms skull shapes.
- **Removal**: Paste "UNCURSE" into any text field or end "ClipCurse.exe" in Task Manager.

## Virus 19: Glitchy Graveyard Game
- **Description**: A fake game overlay appears with creepy challenges.
- **Behavior**: A pop-up "game" prompts the user to "catch skulls" with the mouse. Skulls appear randomly with eerie sounds.
- **Visual Effects**: Skulls glitch and melt as they move, with a glitchy background.
- **Removal**: Click "Exit Game" in the pop-up or run "GameBanish.exe".

## Virus 20: Spectral Sound Switcher
- **Description**: System sounds are replaced with creepy noises.
- **Behavior**: Normal Windows sounds (e.g., alerts) become screams, moans, or whispers. Volume fluctuates slightly.
- **Visual Effects**: A glitchy skull flashes when sounds play, with melting effects around it.
- **Removal**: Open Sound Settings and select "Restore Sounds" from a custom option or run "SoundFix.bat".

---

## Technical Notes
- **Implementation**: These pranks are coded as lightweight Python scripts, using Windows APIs for UI manipulation, sound playback, and visual effects (e.g., PIL for glitch/melt animations). All effects are temporary, stored in memory, and do not modify system files.
- **Safety**: No data is altered or deleted. All changes are cosmetic and reversible via key combos, hidden files, or rebooting.
- **Ethical Use**: Deploy only on personal test systems or with user consent. Include clear exit instructions in a hidden README file.
- **Visual Effects**: Glitch effects use pixelation techniques; melting effects use warping animations; skull imagery is rendered as semi-transparent overlays.

## Disclaimer
These are fictional pranks for entertainment on personal test systems. Real-world deployment requires permission and must avoid distress or system harm. Always provide clear "removal" instructions to users.

---

## README: Ethical Usage and Instructions

### Usage Instructions
1. **Running the Launcher**: Execute this script (`launcher.py`) to access the interactive menu.
2. **Selecting a Virus**: Enter a number from 1 to 20 to run the corresponding prank virus, 7 for help (displays this documentation), 99 to launch all viruses simultaneously, 100 to launch all viruses sequentially at a user-defined interval, or 0 to exit. Multiple viruses can run concurrently.
3. **Virus Execution**: Each virus runs as a separate process. Use the removal instructions below to stop individual viruses.
4. **Safety**: All viruses are harmless, with no data loss or permanent changes. Effects are reversible via key combos, desktop shortcuts, or rebooting.

### Ethical Guidelines
- **Consent**: Only run these pranks on your own experimental system or with explicit permission from the user. Unauthorized use may cause distress or be unethical.
- **Transparency**: Since this is a personal test PC, ensure you understand the effects and removal methods. For others, inform users that the program is a prank and provide clear exit instructions.
- **No Harm**: Ensure the system remains functional. These scripts are designed to avoid modifying or deleting data.
- **Exit Instructions**: Each virus has a specific removal method (listed below). Ensure you know how to stop each prank.

### Removal Instructions
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

### Notes
- Ensure all virus scripts (`virus_1.py` to `virus_20.py`) are in the same directory as this launcher.
- If a virus does not stop as expected, rebooting the system will terminate all effects.
- Running all 20 viruses simultaneously may strain an older PC. Monitor system performance and stop processes if needed.
- For support, refer to the documentation above or experiment safely on your test system.

**Disclaimer**: Use responsibly on your experimental PC. These pranks are for fun and must not be used to cause distress or harm.
"""

# Interactive Launcher with Concurrent and Sequential Execution
class LauncherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spooky Pack 2 Prank Virus Launcher")
        self.root.geometry("600x400")
        self.root.configure(bg='black')

        # Instructions label
        tk.Label(self.root, text="Select: 1-20 (virus), 7 (help), 99 (launch all), 100 (sequential), 0 (exit):", 
                 fg='red', bg='black', font=('Arial', 14)).pack(pady=10)

        # Entry for user input
        self.entry = tk.Entry(self.root, font=('Arial', 12))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.process_input)

        # Output area
        self.output = scrolledtext.ScrolledText(self.root, height=15, width=70, fg='white', bg='black', font=('Arial', 10))
        self.output.pack(pady=10)
        self.output.insert(tk.END, "Checking and installing dependencies...\n")
        self.output.config(state='disabled')

        # List to track running processes
        self.processes = []

        # Start dependency check in a separate thread
        threading.Thread(target=self.check_and_install_dependencies, daemon=True).start()

    def log_message(self, message):
        self.output.config(state='normal')
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)
        self.output.config(state='disabled')

    def check_and_install_dependencies(self):
        """Check and install required dependencies if not present."""
        required_libraries = ['pywin32', 'Pillow', 'pyperclip', 'keyboard']
        
        for lib in required_libraries:
            try:
                pkg_resources.get_distribution(lib)
                self.log_message(f"Dependency {lib} is already installed.")
            except pkg_resources.DistributionNotFound:
                self.log_message(f"Installing {lib}...")
                try:
                    # Run pip install in a subprocess
                    subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                    self.log_message(f"Successfully installed {lib}.")
                except subprocess.CalledProcessError as e:
                    self.log_message(f"Error installing {lib}: {str(e)}")
                except Exception as e:
                    self.log_message(f"Unexpected error installing {lib}: {str(e)}")
                time.sleep(1)  # Brief pause to ensure installation completes
        
        # Verify installations
        for lib in required_libraries:
            try:
                importlib.import_module(lib.lower().replace('-', ''))
                self.log_message(f"Verified {lib} is installed and importable.")
            except ImportError:
                self.log_message(f"Failed to import {lib}. Some pranks may not function correctly.")
        
        self.log_message("Dependency check complete. Enter a number (1-20, 7 for help, 99 for all, 100 for sequential, or 0 to exit).\nMultiple viruses can run at once.\n")

    def process_input(self, event):
        choice = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        try:
            choice = int(choice)
            if choice == 0:
                self.terminate_all()
                self.root.destroy()
                sys.exit(0)
            elif choice == 7:
                self.show_help()
            elif choice == 99:
                self.launch_all()
            elif choice == 100:
                self.launch_sequential()
            elif 1 <= choice <= 20:
                self.run_virus(choice)
            else:
                self.log_message("Invalid choice. Enter 1-20, 7 for help, 99 for all, 100 for sequential, or 0 to exit.")
        except ValueError:
            self.log_message("Please enter a valid number.")

    def run_virus(self, number):
        script_name = f"virus_{number}.py"
        if not os.path.exists(script_name):
            self.log_message(f"Error: {script_name} not found in the current directory.")
            return
        try:
            process = subprocess.Popen([sys.executable, script_name])
            self.processes.append(process)
            self.log_message(f"Started Virus {number}: {self.get_virus_name(number)} (PID: {process.pid})")
        except Exception as e:
            self.log_message(f"Error running {script_name}: {str(e)}")

    def launch_all(self):
        self.log_message("Launching all 20 viruses simultaneously...")
        for i in range(1, 21):
            self.run_virus(i)

    def launch_sequential(self):
        interval = simpledialog.askfloat("Sequential Launch", "Enter interval between launches (seconds, e.g., 2.0):", 
                                        parent=self.root, minvalue=0.1, maxvalue=60.0)
        if interval is None:
            self.log_message("Sequential launch cancelled.")
            return
        self.log_message(f"Launching all 20 viruses sequentially with {interval}-second intervals...")
        def sequential_task():
            for i in range(1, 21):
                self.run_virus(i)
                self.root.update()
                time.sleep(interval)
        threading.Thread(target=sequential_task, daemon=True).start()

    def terminate_all(self):
        self.log_message("Terminating all running virus processes...")
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=3)  # Wait up to 3 seconds for termination
                self.log_message(f"Terminated process PID: {process.pid}")
            except subprocess.TimeoutExpired:
                self.log_message(f"Process PID: {process.pid} did not terminate gracefully.")
            except Exception as e:
                self.log_message(f"Error terminating process PID: {process.pid}: {str(e)}")
        self.processes.clear()

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - Spooky Pack 2 Prank Virus Documentation")
        help_window.geometry("800x600")
        help_window.configure(bg='black')

        text_area = scrolledtext.ScrolledText(help_window, height=30, width=90, fg='white', bg='black', font=('Arial', 10))
        text_area.pack(pady=10)
        text_area.insert(tk.END, DOCUMENTATION)
        text_area.config(state='disabled')

    def get_virus_name(self, number):
        names = {
            1: "Shadowy Scroll Sabotage",
            2: "Melting Task Manager",
            3: "Eerie Icon Invasion",
            4: "Phantom File Flipper",
            5: "Glitchy Graveyard Glow",
            6: "Cursed Caps Lock",
            7: "Haunted Hard Drive Hum",
            8: "Skull-Filled Search Bar",
            9: "Wraithful Window Wanderer",
            10: "Creepy Color Shift",
            11: "Phantom Folder Flicker",
            12: "Eerie Emoji Explosion",
            13: "Melting Mouse Mayhem",
            14: "Ghostly Glitch Grid",
            15: "Haunted Notification Nudge",
            16: "Spooky Shortcut Shuffle",
            17: "Phantom Power Pulse",
            18: "Creepy Clipboard Curse",
            19: "Glitchy Graveyard Game",
            20: "Spectral Sound Switcher"
        }
        return names.get(number, "Unknown")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LauncherApp()
    app.run()
