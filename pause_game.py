import time
import keyboard
import threading
import cv2
import numpy as np
import win32api
import win32con
from mss import mss
from skimage.metrics import structural_similarity as ssim
from skimage import transform

# Define constants for the region
REGION_X = 500
REGION_Y = 300
REGION_WIDTH = 300
REGION_HEIGHT = 200
THRESHOLD = 0.95  # Adjust this threshold based on your needs

# Define the click function
def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# Function to continuously capture screenshots and check for changes
def screenshot_thread():
    global still_pic
    with mss() as sct:
        while not exit_flag.is_set():
            # Capture the current screenshot
            current_screenshot = np.array(sct.grab(monitor))

            # Resize the images to have the same dimensions
            current_screenshot_resized = transform.resize(current_screenshot, still_pic.shape)

            # Check for changes in the screenshot
            similarity_index = ssim(current_screenshot_resized, still_pic, multichannel=True, win_size=3, data_range=current_screenshot_resized.max() - current_screenshot_resized.min())
            if similarity_index < THRESHOLD:
                click(848, 623)
                time.sleep(0.1)  # Adjust the sleep time after each click

            # Update the still_pic with the current screenshot for the next iteration
            still_pic = current_screenshot_resized

            # Introduce a small delay between consecutive screenshot captures
            time.sleep(0.01)

# Set up initial variables
exit_flag = threading.Event()
monitor = {"top": REGION_Y, "left": REGION_X, "width": REGION_WIDTH, "height": REGION_HEIGHT}
with mss() as sct:
    still_pic = np.array(sct.grab(monitor))

# Start the screenshot thread
screenshot_thread = threading.Thread(target=screenshot_thread)
screenshot_thread.start()

# Wait for 'x' key to be pressed to exit the script
keyboard.wait('x')
exit_flag.set()
screenshot_thread.join()
