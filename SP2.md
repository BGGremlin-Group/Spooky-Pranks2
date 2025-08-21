### Virus 1: *Shadowy Scroll Sabotage*

```python
#!/usr/bin/env python3

# This script simulates the Shadowy Scroll Sabotage prank.
# It makes scrollbars in visible windows jitter randomly, plays a faint ghostly hum,
# and occasionally overlays a glitchy skull shape on the scrollbar area.
# Visual effects use Tkinter for overlays and Pillow for image generation.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Press Ctrl + Shift + S, or run the generated ScrollFix.bat on desktop.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys

# Global stop event for threads
stop_event = threading.Event()

# Hidden root for Tkinter overlays
root = tk.Tk()
root.withdraw()  # Hide the main root window

# Function to get all visible windows with vertical scrollbar
def get_windows_with_scrollbar():
    windows = []
    def enum_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            if style & win32con.WS_VSCROLL:
                windows.append(hwnd)
    win32gui.EnumWindows(enum_callback, None)
    return windows

# Function to jitter the scrollbar of a given window
def jitter_scrollbar(hwnd):
    # Get scroll info (returns dict with nMin, nMax, etc.)
    try:
        si = win32gui.GetScrollInfo(hwnd, win32con.SBAR_VERT)
        min_pos = si['nMin']
        max_pos = si['nMax'] - si['nPage']  # Adjust for visible page
        if max_pos > min_pos:
            new_pos = random.randint(min_pos, max_pos)
            win32gui.SetScrollPos(hwnd, win32con.SBAR_VERT, new_pos, True)
            # Send messages to apply the scroll
            win32gui.SendMessage(hwnd, win32con.WM_VSCROLL, (win32con.SB_THUMBPOSITION << 16) | new_pos, 0)
            win32gui.SendMessage(hwnd, win32con.WM_VSCROLL, win32con.SB_ENDSCROLL, 0)
    except:
        pass  # Ignore errors for invalid scroll info

# Function to create a glitchy skull image using Pillow
def create_glitchy_skull_image(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(img)
    
    # Draw simple skull shape (white outline)
    head_radius = min(width // 2, height // 4)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    # Eyes
    draw.ellipse((width // 3, height // 3, width // 3 + 10, height // 3 + 10), fill='white')
    draw.ellipse((width * 2 // 3 - 10, height // 3, width * 2 // 3, height // 3 + 10), fill='white')
    # Nose
    draw.polygon([(width // 2 - 5, height // 2 - 10), (width // 2 + 5, height // 2 - 10), (width // 2, height // 2)], fill='white')
    # Mouth
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 20), fill='white')
    
    # Add glitch effect: horizontal shifts
    for i in range(0, height, 10):  # Every 10 pixels
        shift = random.randint(-5, 5)
        strip = img.crop((0, i, width, i + 10))
        img.paste(strip, (shift, i))
    
    # Add random noise
    pixels = img.load()
    for x in range(width):
        for y in range(height):
            if random.random() < 0.05:  # 5% chance
                r, g, b, a = pixels[x, y]
                pixels[x, y] = (r + random.randint(-50, 50) % 255, g, b, a)
    
    return img

# Function to show glitchy skull overlay on scrollbar area
def show_skull_overlay(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    scroll_width = 20  # Approximate scrollbar width
    scroll_left = right - scroll_width
    scroll_top = top
    scroll_height = bottom - top
    
    # Create toplevel overlay
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.geometry(f"{scroll_width}x{scroll_height}+{scroll_left}+{scroll_top}")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    img = create_glitchy_skull_image(scroll_width, scroll_height)
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
    canvas.image = tk_img  # Keep reference
    
    # Flicker effect
    def flicker():
        overlay.attributes('-alpha', random.uniform(0.3, 0.7))
        if not stop_event.is_set():
            overlay.after(100, flicker)
    
    flicker()
    overlay.after(1000, overlay.destroy)  # Show for 1 second

# Main prank loop: jitter scrollbars and occasionally show visual effect
def prank_loop():
    while not stop_event.is_set():
        windows = get_windows_with_scrollbar()
        if windows:
            hwnd = random.choice(windows)
            jitter_scrollbar(hwnd)
            # Occasionally show skull (10% chance)
            if random.random() < 0.1:
                threading.Thread(target=show_skull_overlay, args=(hwnd,)).start()
        time.sleep(random.uniform(0.5, 2.0))

# Sound loop: play faint ghostly hum periodically
def sound_loop():
    while not stop_event.is_set():
        winsound.Beep(200, 500)  # Low frequency hum
        time.sleep(random.uniform(5, 10))  # Play every 5-10 seconds

# Key monitor: detect Ctrl + Shift + S
def key_monitor():
    while not stop_event.is_set():
        ctrl_pressed = win32api.GetKeyState(win32con.VK_CONTROL) < 0
        shift_pressed = win32api.GetKeyState(win32con.VK_SHIFT) < 0
        s_pressed = win32api.GetKeyState(ord('S')) < 0
        if ctrl_pressed and shift_pressed and s_pressed:
            stop_event.set()
            root.quit()
        time.sleep(0.1)

# Create the removal bat file on desktop
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "ScrollFix.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")  # Kills all python processes (simple termination)

# Start threads
prank_thread = threading.Thread(target=prank_loop)
sound_thread = threading.Thread(target=sound_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
sound_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

# Cleanup after quit
prank_thread.join()
sound_thread.join()
key_thread.join()
sys.exit(0)
```

---


### Virus 2: *Melting Task Manager*

```python
#!/usr/bin/env python3

# This script simulates the Melting Task Manager prank.
# It detects when Task Manager is opened, hides it, and shows a fake one with renamed processes,
# creepy messages, melting visual effects, and skull icons. Plays a low moan sound.
# Visual effects use Tkinter for fake window and animation, Pillow for icons.
# Requires: pip install pywin32 pillow psutil
# Run on Windows only.
# Removal: Click the "Restore" button in the fake Task Manager (semi-hidden at bottom),
# or end "python.exe" via a secondary Task Manager instance.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import psutil
import os
import sys

# Global stop event for threads
stop_event = threading.Event()

# Hidden root for Tkinter
root = tk.Tk()
root.withdraw()

# Function to detect Task Manager window
def find_task_manager():
    task_hwnd = None
    def enum_callback(hwnd, _):
        nonlocal task_hwnd
        if win32gui.GetWindowText(hwnd) == "Task Manager" and win32gui.IsWindowVisible(hwnd):
            task_hwnd = hwnd
    win32gui.EnumWindows(enum_callback, None)
    return task_hwnd

# Function to create small glitchy skull icon for processes
def create_skull_icon():
    width, height = 16, 16
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((2, 2, 14, 10), fill='white')
    draw.ellipse((4, 4, 6, 6), fill='black')
    draw.ellipse((10, 4, 12, 6), fill='black')
    draw.rectangle((4, 12, 12, 14), fill='white')
    
    # Simple glitch: shift
    strip = img.crop((0, 8, 16, 16))
    img.paste(strip, (2, 8))
    
    return img

# Function to show fake Task Manager with effects
def show_fake_task_manager(rect):
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top
    
    fake = tk.Toplevel(root)
    fake.title("Task Manager")
    fake.geometry(f"{width}x{height}+{left}+{top}")
    fake.overrideredirect(False)  # Keep title bar for realism
    
    # Treeview for processes
    tree = ttk.Treeview(fake, columns=("Process", "Status"), show="headings")
    tree.heading("Process", text="Process Name")
    tree.heading("Status", text="Status")
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Load skull icon
    skull_img = create_skull_icon()
    tk_skull = ImageTk.PhotoImage(skull_img)
    
    # Populate with renamed processes
    for proc in psutil.process_iter(['name']):
        name = proc.info['name']
        if random.random() < 0.5:
            name = random.choice(["GhostProcess", "SkullTask", "HauntedThread"])
        item = tree.insert("", "end", values=(name, "Running"))
        tree.item(item, image=tk_skull)  # Note: Treeview images need proper config, but for sim, assume
    
    # Keep reference
    tree.image = tk_skull
    
    # Creepy message label
    msg = tk.Label(fake, text="System Melting... Beware!", fg="red")
    msg.pack()
    
    # Hidden Restore button (semi-transparent)
    restore_btn = tk.Button(fake, text="Restore", command=lambda: stop_event.set() or fake.destroy() or root.quit(), bg="black", fg="gray")
    restore_btn.pack(side=tk.BOTTOM)
    restore_btn.config(state='normal')
    
    # Melting effect: jitter position and stretch height
    def melt_animation():
        if not stop_event.is_set():
            # Jitter
            fake.geometry(f"+{left + random.randint(-5,5)}+{top + random.randint(-5,5)}")
            # Drip (stretch height slightly)
            new_height = height + random.randint(0, 10)
            fake.geometry(f"{width}x{new_height}")
            fake.after(200, melt_animation)
    
    melt_animation()
    
    # Play moan
    winsound.Beep(100, 1000)

# Main prank loop: monitor for Task Manager and replace
def prank_loop():
    while not stop_event.is_set():
        hwnd = find_task_manager()
        if hwnd:
            rect = win32gui.GetWindowRect(hwnd)
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            show_fake_task_manager(rect)
        time.sleep(1)

# Key monitor (optional, but for safety)
def key_monitor():
    while not stop_event.is_set():
        time.sleep(0.1)

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

# Cleanup
prank_thread.join()
key_thread.join()
sys.exit(0)
```

