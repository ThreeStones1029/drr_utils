'''
Description: this file will be used to evaulation time
version: 
Author: ThreeStones1029 221620010039@hhu.edu.cn
Date: 2023-12-28 20:47:22
LastEditors: ShuaiLei
LastEditTime: 2023-12-28 21:09:30
'''
import time


class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.start()

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def elapsed_time(self):
        if self.start_time is None:
            raise ValueError("Timer has not been started.")
        if self.end_time is None:
            raise ValueError("Timer has not been stopped.")
        return self.end_time - self.start_time
    
    def second2minute(self, second_time):
        minute_time = second_time / 60
        return minute_time
    
    def second2hour(self, second_time):
        hour_time = second_time / 3600
        return hour_time
    
    def reset(self):
        self.start_time = None
        self.end_time = None