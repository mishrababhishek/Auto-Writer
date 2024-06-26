from __future__ import annotations
import pyautogui
import time
import random
from multiprocessing import Process, Value

class Writer(Process):
    def __init__(self, text, min_delay, max_delay) -> None:
        super().__init__()
        self._text: str = text
        self._miin_delay: float = min_delay
        self._max_delay: float = max_delay
        self._pause_flag = Value("b", False)
        self._exit_flag = Value("b", False)
        
    def pause(self):
        self._pause_flag.value = True
        
    def resume(self):
        self._pause_flag.value = False
        
    def stop(self):
        self._exit_flag.value = True
        self.join()
        
    def __writer(self):
        for line in self._text.strip().split("\n"):
            for char in line:
                if self._exit_flag.value:
                    return
                while self._pause_flag.value:
                    if self._exit_flag.value:
                        return
                    time.sleep(0.1)
                pyautogui.typewrite(char)
                delay = random.uniform(self._miin_delay, self._max_delay)
                time.sleep(delay)
            pyautogui.press("enter")   
    
    def run(self) -> None:
        self.__writer()
        
    @staticmethod
    def create_and_start_process(text: str, min_delay: float, max_delay: float) -> Writer:
        process = Writer(text, min_delay, max_delay)
        process.start()
        return process