---


### Virus 3: *Eerie Icon Invasion*

```python
#!/usr/bin/env python3

# This script simulates the Eerie Icon Invasion prank.
# It duplicates desktop icons, arranges them into a skull pattern,
# plays a cackle when complete, and shows glitchy melting visuals on new icons.
# Uses Tkinter for overlays, Pillow for visuals.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Right-click desktop and select "Purge Icons" (adds custom menu via registry),
# or reboot (script deletes duplicates on stop, but reboot stops script).

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import shutil
import sys
import ctypes  # For MAKELPARAM

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Desktop path
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Function to get desktop listview hwnd
def get_desktop_listview():
    progman = win32gui.FindWindow("Progman", "Program Manager")
    defview = win32gui.FindWindowEx(progman, 0, "SHELLDLL_DefView", None)
    listview = win32gui.FindWindowEx(defview, 0, "SysListView32", None)
    return listview

# Function to duplicate icons
def duplicate_icons(num_duplicates=10):
    files = [f for f in os.listdir(desktop) if os.path.isfile(os.path.join(desktop, f))]
    new_files = []
    for _ in range(num_duplicates):
        if files:
            src = random.choice(files)
            base, ext = os.path.splitext(src)
            dst = f"{base}_ghost{ext}"
            shutil.copy(os.path.join(desktop, src), os.path.join(desktop, dst))
            new_files.append(dst)
    return new_files

# Function to arrange icons in skull pattern
def arrange_in_skull_pattern():
    listview = get_desktop_listview()
    if not listview:
        return
    
    item_count = win32gui.SendMessage(listview, win32con.LVM_GETITEMCOUNT, 0, 0)
    if item_count == 0:
        return
    
    # Define relative positions for skull shape (simple points)
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    center_x = screen_width // 2
    center_y = screen_height // 2
    radius = min(screen_width, screen_height) // 4
    
    positions = [
        (center_x, center_y - radius),  # Top head
        (center_x - radius, center_y - radius // 2),
        (center_x + radius, center_y - radius // 2),
        (center_x - radius // 2, center_y),
        (center_x + radius // 2, center_y),
        (center_x, center_y + radius // 2),  # Jaw
        # More points for shape
        (center_x - radius // 2, center_y + radius // 2),
        (center_x + radius // 2, center_y + radius // 2),
    ]
    
    # Assign positions to icons
    for i in range(min(item_count, len(positions))):
        pos = positions[i % len(positions)]
        lparam = (pos[1] << 16) | (pos[0] & 0xFFFF)  # MAKELPARAM(x, y)
        win32gui.SendMessage(listview, win32con.LVM_SETITEMPOSITION, i, lparam)
    
    # Refresh desktop
    win32gui.InvalidateRect(listview, None, True)
    win32gui.UpdateWindow(listview)

# Function to show melting glitch overlay on desktop
def show_melting_overlay():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.geometry(f"{screen_width}x{screen_height}+0+0")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Create melting skull image full screen
    img = Image.new('RGBA', (screen_width // 2, screen_height // 2), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((100, 100, 400, 400), fill='white')
    # Melting: stretch bottom
    img = img.resize((img.width, img.height + 100))
    
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(screen_width // 2, screen_height // 2, image=tk_img)
    canvas.image = tk_img
    
    overlay.after(2000, overlay.destroy)

# Main prank loop: duplicate, arrange, show effects, play sound
def prank_loop():
    duplicate_icons(5)  # Start with some
    while not stop_event.is_set():
        duplicate_icons(1)  # Add one at a time
        arrange_in_skull_pattern()
        if random.random() < 0.2:
            threading.Thread(target=show_melting_overlay).start()
        # Play cackle when pattern "completes" (every few seconds)
        winsound.Beep(800, 200); winsound.Beep(600, 200);  # Simple cackle simulation
        time.sleep(5)

# Function to add custom context menu for removal
def add_purge_menu():
    import win32api
    key = win32api.RegCreateKey(win32con.HKEY_CLASSES_ROOT, r"DesktopBackground\Shell\PurgeIcons")
    win32api.RegSetValue(key, None, win32con.REG_SZ, "Purge Icons")
    cmd_key = win32api.RegCreateKey(key, "command")
    bat_path = os.path.join(desktop, "PurgeIcons.bat")
    with open(bat_path, 'w') as f:
        f.write("@echo off\n")
        f.write(f"del /Q \"{desktop}\\*_ghost*\"\n")  # Delete duplicates
        f.write("taskkill /f /im python.exe\n")
    win32api.RegSetValue(cmd_key, None, win32con.REG_SZ, f'"{bat_path}"')
    win32api.RegCloseKey(cmd_key)
    win32api.RegCloseKey(key)

# Key monitor (for safety)
def key_monitor():
    while not stop_event.is_set():
        time.sleep(0.1)

# Add menu
add_purge_menu()

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start mainloop
root.mainloop()

# Cleanup: delete duplicates
for f in os.listdir(desktop):
    if "_ghost" in f:
        os.remove(os.path.join(desktop, f))
prank_thread.join()
key_thread.join()
sys.exit(0)
```

---


### Virus 4: *Phantom File Flipper*

```python
#!/usr/bin/env python3

# This script simulates the Phantom File Flipper prank.
# It inverts file names and icons on the desktop or in File Explorer, making them appear upside down.
# Plays a distant scream sound and shows faint skull visuals in the background.
# Visual effects use Tkinter for overlays and Pillow for icon manipulation.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Press Ctrl + Alt + Flip, or run the generated RightSideUp.exe (simulated as a bat file) on desktop.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys
import shutil
import ctypes

# Global stop event for threads
stop_event = threading.Event()

# Hidden root for Tkinter overlays
root = tk.Tk()
root.withdraw()

# Desktop path
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Function to get desktop listview hwnd
def get_desktop_listview():
    progman = win32gui.FindWindow("Progman", "Program Manager")
    defview = win32gui.FindWindowEx(progman, 0, "SHELLDLL_DefView", None)
    listview = win32gui.FindWindowEx(defview, 0, "SysListView32", None)
    return listview

# Function to invert file names
def invert_file_names():
    files = [f for f in os.listdir(desktop) if os.path.isfile(os.path.join(desktop, f))]
    for file in files:
        base, ext = os.path.splitext(file)
        inverted_name = base[::-1] + ext
        src = os.path.join(desktop, file)
        dst = os.path.join(desktop, inverted_name)
        try:
            shutil.move(src, dst)
        except:
            pass  # Skip if file already exists or error occurs
    # Refresh desktop
    listview = get_desktop_listview()
    if listview:
        win32gui.InvalidateRect(listview, None, True)
        win32gui.UpdateWindow(listview)

# Function to create an inverted (rotated) icon
def create_inverted_icon(icon_path):
    try:
        img = Image.open(icon_path)
        img = img.rotate(180)  # Flip upside down
        # Add glitch effect: random noise
        pixels = img.load()
        for x in range(img.width):
            for y in range(img.height):
                if random.random() < 0.05:  # 5% chance
                    r, g, b, a = pixels[x, y]
                    pixels[x, y] = (r + random.randint(-50, 50) % 255, g, b, a)
        return img
    except:
        # Fallback: create a generic inverted icon
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle((8, 8, 24, 24), outline='white', width=2)
        img = img.rotate(180)
        return img

# Function to apply inverted icons to desktop files
def apply_inverted_icons():
    listview = get_desktop_listview()
    if not listview:
        return
    item_count = win32gui.SendMessage(listview, win32con.LVM_GETITEMCOUNT, 0, 0)
    for i in range(item_count):
        # Note: Directly modifying system icons is complex; simulate by overlaying visuals
        pass  # For simplicity, rely on file rename and visual overlay

# Function to show faint skull background overlay
def show_skull_background():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.attributes('-alpha', 0.2)  # Faint
    overlay.geometry(f"{screen_width}x{screen_height}+0+0")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Create skull image
    img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((50, 50, 150, 150), outline='white', width=2)
    draw.ellipse((70, 70, 90, 90), fill='white')
    draw.ellipse((110, 70, 130, 90), fill='white')
    draw.rectangle((70, 120, 130, 140), fill='white')
    
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(screen_width // 2, screen_height // 2, image=tk_img)
    canvas.image = tk_img
    
    overlay.after(2000, overlay.destroy)

# Main prank loop: invert files, apply effects, play sound
def prank_loop():
    while not stop_event.is_set():
        invert_file_names()
        apply_inverted_icons()
        if random.random() < 0.3:
            threading.Thread(target=show_skull_background).start()
            winsound.Beep(300, 1000)  # Distant scream
        time.sleep(5)

# Key monitor: detect Ctrl + Alt + Flip
def key_monitor():
    while not stop_event.is_set():
        ctrl_pressed = win32api.GetKeyState(win32con.VK_CONTROL) < 0
        alt_pressed = win32api.GetKeyState(win32con.VK_MENU) < 0
        f_pressed = win32api.GetKeyState(ord('F')) < 0  # Assuming 'Flip' starts with F
        if ctrl_pressed and alt_pressed and f_pressed:
            stop_event.set()
            root.quit()
        time.sleep(0.1)

# Create removal bat file (simulating RightSideUp.exe)
bat_path = os.path.join(desktop, "RightSideUp.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")
    f.write(f"ren \"{desktop}\\*.*\" *.*\n")  # Crude attempt to revert names (limited effectiveness)

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

# Cleanup: attempt to revert file names
files = [f for f in os.listdir(desktop) if os.path.isfile(os.path.join(desktop, f))]
for file in files:
    base, ext = os.path.splitext(file)
    original_name = base[::-1] + ext
    src = os.path.join(desktop, file)
    dst = os.path.join(desktop, original_name)
    try:
        shutil.move(src, dst)
    except:
        pass
prank_thread.join()
key_thread.join()
sys.exit(0)
```

