import pyautogui
import asyncio
import random

class Writer:
    def __init__(self, log_func):
        self.log_func = log_func
        self.paused = False
        self.stopped = False

    def log(self, message, error=False):
        self.log_func(message, error)

    async def write(self, text, min_delay, max_delay):
        self.stopped = False
        self.paused = False
        for line in text.strip().split("\n"):
            for char in line:
                if self.stopped:
                    return
                while self.paused:
                    if self.stopped:
                        return
                    await asyncio.sleep(0.1)
                pyautogui.typewrite(char)
                delay = random.uniform(min_delay, max_delay)
                await asyncio.sleep(delay)
            pyautogui.press("enter")
        self.log("Writing completed")

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.stopped = True
        self.paused = False