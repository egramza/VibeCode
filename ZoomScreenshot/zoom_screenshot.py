import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import os
from datetime import datetime
import keyboard  # NEW

def take_screenshot():
    screenshot = pyautogui.screenshot()
    return np.array(screenshot), screenshot

def find_border(np_img):
    target_bgr = np.array([35, 192, 136])
    lower = np.clip(target_bgr - 20, 0, 255)
    upper = np.clip(target_bgr + 20, 0, 255)

    bgr_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    mask = cv2.inRange(bgr_img, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        return x, y, w, h
    return None

def preview_and_prompt(image, x, y, w, h):
    cropped = image.crop((x, y, x + w, y + h))
    preview_img = cropped.copy()
    preview_img.thumbnail((600, 400))

    root = tk.Tk()
    root.title("Screenshot Preview")
    img_tk = ImageTk.PhotoImage(preview_img)
    label = tk.Label(root, image=img_tk)
    label.pack(padx=10, pady=10)

    def on_yes():
        root.result = True
        root.destroy()

    def on_no():
        root.result = False
        root.destroy()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Save to Pictures", command=on_yes, width=20).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Cancel", command=on_no, width=20).pack(side="right", padx=5)

    root.mainloop()
    return root.result, cropped

def save_image(cropped):
    pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
    if not os.path.exists(pictures_dir):
        os.makedirs(pictures_dir)
    filename = f"ZoomScreenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    full_path = os.path.join(pictures_dir, filename)
    cropped.save(full_path)
    print(f"Saved screenshot to {full_path}")

def run_screenshot():
    np_img, pil_img = take_screenshot()
    border_coords = find_border(np_img)
    if border_coords:
        user_confirmed, cropped_img = preview_and_prompt(pil_img, *border_coords)
        if user_confirmed:
            save_image(cropped_img)
    else:
        print("No border with target color detected.")

# 🔥 HOTKEY LISTENER
print("🟢 Script running. Press CTRL+ALT+S to capture a screenshot.")
keyboard.add_hotkey('ctrl+alt+s', run_screenshot)

# Keeps the script alive
keyboard.wait('esc')  # You can press ESC to quit