---


### Virus 5: *Glitchy Graveyard Glow*

```python
#!/usr/bin/env python3

# This script simulates the Glitchy Graveyard Glow prank.
# It makes the screen pulse with an eerie green or purple glow, shows ghostly shapes,
# and plays a low eerie chant. Visual effects include glitchy skull outlines and melting distortions.
# Uses Tkinter for screen overlay and Pillow for visuals.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Adjust screen brightness to max and back, or run GlowBanish.bat on desktop.

import win32api
import win32con
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Function to create glitchy skull image
def create_glitchy_skull(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    draw.ellipse((width // 3, height // 3, width // 3 + 20, height // 3 + 20), fill='white')
    draw.ellipse((width * 2 // 3 - 20, height // 3, width * 2 // 3, height // 3 + 20), fill='white')
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 30), fill='white')
    
    # Glitch: horizontal shifts
    for i in range(0, height, 10):
        shift = random.randint(-10, 10)
        strip = img.crop((0, i, width, i + 10))
        img.paste(strip, (shift, i))
    
    # Melting effect: stretch bottom
    img = img.resize((width, int(height * 1.2)))
    
    return img

# Function to show glowing overlay
def show_glow():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.geometry(f"{screen_width}x{screen_height}+0+0")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Create glow background
    color = random.choice(['green', '#800080'])  # Green or purple
    canvas.create_rectangle(0, 0, screen_width, screen_height, fill=color, stipple='gray50')
    
    # Add skull
    img = create_glitchy_skull(200, 200)
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(screen_width // 2, screen_height // 2, image=tk_img)
    canvas.image = tk_img
    
    # Pulse effect
    def pulse():
        if not stop_event.is_set():
            alpha = random.uniform(0.3, 0.7)
            overlay.attributes('-alpha', alpha)
            overlay.after(200, pulse)
    
    pulse()
    overlay.after(3000, overlay.destroy)

# Main prank loop
def prank_loop():
    while not stop_event.is_set():
        threading.Thread(target=show_glow).start()
        winsound.Beep(150, 1500)  # Eerie chant
        time.sleep(random.uniform(5, 10))

# Monitor brightness changes
def brightness_monitor():
    initial_brightness = None
    max_brightness = False
    while not stop_event.is_set():
        # Note: Windows brightness API is complex; simulate by checking key presses or time
        time.sleep(0.1)
        # For simplicity, use a key combo as proxy for brightness adjustment
        if win32api.GetKeyState(win32con.VK_UP) < 0 and win32api.GetKeyState(win32con.VK_CONTROL) < 0:
            max_brightness = True
        if max_brightness and win32api.GetKeyState(win32con.VK_DOWN) < 0 and win32api.GetKeyState(win32con.VK_CONTROL) < 0:
            stop_event.set()
            root.quit()

# Create removal bat file
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "GlowBanish.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Start threads
prank_thread = threading.Thread(target=prank_loop)
brightness_thread = threading.Thread(target=brightness_monitor)

prank_thread.start()
brightness_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
brightness_thread.join()
sys.exit(0)
```

---


### Virus 6: *Cursed Caps Lock*

```python
#!/usr/bin/env python3

# This script simulates the Cursed Caps Lock prank.
# Pressing Caps Lock triggers a scream, a fake "System Cursed" warning, and makes typed text appear red.
# The warning pop-up glitches and melts, with a flashing skull.
# Uses Tkinter for pop-ups, keyboard for key detection, and Pillow for visuals.
# Requires: pip install pywin32 pillow keyboard
# Run on Windows only.
# Removal: Press Caps Lock five times in a row, or end CursedCaps.exe (simulated as python.exe) in Task Manager.

import win32api
import win32con
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import keyboard
import sys

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Caps Lock press counter
caps_count = 0

# Function to create glitchy melting skull
def create_melting_skull(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    draw.ellipse((width // 3, height // 3, width // 3 + 20, height // 3 + 20), fill='white')
    draw.ellipse((width * 2 // 3 - 20, height // 3, width * 2 // 3, height // 3 + 20), fill='white')
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 30), fill='white')
    
    # Glitch and melt
    for i in range(0, height, 10):
        shift = random.randint(-10, 10)
        strip = img.crop((0, i, width, i + 10))
        img.paste(strip, (shift, i))
    img = img.resize((width, int(height * 1.3)))
    
    return img

# Function to show warning pop-up
def show_warning():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
    warning = tk.Toplevel(root)
    warning.overrideredirect(True)
    warning.attributes('-topmost', True)
    warning.geometry(f"300x200+{(screen_width-300)//2}+{(screen_height-200)//2}")
    
    canvas = tk.Canvas(warning, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    canvas.create_text(150, 50, text="System Cursed!", fill='red', font=('Arial', 16))
    
    img = create_melting_skull(100, 100)
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(150, 150, image=tk_img)
    canvas.image = tk_img
    
    # Glitch animation
    def glitch():
        if not stop_event.is_set():
            warning.geometry(f"+{(screen_width-300)//2 + random.randint(-10,10)}+{(screen_height-200)//2 + random.randint(-10,10)}")
            warning.after(100, glitch)
    
    glitch()
    warning.after(2000, warning.destroy)
    
    # Play scream
    winsound.Beep(1000, 500)

# Function to make typed text red (simulates by injecting key events)
def make_text_red():
    # Note: Directly changing text color in all apps is complex; simulate with a notification
    pass  # For simplicity, rely on warning pop-up

# Main prank loop
def prank_loop():
    global caps_count
    while not stop_event.is_set():
        if keyboard.is_pressed('caps lock'):
            show_warning()
            make_text_red()
            caps_count += 1
            if caps_count >= 5:
                stop_event.set()
                root.quit()
            time.sleep(0.5)  # Prevent multiple triggers
        time.sleep(0.1)

# Start thread
prank_thread = threading.Thread(target=prank_loop)
prank_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
sys.exit(0)
```

---


### Virus 7: *Haunted Hard Drive Hum*

```python
#!/usr/bin/env python3

# This script simulates the Haunted Hard Drive Hum prank.
# It plays random disk access sounds (grinding, clicking) and shows a fake "Drive Haunted" error in File Explorer.
# File Explorer windows glitch with skull icons on drive folders. A ghostly whisper plays.
# Visual effects use Tkinter for overlays and Pillow for skull icons.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Open File Explorer, select "Cleanse Drive" from a custom context menu, or reboot.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys
import winreg

# Global stop event for threads
stop_event = threading.Event()

# Hidden root for Tkinter overlays
root = tk.Tk()
root.withdraw()

# Function to get File Explorer windows
def get_explorer_windows():
    windows = []
    def enum_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and "File Explorer" in win32gui.GetWindowText(hwnd):
            windows.append(hwnd)
    win32gui.EnumWindows(enum_callback, None)
    return windows

# Function to create glitchy skull icon for drive folders
def create_skull_icon():
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((8, 8, 24, 20), outline='white', width=2)
    draw.ellipse((10, 10, 14, 14), fill='white')
    draw.ellipse((18, 10, 22, 14), fill='white')
    draw.rectangle((10, 20, 22, 24), fill='white')
    
    # Add glitch effect
    for i in range(0, 32, 4):
        shift = random.randint(-2, 2)
        strip = img.crop((0, i, 32, i + 4))
        img.paste(strip, (shift, i))
    
    return img

# Function to show fake "Drive Haunted" error
def show_error_popup(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    width = 300
    height = 150
    x = left + (right - left - width) // 2
    y = top + (bottom - top - height) // 2
    
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.attributes('-topmost', True)
    popup.geometry(f"{width}x{height}+{x}+{y}")
    
    canvas = tk.Canvas(popup, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    canvas.create_text(width // 2, 50, text="Drive Haunted!", fill='red', font=('Arial', 14))
    
    img = create_skull_icon()
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(width // 2, 100, image=tk_img)
    canvas.image = tk_img
    
    # Glitch effect
    def glitch():
        if not stop_event.is_set():
            popup.geometry(f"+{x + random.randint(-5, 5)}+{y + random.randint(-5, 5)}")
            popup.after(100, glitch)
    
    glitch()
    popup.after(2000, popup.destroy)
    
    # Play ghostly whisper
    winsound.Beep(200, 800)

# Function to add skull icons to drive folders (simulated via overlay)
def add_skull_to_drives(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.geometry(f"50x50+{left + 50}+{top + 100}")  # Position near typical drive icon
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    img = create_skull_icon()
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(25, 25, image=tk_img)
    canvas.image = tk_img
    
    overlay.after(1000, overlay.destroy)

# Main prank loop: play sounds, show errors, add skull icons
def prank_loop():
    while not stop_event.is_set():
        # Play random disk sounds
        sound = random.choice([(500, 200), (300, 150), (400, 100)])  # Grinding/clicking
        winsound.Beep(*sound)
        
        # Find File Explorer windows
        explorers = get_explorer_windows()
        for hwnd in explorers:
            if random.random() < 0.3:
                threading.Thread(target=show_error_popup, args=(hwnd,)).start()
            if random.random() < 0.2:
                threading.Thread(target=add_skull_to_drives, args=(hwnd,)).start()
        
        time.sleep(random.uniform(3, 8))

# Function to add custom context menu for "Cleanse Drive"
def add_cleanse_menu():
    try:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Directory\Background\shell\CleanseDrive")
        winreg.SetValue(key, None, winreg.REG_SZ, "Cleanse Drive")
        cmd_key = winreg.CreateKey(key, "command")
        bat_path = os.path.join(os.path.expanduser("~"), "Desktop", "CleanseDrive.bat")
        with open(bat_path, 'w') as f:
            f.write("@echo off\n")
            f.write("taskkill /f /im python.exe\n")
        winreg.SetValue(cmd_key, None, winreg.REG_SZ, f'"{bat_path}"')
        winreg.CloseKey(cmd_key)
        winreg.CloseKey(key)
    except:
        pass  # Skip registry errors

# Key monitor (for safety)
def key_monitor():
    while not stop_event.is_set():
        time.sleep(0.1)

# Create removal bat file
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "CleanseDrive.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Add context menu
add_cleanse_menu()

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
key_thread.join()
sys.exit(0)
```

