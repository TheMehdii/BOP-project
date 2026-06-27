import math 
import time

class Liner_Congruential_Generator:
    def __init__(self):
        current_time = time.time()
        self.seed = (current_time - math.floor(current_time)) * 1000000

        self.a = 48271
        self.m = 2**31 - 1

        if self.seed == 0:
            self.current_x = 2222 # random number
        else:
            self.current_x = self.seed
    
    def next_random_x(self):
        self.current_x = (self.a * self.current_x) % self.m
        return self.current_x / self.m