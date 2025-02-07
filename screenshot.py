import pyautogui

def capture_screenshot():
    screenshot = pyautogui.screenshot()
    path = "screenshot.png"
    screenshot.save(path)
    print(f"Screenshot saved at: {path}")
    return path