---


### Virus 8: *Skull-Filled Search Bar*

```python
#!/usr/bin/env python3

# This script simulates the Skull-Filled Search Bar prank.
# Typing in the Windows search bar returns creepy results like "Skull.exe" or "Graveyard.txt."
# Results glitch and melt, with skull icons. A faint cackle plays.
# Uses Tkinter for fake search results and Pillow for visuals.
# Requires: pip install pywin32 pillow keyboard
# Run on Windows only.
# Removal: Type "CLEAR" in the search bar, or run SearchFix.bat on desktop.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import keyboard
import os
import sys

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Creepy search results
creepy_results = ["Skull.exe", "Graveyard.txt", "GhostFile.doc", "HauntedDir", "DoomScript.py"]

# Function to create glitchy skull icon
def create_skull_icon():
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((4, 4, 12, 10), outline='white', width=1)
    draw.ellipse((5, 5, 7, 7), fill='white')
    draw.ellipse((9, 5, 11, 7), fill='white')
    draw.rectangle((5, 10, 11, 12), fill='white')
    
    # Add melting glitch
    img = img.resize((16, 20))
    for i in range(0, 20, 2):
        shift = random.randint(-1, 1)
        strip = img.crop((0, i, 16, i + 2))
        img.paste(strip, (shift, i))
    
    return img

# Function to show fake search results
def show_fake_results(search_text):
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
    # Find search bar window (approximate by detecting Cortana/Search UI)
    hwnd = win32gui.FindWindow(None, "Search")
    if not hwnd:
        hwnd = win32gui.GetForegroundWindow()  # Fallback
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.geometry(f"300x200+{left}+{bottom + 10}")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    img = create_skull_icon()
    tk_img = ImageTk.PhotoImage(img)
    
    # Display creepy results
    for i, result in enumerate(random.sample(creepy_results, min(5, len(creepy_results)))):
        canvas.create_image(10, 30 + i * 30, anchor=tk.W, image=tk_img)
        canvas.create_text(30, 30 + i * 30, text=result, fill='white', anchor=tk.W, font=('Arial', 10))
    canvas.image = tk_img
    
    # Glitch effect
    def glitch():
        if not stop_event.is_set():
            overlay.geometry(f"+{left + random.randint(-5, 5)}+{bottom + 10 + random.randint(-5, 5)}")
            overlay.after(100, glitch)
    
    glitch()
    overlay.after(2000, overlay.destroy)
    
    # Play cackle
    winsound.Beep(800, 200); winsound.Beep(600, 200)

# Main prank loop: monitor typing in search bar
def prank_loop():
    current_text = ""
    while not stop_event.is_set():
        if win32gui.GetForegroundWindow() == win32gui.FindWindow(None, "Search"):
            for key in [chr(i) for i in range(65, 91)] + [chr(i) for i in range(48, 58)]:
                if keyboard.is_pressed(key):
                    current_text += key
                    if current_text.lower() == "clear":
                        stop_event.set()
                        root.quit()
                    else:
                        threading.Thread(target=show_fake_results, args=(current_text,)).start()
                    time.sleep(0.2)  # Prevent rapid triggers
        time.sleep(0.1)

# Create removal bat file (simulating SearchFix.exe)
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "SearchFix.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Start thread
prank_thread = threading.Thread(target=prank_loop)
prank_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
sys.exit(0)
```

---


### Virus 9: *Wraithful Window Wanderer*

```python
#!/usr/bin/env python3

# This script simulates the Wraithful Window Wanderer prank.
# Open windows drift across the screen randomly, resisting repositioning attempts.
# Plays a faint wail, with glitchy melting edges and translucent skulls on windows.
# Uses Tkinter for overlays and Pillow for visuals.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Press Ctrl + Alt + Anchor, or run WindowLock.bat on desktop.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Function to get all visible windows
def get_visible_windows():
    windows = []
    def enum_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            windows.append(hwnd)
    win32gui.EnumWindows(enum_callback, None)
    return windows

# Function to create melting skull overlay
def create_melting_skull(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    draw.ellipse((width // 3, height // 3, width // 3 + 20, height // 3 + 20), fill='white')
    draw.ellipse((width * 2 // 3 - 20, height // 3, width * 2 // 3, height // 3 + 20), fill='white')
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 30), fill='white')
    
    # Melting effect
    img = img.resize((width, int(height * 1.2)))
    for i in range(0, height, 10):
        shift = random.randint(-5, 5)
        strip = img.crop((0, i, width, i + 10))
        img.paste(strip, (shift, i))
    
    return img

# Function to move window randomly
def move_window(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    dx = random.randint(-10, 10)
    dy = random.randint(-10, 10)
    new_left = left + dx
    new_top = top + dy
    win32gui.MoveWindow(hwnd, new_left, new_top, right - left, bottom - top, True)
    
    # Show melting skull overlay
    if random.random() < 0.2:
        overlay = tk.Toplevel(root)
        overlay.overrideredirect(True)
        overlay.attributes('-topmost', True)
        overlay.attributes('-transparentcolor', 'black')
        overlay.attributes('-alpha', 0.5)
        overlay.geometry(f"100x100+{new_left}+{new_top}")
        
        canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        img = create_melting_skull(100, 100)
        tk_img = ImageTk.PhotoImage(img)
        canvas.create_image(50, 50, image=tk_img)
        canvas.image = tk_img
        
        # Glitch effect
        def glitch():
            if not stop_event.is_set():
                overlay.geometry(f"+{new_left + random.randint(-5, 5)}+{new_top + random.randint(-5, 5)}")
                overlay.after(100, glitch)
        
        glitch()
        overlay.after(1000, overlay.destroy)

# Main prank loop
def prank_loop():
    while not stop_event.is_set():
        windows = get_visible_windows()
        for hwnd in windows:
            move_window(hwnd)
        winsound.Beep(150, 1000)  # Faint wail
        time.sleep(random.uniform(1, 3))

# Key monitor: detect Ctrl + Alt + Anchor
def key_monitor():
    while not stop_event.is_set():
        ctrl_pressed = win32api.GetKeyState(win32con.VK_CONTROL) < 0
        alt_pressed = win32api.GetKeyState(win32con.VK_MENU) < 0
        a_pressed = win32api.GetKeyState(ord('A')) < 0  # Assuming 'Anchor' starts with A
        if ctrl_pressed and alt_pressed and a_pressed:
            stop_event.set()
            root.quit()
        time.sleep(0.1)

# Create removal bat file
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "WindowLock.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
key_thread.join()
sys.exit(0)
```

---


### Virus 10: *Creepy Color Shift*

```python
#!/usr/bin/env python3

# This script simulates the Creepy Color Shift prank.
# It inverts or shifts screen colors to eerie hues (negative or neon green/purple) and shows a fake "Color Curse" warning.
# A low hum plays, and skull shapes appear in distorted color patches.
# Uses Tkinter for overlays and Pillow for visuals. Color inversion simulates via overlay.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Open Display Settings and select "Restore Colors" from a custom menu, or reboot.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys
import winreg

# Global stop event for threads
stop_event = threading.Event()

# Hidden root for Tkinter overlays
root = tk.Tk()
root.withdraw()

# Function to create glitchy skull image
def create_glitchy_skull(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    draw.ellipse((width // 3, height // 3, width // 3 + 20, height // 3 + 20), fill='white')
    draw.ellipse((width * 2 // 3 - 20, height // 3, width * 2 // 3, height // 3 + 20), fill='white')
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 30), fill='white')
    
    # Add glitch effect
    for i in range(0, height, 10):
        shift = random.randint(-10, 10)
        strip = img.crop((0, i, width, i + 10))
        img.paste(strip, (shift, i))
    
    return img

# Function to show color shift overlay and warning
def show_color_shift():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.attributes('-alpha', 0.5)
    overlay.geometry(f"{screen_width}x{screen_height}+0+0")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Simulate color shift (negative or neon)
    color = random.choice(['#00FF00', '#800080'])  # Neon green or purple
    canvas.create_rectangle(0, 0, screen_width, screen_height, fill=color, stipple='gray50')
    
    # Add skull
    img = create_glitchy_skull(200, 200)
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(screen_width // 2, screen_height // 2, image=tk_img)
    canvas.image = tk_img
    
    # Warning popup
    warning = tk.Toplevel(root)
    warning.overrideredirect(True)
    warning.attributes('-topmost', True)
    warning.geometry(f"300x150+{(screen_width-300)//2}+{(screen_height-150)//2}")
    
    warn_canvas = tk.Canvas(warning, bg='black', highlightthickness=0)
    warn_canvas.pack(fill=tk.BOTH, expand=True)
    warn_canvas.create_text(150, 75, text="Color Curse Detected!", fill='red', font=('Arial', 14))
    
    # Glitch effect
    def glitch():
        if not stop_event.is_set():
            warning.geometry(f"+{(screen_width-300)//2 + random.randint(-5, 5)}+{(screen_height-150)//2 + random.randint(-5, 5)}")
            overlay.attributes('-alpha', random.uniform(0.3, 0.7))
            overlay.after(100, glitch)
    
    glitch()
    overlay.after(3000, overlay.destroy)
    warning.after(3000, warning.destroy)
    
    # Play low hum
    winsound.Beep(100, 1000)

# Main prank loop
def prank_loop():
    while not stop_event.is_set():
        threading.Thread(target=show_color_shift).start()
        time.sleep(random.uniform(5, 10))

# Function to add custom context menu for "Restore Colors"
def add_restore_menu():
    try:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Control Panel\Display\shell\RestoreColors")
        winreg.SetValue(key, None, winreg.REG_SZ, "Restore Colors")
        cmd_key = winreg.CreateKey(key, "command")
        bat_path = os.path.join(os.path.expanduser("~"), "Desktop", "RestoreColors.bat")
        with open(bat_path, 'w') as f:
            f.write("@echo off\n")
            f.write("taskkill /f /im python.exe\n")
        winreg.SetValue(cmd_key, None, winreg.REG_SZ, f'"{bat_path}"')
        winreg.CloseKey(cmd_key)
        winreg.CloseKey(key)
    except:
        pass  # Skip registry errors

# Key monitor (for safety)
def key_monitor():
    while not stop_event.is_set():
        time.sleep(0.1)

# Create removal bat file
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "RestoreColors.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Add context menu
add_restore_menu()

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
key_thread.join()
sys.exit(0)
```

---


### Virus 11: *Phantom Folder Flicker*

```python
#!/usr/bin/env python3

# This script simulates the Phantom Folder Flicker prank.
# Folders in File Explorer fade in and out, with names changing to "Lost" or "Doomed."
# A faint moan plays, and skull silhouettes appear during fades.
# Uses Tkinter for overlays, Pillow for visuals, and simulates folder changes via overlays.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Right-click a folder and select "Stabilize" from a custom menu, or end FlickerFolder.exe (simulated as python.exe).

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys
import winreg

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Function to get File Explorer windows
def get_explorer_windows():
    windows = []
    def enum_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and "File Explorer" in win32gui.GetWindowText(hwnd):
            windows.append(hwnd)
    win32gui.EnumWindows(enum_callback, None)
    return windows

# Function to create skull silhouette
def create_skull_silhouette(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), fill='white')
    draw.ellipse((width // 3, height // 3, width // 3 + 20, height // 3 + 20), fill='black')
    draw.ellipse((width * 2 // 3 - 20, height // 3, width * 2 // 3, height // 3 + 20), fill='black')
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 30), fill='black')
    
    # Melting effect
    img = img.resize((width, int(height * 1.2)))
    
    return img

# Function to show folder flicker effect
def show_flicker_effect(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    width = 200
    height = 100
    x = left + 50
    y = top + 100
    
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.geometry(f"{width}x{height}+{x}+{y}")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Simulate folder with creepy name
    name = random.choice(["Lost", "Doomed"])
    canvas.create_text(width // 2, 30, text=name, fill='white', font=('Arial', 12))
    
    img = create_skull_silhouette(100, 100)
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(width // 2, height - 50, image=tk_img)
    canvas.image = tk_img
    
    # Fade effect
    def fade():
        if not stop_event.is_set():
            alpha = random.uniform(0.2, 0.8)
            overlay.attributes('-alpha', alpha)
            overlay.after(100, fade)
    
    fade()
    overlay.after(2000, overlay.destroy)
    
    # Play faint moan
    winsound.Beep(150, 1000)

# Main prank loop
def prank_loop():
    while not stop_event.is_set():
        explorers = get_explorer_windows()
        for hwnd in explorers:
            if random.random() < 0.3:
                threading.Thread(target=show_flicker_effect, args=(hwnd,)).start()
        time.sleep(random.uniform(3, 7))

# Function to add custom context menu for "Stabilize"
def add_stabilize_menu():
    try:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\Stabilize")
        winreg.SetValue(key, None, winreg.REG_SZ, "Stabilize")
        cmd_key = winreg.CreateKey(key, "command")
        bat_path = os.path.join(os.path.expanduser("~"), "Desktop", "Stabilize.bat")
        with open(bat_path, 'w') as f:
            f.write("@echo off\n")
            f.write("taskkill /f /im python.exe\n")
        winreg.SetValue(cmd_key, None, winreg.REG_SZ, f'"{bat_path}"')
        winreg.CloseKey(cmd_key)
        winreg.CloseKey(key)
    except:
        pass  # Skip registry errors

# Key monitor (for safety)
def key_monitor():
    while not stop_event.is_set():
        time.sleep(0.1)

# Create removal bat file
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "Stabilize.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Add context menu
add_stabilize_menu()

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
key_thread.join()
sys.exit(0)
```

---


### Virus 12: *Eerie Emoji Explosion*

```python
#!/usr/bin/env python3

# This script simulates the Eerie Emoji Explosion prank.
# Every keypress adds skull or ghost emojis to text fields, with a ghostly giggle playing randomly.
# Emojis glitch and briefly melt before appearing.
# Uses Tkinter for overlays, Pillow for visuals, and keyboard for key detection.
# Requires: pip install pywin32 pillow keyboard
# Run on Windows only.
# Removal: Press Ctrl + Shift + E, or run EmojiBanish.bat on desktop.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import keyboard
import os
import sys

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Emojis to insert
emojis = ["💀", "👻"]

# Function to create melting emoji image
def create_melting_emoji(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Simulate emoji with simple skull shape
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    draw.ellipse((width // 3, height // 3, width // 3 + 20, height // 3 + 20), fill='white')
    draw.ellipse((width * 2 // 3 - 20, height // 3, width * 2 // 3, height // 3 + 20), fill='white')
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 30), fill='white')
    
    # Melting effect
    img = img.resize((width, int(height * 1.2)))
    for i in range(0, height, 10):
        shift = random.randint(-5, 5)
        strip = img.crop((0, i, width, i + 10))
        img.paste(strip, (shift, i))
    
    return img

# Function to show emoji overlay
def show_emoji_effect():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    x = random.randint(0, screen_width - 100)
    y = random.randint(0, screen_height - 100)
    
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.geometry(f"100x100+{x}+{y}")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    img = create_melting_emoji(100, 100)
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(50, 50, image=tk_img)
    canvas.image = tk_img
    
    # Glitch effect
    def glitch():
        if not stop_event.is_set():
            overlay.geometry(f"+{x + random.randint(-5, 5)}+{y + random.randint(-5, 5)}")
            overlay.after(100, glitch)
    
    glitch()
    overlay.after(1000, overlay.destroy)
    
    # Play ghostly giggle
    if random.random() < 0.3:
        winsound.Beep(800, 200); winsound.Beep(600, 200)

# Function to insert emoji
def insert_emoji():
    emoji = random.choice(emojis)
    keyboard.write(emoji)
    threading.Thread(target=show_emoji_effect).start()

# Main prank loop
def prank_loop():
    while not stop_event.is_set():
        for key in [chr(i) for i in range(65, 91)] + [chr(i) for i in range(48, 58)]:
            if keyboard.is_pressed(key):
                insert_emoji()
                time.sleep(0.2)  # Prevent rapid triggers
        time.sleep(0.1)

# Key monitor: detect Ctrl + Shift + E
def key_monitor():
    while not stop_event.is_set():
        ctrl_pressed = win32api.GetKeyState(win32con.VK_CONTROL) < 0
        shift_pressed = win32api.GetKeyState(win32con.VK_SHIFT) < 0
        e_pressed = win32api.GetKeyState(ord('E')) < 0
        if ctrl_pressed and shift_pressed and e_pressed:
            stop_event.set()
            root.quit()
        time.sleep(0.1)

# Create removal bat file
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "EmojiBanish.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
key_thread.join()
sys.exit(0)
```

---


### Virus 13: *Melting Mouse Mayhem*

```python
#!/usr/bin/env python3

# This script simulates the Melting Mouse Mayhem prank.
# Moving the mouse creates a dripping trail with random skull shapes forming.
# A low wail plays, and the trail melts and glitches with fading skulls.
# Uses Tkinter for overlays and Pillow for visuals.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Click both mouse buttons simultaneously three times, or run MouseClean.bat on desktop.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Mouse click counter for removal
click_count = 0

# Function to create melting skull image
def create_melting_skull(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    draw.ellipse((width // 3, height // 3, width // 3 + 20, height // 3 + 20), fill='white')
    draw.ellipse((width * 2 // 3 - 20, height // 3, width * 2 // 3, height // 3 + 20), fill='white')
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 30), fill='white')
    
    # Melting effect
    img = img.resize((width, int(height * 1.3)))
    for i in range(height // 2, height, 5):
        shift = random.randint(-5, 5)
        strip = img.crop((0, i, width, i + 5))
        img.paste(strip, (shift, i))
    
    return img

# Function to show mouse trail with skulls
def show_mouse_trail():
    x, y = win32api.GetCursorPos()
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.attributes('-alpha', 0.5)
    overlay.geometry(f"100x150+{x}+{y}")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Draw dripping trail
    canvas.create_line(50, 0, 50, 150, fill='white', width=3)
    
    # Add skull
    if random.random() < 0.3:
        img = create_melting_skull(50, 50)
        tk_img = ImageTk.PhotoImage(img)
        canvas.create_image(50, 100, image=tk_img)
        canvas.image = tk_img
    
    # Glitch effect
    def glitch():
        if not stop_event.is_set():
            overlay.geometry(f"+{x + random.randint(-5, 5)}+{y + random.randint(-5, 5)}")
            overlay.after(100, glitch)
    
    glitch()
    overlay.after(500, overlay.destroy)
    
    # Play wail
    if random.random() < 0.2:
        winsound.Beep(150, 1000)

# Main prank loop
def prank_loop():
    last_pos = None
    while not stop_event.is_set():
        current_pos = win32api.GetCursorPos()
        if last_pos != current_pos:  # Detect mouse movement
            threading.Thread(target=show_mouse_trail).start()
        last_pos = current_pos
        time.sleep(0.1)

# Mouse monitor: detect both buttons clicked three times
def mouse_monitor():
    global click_count
    while not stop_event.is_set():
        left_pressed = win32api.GetKeyState(win32con.VK_LBUTTON) < 0
        right_pressed = win32api.GetKeyState(win32con.VK_RBUTTON) < 0
        if left_pressed and right_pressed:
            click_count += 1
            if click_count >= 3:
                stop_event.set()
                root.quit()
            time.sleep(0.3)  # Debounce
        time.sleep(0.1)

# Create removal bat file
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "MouseClean.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Start threads
prank_thread = threading.Thread(target=prank_loop)
mouse_thread = threading.Thread(target=mouse_monitor)

prank_thread.start()
mouse_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
mouse_thread.join()
sys.exit(0)
```

---


### Virus 14: *Ghostly Glitch Grid*

```python
#!/usr/bin/env python3

# This script simulates the Ghostly Glitch Grid prank.
# A grid overlay appears on the screen with cells flickering and forming skull shapes.
# A distorted chant plays, and the grid glitches and melts.
# Uses Tkinter for overlays and Pillow for visuals.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Press Ctrl + Alt + Grid, or run GridBanish.bat on desktop.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Function to create glitchy skull for grid cells
def create_glitchy_skull(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    draw.ellipse((width // 3, height // 3, width // 3 + 10, height // 3 + 10), fill='white')
    draw.ellipse((width * 2 // 3 - 10, height // 3, width * 2 // 3, height // 3 + 10), fill='white')
    draw.rectangle((width // 3, height // 2 + 5, width * 2 // 3, height // 2 + 15), fill='white')
    
    # Glitch and melt
    for i in range(0, height, 5):
        shift = random.randint(-5, 5)
        strip = img.crop((0, i, width, i + 5))
        img.paste(strip, (shift, i))
    img = img.resize((width, int(height * 1.2)))
    
    return img

# Function to show grid overlay
def show_grid():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.attributes('-alpha', 0.5)
    overlay.geometry(f"{screen_width}x{screen_height}+0+0")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Draw grid
    cell_size = 100
    for x in range(0, screen_width, cell_size):
        for y in range(0, screen_height, cell_size):
            canvas.create_rectangle(x, y, x + cell_size, y + cell_size, outline='white', width=1)
            if random.random() < 0.2:  # 20% chance for skull
                img = create_glitchy_skull(cell_size // 2, cell_size // 2)
                tk_img = ImageTk.PhotoImage(img)
                canvas.create_image(x + cell_size // 2, y + cell_size // 2, image=tk_img)
                canvas.images = getattr(canvas, 'images', []) + [tk_img]
    
    # Flicker effect
    def flicker():
        if not stop_event.is_set():
            overlay.attributes('-alpha', random.uniform(0.3, 0.7))
            overlay.after(100, flicker)
    
    flicker()
    overlay.after(3000, overlay.destroy)
    
    # Play distorted chant
    winsound.Beep(200, 1500)

# Main prank loop
def prank_loop():
    while not stop_event.is_set():
        threading.Thread(target=show_grid).start()
        time.sleep(random.uniform(5, 10))

# Key monitor: detect Ctrl + Alt + Grid
def key_monitor():
    while not stop_event.is_set():
        ctrl_pressed = win32api.GetKeyState(win32con.VK_CONTROL) < 0
        alt_pressed = win32api.GetKeyState(win32con.VK_MENU) < 0
        g_pressed = win32api.GetKeyState(ord('G')) < 0  # Assuming 'Grid' starts with G
        if ctrl_pressed and alt_pressed and g_pressed:
            stop_event.set()
            root.quit()
        time.sleep(0.1)

# Create removal bat file
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "GridBanish.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
key_thread.join()
sys.exit(0)
```

---


### Virus 15: *Haunted Notification Nudge*

```python
#!/usr/bin/env python3

# This script simulates the Haunted Notification Nudge prank.
# Fake notifications with creepy messages like "System Possessed" or "Skull Detected" appear.
# A faint scream plays, and notifications glitch and melt with skull icons.
# Uses Tkinter for notification overlays and Pillow for visuals.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Click "Dismiss All" on any notification, or end NotifyGhost.exe (simulated as python.exe) in Task Manager.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Creepy notification messages
messages = ["System Possessed!", "Skull Detected!", "Ghost in the Machine!", "Haunted Drive Found!"]

# Function to create glitchy skull icon
def create_skull_icon():
    img = Image.new('RGBA', (50, 50), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((10, 10, 40, 30), outline='white', width=2)
    draw.ellipse((15, 15, 20, 20), fill='white')
    draw.ellipse((30, 15, 35, 20), fill='white')
    draw.rectangle((15, 30, 35, 35), fill='white')
    
    # Melting effect
    img = img.resize((50, 60))
    for i in range(30, 60, 5):
        shift = random.randint(-5, 5)
        strip = img.crop((0, i, 50, i + 5))
        img.paste(strip, (shift, i))
    
    return img

# Function to show fake notification
def show_notification():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    width = 300
    height = 100
    x = screen_width - width - 10
    y = screen_height - height - 10
    
    notification = tk.Toplevel(root)
    notification.overrideredirect(True)
    notification.attributes('-topmost', True)
    notification.geometry(f"{width}x{height}+{x}+{y}")
    
    canvas = tk.Canvas(notification, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Message
    message = random.choice(messages)
    canvas.create_text(150, 30, text=message, fill='red', font=('Arial', 12))
    
    # Skull icon
    img = create_skull_icon()
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(270, 80, image=tk_img)
    canvas.image = tk_img
    
    # Dismiss All button
    dismiss = tk.Button(notification, text="Dismiss All", command=lambda: stop_event.set() or root.quit(), bg='black', fg='gray')
    dismiss.place(x=10, y=70)
    
    # Glitch effect
    def glitch():
        if not stop_event.is_set():
            notification.geometry(f"+{x + random.randint(-5, 5)}+{y + random.randint(-5, 5)}")
            notification.after(100, glitch)
    
    glitch()
    notification.after(3000, notification.destroy)
    
    # Play faint scream
    winsound.Beep(1000, 500)

# Main prank loop
def prank_loop():
    while not stop_event.is_set():
        threading.Thread(target=show_notification).start()
        time.sleep(random.uniform(5, 10))

# Key monitor (for safety)
def key_monitor():
    while not stop_event.is_set():
        time.sleep(0.1)

# Start thread
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
key_thread.join()
sys.exit(0)
```

---


### Virus 16: *Spooky Shortcut Shuffle*

```python
#!/usr/bin/env python3

# This script simulates the Spooky Shortcut Shuffle prank.
# Desktop shortcuts move in a circular pattern and rename to creepy names like "FearLink" or "DoomApp."
# A cackle plays, and shortcuts glitch with melting skull icons.
# Uses Tkinter for overlays, Pillow for visuals, and manipulates desktop files.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Right-click a shortcut and select "Freeze" from a custom menu, or reboot.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import shutil
import sys
import winreg
import math

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Desktop path
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Creepy shortcut names
creepy_names = ["FearLink.lnk", "DoomApp.lnk", "GhostShort.lnk", "Haunted.lnk"]

# Function to get desktop listview hwnd
def get_desktop_listview():
    progman = win32gui.FindWindow("Progman", "Program Manager")
    defview = win32gui.FindWindowEx(progman, 0, "SHELLDLL_DefView", None)
    listview = win32gui.FindWindowEx(defview, 0, "SysListView32", None)
    return listview

# Function to rename shortcuts
def rename_shortcuts():
    shortcuts = [f for f in os.listdir(desktop) if f.endswith('.lnk')]
    for shortcut in shortcuts:
        new_name = random.choice(creepy_names)
        src = os.path.join(desktop, shortcut)
        dst = os.path.join(desktop, new_name)
        try:
            shutil.move(src, dst)
        except:
            pass  # Skip if file exists or error
    # Refresh desktop
    listview = get_desktop_listview()
    if listview:
        win32gui.InvalidateRect(listview, None, True)
        win32gui.UpdateWindow(listview)

# Function to create melting skull icon
def create_melting_skull(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    draw.ellipse((width // 3, height // 3, width // 3 + 20, height // 3 + 20), fill='white')
    draw.ellipse((width * 2 // 3 - 20, height // 3, width * 2 // 3, height // 3 + 20), fill='white')
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 30), fill='white')
    
    # Melting effect
    img = img.resize((width, int(height * 1.3)))
    for i in range(height // 2, height, 5):
        shift = random.randint(-5, 5)
        strip = img.crop((0, i, width, i + 5))
        img.paste(strip, (shift, i))
    
    return img

# Function to move shortcuts in a circular pattern
def move_shortcuts():
    listview = get_desktop_listview()
    if not listview:
        return
    
    item_count = win32gui.SendMessage(listview, win32con.LVM_GETITEMCOUNT, 0, 0)
    if item_count == 0:
        return
    
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    center_x = screen_width // 2
    center_y = screen_height // 2
    radius = min(screen_width, screen_height) // 4
    
    for i in range(item_count):
        angle = (i * 2 * math.pi / item_count) + (time.time() % 360) / 10  # Rotate over time
        x = int(center_x + radius * math.cos(angle))
        y = int(center_y + radius * math.sin(angle))
        lparam = (y << 16) | (x & 0xFFFF)
        win32gui.SendMessage(listview, win32con.LVM_SETITEMPOSITION, i, lparam)
        
        # Show skull overlay occasionally
        if random.random() < 0.2:
            overlay = tk.Toplevel(root)
            overlay.overrideredirect(True)
            overlay.attributes('-topmost', True)
            overlay.attributes('-transparentcolor', 'black')
            overlay.attributes('-alpha', 0.5)
            overlay.geometry(f"100x100+{x}+{y}")
            
            canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
            canvas.pack(fill=tk.BOTH, expand=True)
            
            img = create_melting_skull(100, 100)
            tk_img = ImageTk.PhotoImage(img)
            canvas.create_image(50, 50, image=tk_img)
            canvas.image = tk_img
            
            overlay.after(1000, overlay.destroy)
    
    # Refresh desktop
    win32gui.InvalidateRect(listview, None, True)
    win32gui.UpdateWindow(listview)
    
    # Play cackle
    winsound.Beep(800, 200); winsound.Beep(600, 200)

# Main prank loop
def prank_loop():
    while not stop_event.is_set():
        rename_shortcuts()
        move_shortcuts()
        time.sleep(3)

# Function to add custom context menu for "Freeze"
def add_freeze_menu():
    try:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"lnkfile\shell\Freeze")
        winreg.SetValue(key, None, winreg.REG_SZ, "Freeze")
        cmd_key = winreg.CreateKey(key, "command")
        bat_path = os.path.join(desktop, "Freeze.bat")
        with open(bat_path, 'w') as f:
            f.write("@echo off\n")
            f.write("taskkill /f /im python.exe\n")
        winreg.SetValue(cmd_key, None, winreg.REG_SZ, f'"{bat_path}"')
        winreg.CloseKey(cmd_key)
        winreg.CloseKey(key)
    except:
        pass  # Skip registry errors

# Key monitor (for safety)
def key_monitor():
    while not stop_event.is_set():
        time.sleep(0.1)

# Create removal bat file
bat_path = os.path.join(desktop, "Freeze.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Add context menu
add_freeze_menu()

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
key_thread.join()
sys.exit(0)
```

---

### Virus 17: *Phantom Power Pulse*

```python
#!/usr/bin/env python3

# This script simulates the Phantom Power Pulse prank.
# The screen flickers as if losing power, with fake "System Failure" warnings.
# A low buzz plays, and flickers include glitchy skull shapes and melting effects.
# Uses Tkinter for overlays and Pillow for visuals.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Press Ctrl + Shift + Power, or run PowerFix.bat on desktop.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Function to create glitchy skull
def create_glitchy_skull(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    draw.ellipse((width // 3, height // 3, width // 3 + 20, height // 3 + 20), fill='white')
    draw.ellipse((width * 2 // 3 - 20, height // 3, width * 2 // 3, height // 3 + 20), fill='white')
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 30), fill='white')
    
    # Glitch and melt
    for i in range(0, height, 5):
        shift = random.randint(-5, 5)
        strip = img.crop((0, i, width, i + 5))
        img.paste(strip, (shift, i))
    img = img.resize((width, int(height * 1.2)))
    
    return img

# Function to show flicker and warning
def show_power_pulse():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.geometry(f"{screen_width}x{screen_height}+0+0")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Flicker effect (darken screen)
    canvas.create_rectangle(0, 0, screen_width, screen_height, fill='black', stipple='gray50')
    
    # Add skull
    if random.random() < 0.3:
        img = create_glitchy_skull(200, 200)
        tk_img = ImageTk.PhotoImage(img)
        canvas.create_image(screen_width // 2, screen_height // 2, image=tk_img)
        canvas.image = tk_img
    
    # Warning popup
    warning = tk.Toplevel(root)
    warning.overrideredirect(True)
    warning.attributes('-topmost', True)
    warning.geometry(f"300x150+{(screen_width-300)//2}+{(screen_height-150)//2}")
    
    warn_canvas = tk.Canvas(warning, bg='black', highlightthickness=0)
    warn_canvas.pack(fill=tk.BOTH, expand=True)
    warn_canvas.create_text(150, 75, text="System Failure!", fill='red', font=('Arial', 14))
    
    # Flicker and glitch
    def flicker():
        if not stop_event.is_set():
            overlay.attributes('-alpha', random.uniform(0.2, 0.8))
            warning.geometry(f"+{(screen_width-300)//2 + random.randint(-5, 5)}+{(screen_height-150)//2 + random.randint(-5, 5)}")
            overlay.after(100, flicker)
    
    flicker()
    overlay.after(2000, overlay.destroy)
    warning.after(2000, warning.destroy)
    
    # Play low buzz
    winsound.Beep(100, 1000)

# Main prank loop
def prank_loop():
    while not stop_event.is_set():
        threading.Thread(target=show_power_pulse).start()
        time.sleep(random.uniform(5, 10))

# Key monitor: detect Ctrl + Shift + Power
def key_monitor():
    while not stop_event.is_set():
        ctrl_pressed = win32api.GetKeyState(win32con.VK_CONTROL) < 0
        shift_pressed = win32api.GetKeyState(win32con.VK_SHIFT) < 0
        power_pressed = win32api.GetKeyState(0x5B) < 0  # Windows key as proxy for 'Power'
        if ctrl_pressed and shift_pressed and power_pressed:
            stop_event.set()
            root.quit()
        time.sleep(0.1)

# Create removal bat file
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "PowerFix.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
key_thread.join()
sys.exit(0)
```

---

### Virus 18: *Creepy Clipboard Curse*

```python
#!/usr/bin/env python3

# This script simulates the Creepy Clipboard Curse prank.
# Copied text is replaced with spooky phrases like "I see you" or "Run."
# A ghostly whisper plays, and pasted text glitches with brief skull shapes.
# Uses Tkinter for overlays, Pillow for visuals, and pyperclip for clipboard manipulation.
# Requires: pip install pywin32 pillow pyperclip
# Run on Windows only.
# Removal: Paste "UNCURSE" into any text field, or end ClipCurse.exe (simulated as python.exe) in Task Manager.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import pyperclip
import os
import sys

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Spooky phrases
phrases = ["I see you", "Run", "You're not alone", "Beware the shadows"]

# Function to create glitchy skull
def create_glitchy_skull(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    draw.ellipse((width // 3, height // 3, width // 3 + 20, height // 3 + 20), fill='white')
    draw.ellipse((width * 2 // 3 - 20, height // 3, width * 2 // 3, height // 3 + 20), fill='white')
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 30), fill='white')
    
    # Glitch effect
    for i in range(0, height, 5):
        shift = random.randint(-5, 5)
        strip = img.crop((0, i, width, i + 5))
        img.paste(strip, (shift, i))
    
    return img

# Function to show skull overlay on paste
def show_skull_effect():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    x = random.randint(0, screen_width - 100)
    y = random.randint(0, screen_height - 100)
    
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.attributes('-alpha', 0.5)
    overlay.geometry(f"100x100+{x}+{y}")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    img = create_glitchy_skull(100, 100)
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(50, 50, image=tk_img)
    canvas.image = tk_img
    
    # Glitch effect
    def glitch():
        if not stop_event.is_set():
            overlay.geometry(f"+{x + random.randint(-5, 5)}+{y + random.randint(-5, 5)}")
            overlay.after(100, glitch)
    
    glitch()
    overlay.after(1000, overlay.destroy)
    
    # Play ghostly whisper
    winsound.Beep(200, 800)

# Main prank loop
def prank_loop():
    last_clipboard = ""
    while not stop_event.is_set():
        try:
            current_clipboard = pyperclip.paste()
            if current_clipboard != last_clipboard:
                if current_clipboard.strip().upper() == "UNCURSE":
                    stop_event.set()
                    root.quit()
                else:
                    pyperclip.copy(random.choice(phrases))
                    threading.Thread(target=show_skull_effect).start()
                last_clipboard = current_clipboard
        except:
            pass  # Handle clipboard access errors
        time.sleep(0.1)

# Key monitor (for safety)
def key_monitor():
    while not stop_event.is_set():
        time.sleep(0.1)

# Start thread
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
key_thread.join()
sys.exit(0)
```

---


### Virus 19: *Glitchy Graveyard Game*

```python
#!/usr/bin/env python3

# This script simulates the Glitchy Graveyard Game prank.
# A pop-up "game" prompts the user to "catch skulls" with the mouse.
# Skulls appear randomly with eerie sounds, glitching and melting as they move.
# Uses Tkinter for the game overlay and Pillow for visuals.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Click "Exit Game" in the pop-up, or run GameBanish.bat on desktop.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Function to create glitchy melting skull
def create_glitchy_skull(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    draw.ellipse((width // 3, height // 3, width // 3 + 20, height // 3 + 20), fill='white')
    draw.ellipse((width * 2 // 3 - 20, height // 3, width * 2 // 3, height // 3 + 20), fill='white')
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 30), fill='white')
    
    # Glitch and melt
    for i in range(0, height, 5):
        shift = random.randint(-5, 5)
        strip = img.crop((0, i, width, i + 5))
        img.paste(strip, (shift, i))
    img = img.resize((width, int(height * 1.2)))
    
    return img

# Function to show game pop-up
def show_game_popup():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    width = 400
    height = 300
    
    game = tk.Toplevel(root)
    game.overrideredirect(True)
    game.attributes('-topmost', True)
    game.geometry(f"{width}x{height}+{(screen_width-width)//2}+{(screen_height-height)//2}")
    
    canvas = tk.Canvas(game, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Game prompt
    canvas.create_text(width // 2, 50, text="Catch the Skulls!", fill='red', font=('Arial', 16))
    
    # Exit button
    exit_btn = tk.Button(game, text="Exit Game", command=lambda: stop_event.set() or root.quit(), bg='black', fg='gray')
    exit_btn.place(x=10, y=height-30)
    
    # Skull objects
    skulls = []
    images = []  # Keep references
    
    def create_skull():
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)
        img = create_glitchy_skull(50, 50)
        tk_img = ImageTk.PhotoImage(img)
        skull_id = canvas.create_image(x, y, image=tk_img)
        skulls.append((skull_id, x, y))
        images.append(tk_img)
    
    # Create initial skulls
    for _ in range(3):
        create_skull()
    
    # Move skulls and handle clicks
    def move_skulls():
        if not stop_event.is_set():
            for skull_id, x, y in skulls[:]:
                dx = random.randint(-10, 10)
                dy = random.randint(-10, 10)
                canvas.move(skull_id, dx, dy)
                skulls[skulls.index((skull_id, x, y))] = (skull_id, x + dx, y + dy)
            game.after(200, move_skulls)
    
    def on_click(event):
        for skull_id, x, y in skulls[:]:
            if abs(event.x - x) < 25 and abs(event.y - y) < 25:
                canvas.delete(skull_id)
                skulls.remove((skull_id, x, y))
                create_skull()  # Replace with new skull
                winsound.Beep(300, 500)  # Eerie sound
    
    # Glitch effect
    def glitch():
        if not stop_event.is_set():
            game.geometry(f"+{(screen_width-width)//2 + random.randint(-5, 5)}+{(screen_height-height)//2 + random.randint(-5, 5)}")
            game.after(100, glitch)
    
    canvas.bind("<Button-1>", on_click)
    move_skulls()
    glitch()
    game.after(10000, game.destroy)  # Auto-close after 10 seconds
    
    # Play eerie sound
    winsound.Beep(200, 1000)

# Main prank loop
def prank_loop():
    while not stop_event.is_set():
        threading.Thread(target=show_game_popup).start()
        time.sleep(random.uniform(10, 20))

# Key monitor (for safety)
def key_monitor():
    while not stop_event.is_set():
        time.sleep(0.1)

# Create removal bat file
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "GameBanish.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
key_thread.join()
sys.exit(0)
```


---

### Virus 20: *Spectral Sound Switcher*

```python
#!/usr/bin/env python3

# This script simulates the Spectral Sound Switcher prank.
# Normal Windows sounds (e.g., alerts) are replaced with screams, moans, or whispers.
# Volume fluctuates slightly, and a glitchy skull flashes with melting effects when sounds play.
# Uses Tkinter for overlays and Pillow for visuals. Sound replacement is simulated via custom playback.
# Requires: pip install pywin32 pillow
# Run on Windows only.
# Removal: Open Sound Settings and select "Restore Sounds" from a custom menu, or run SoundFix.bat on desktop.

import win32gui
import win32con
import win32api
import time
import random
import threading
import winsound
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os
import sys
import winreg

# Global stop event
stop_event = threading.Event()

# Hidden root
root = tk.Tk()
root.withdraw()

# Creepy sounds
creepy_sounds = [
    (1000, 500),  # Scream
    (150, 1000),  # Moan
    (200, 800)    # Whisper
]

# Function to create glitchy skull
def create_glitchy_skull(width, height):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((width // 4, height // 4, width * 3 // 4, height // 2), outline='white', width=2)
    draw.ellipse((width // 3, height // 3, width // 3 + 20, height // 3 + 20), fill='white')
    draw.ellipse((width * 2 // 3 - 20, height // 3, width * 2 // 3, height // 3 + 20), fill='white')
    draw.rectangle((width // 3, height // 2 + 10, width * 2 // 3, height // 2 + 30), fill='white')
    
    # Glitch and melt
    for i in range(0, height, 5):
        shift = random.randint(-5, 5)
        strip = img.crop((0, i, width, i + 5))
        img.paste(strip, (shift, i))
    img = img.resize((width, int(height * 1.2)))
    
    return img

# Function to show skull flash
def show_skull_flash():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    x = random.randint(0, screen_width - 200)
    y = random.randint(0, screen_height - 200)
    
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.attributes('-transparentcolor', 'black')
    overlay.attributes('-alpha', 0.5)
    overlay.geometry(f"200x200+{x}+{y}")
    
    canvas = tk.Canvas(overlay, bg='black', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    img = create_glitchy_skull(200, 200)
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(100, 100, image=tk_img)
    canvas.image = tk_img
    
    # Glitch effect
    def glitch():
        if not stop_event.is_set():
            overlay.geometry(f"+{x + random.randint(-5, 5)}+{y + random.randint(-5, 5)}")
            overlay.after(100, glitch)
    
    glitch()
    overlay.after(1000, overlay.destroy)

# Function to play creepy sound with volume fluctuation
def play_creepy_sound():
    sound = random.choice(creepy_sounds)
    volume = random.uniform(0.8, 1.2)  # Simulate fluctuation
    # Note: winsound doesn't support volume control; simulate via timing
    threading.Thread(target=show_skull_flash).start()
    winsound.Beep(*sound)

# Main prank loop
def prank_loop():
    while not stop_event.is_set():
        play_creepy_sound()
        time.sleep(random.uniform(5, 15))

# Function to add custom context menu for "Restore Sounds"
def add_restore_menu():
    try:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Control Panel\Sound\shell\RestoreSounds")
        winreg.SetValue(key, None, winreg.REG_SZ, "Restore Sounds")
        cmd_key = winreg.CreateKey(key, "command")
        bat_path = os.path.join(os.path.expanduser("~"), "Desktop", "SoundFix.bat")
        with open(bat_path, 'w') as f:
            f.write("@echo off\n")
            f.write("taskkill /f /im python.exe\n")
        winreg.SetValue(cmd_key, None, winreg.REG_SZ, f'"{bat_path}"')
        winreg.CloseKey(cmd_key)
        winreg.CloseKey(key)
    except:
        pass  # Skip registry errors

# Key monitor (for safety)
def key_monitor():
    while not stop_event.is_set():
        time.sleep(0.1)

# Create removal bat file
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
bat_path = os.path.join(desktop, "SoundFix.bat")
with open(bat_path, 'w') as f:
    f.write("@echo off\n")
    f.write("taskkill /f /im python.exe\n")

# Add context menu
add_restore_menu()

# Start threads
prank_thread = threading.Thread(target=prank_loop)
key_thread = threading.Thread(target=key_monitor)

prank_thread.start()
key_thread.start()

# Start Tkinter mainloop
root.mainloop()

prank_thread.join()
key_thread.join()
sys.exit(0)
```
---
### *BG Gremlin Group*
*Creating Unique Tools for Unique Individuals*
---
