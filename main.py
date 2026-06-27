import math 
import time

class Liner_Congruential_Generator:
    def __init__(self):
        current_time = time.time()
        self.seed = (current_time - math.floor(current_time)) * 1000000

        self.a = 48271
        self.m = 2**31 - 1

        if self.seed == 0:
            self.seed = 2222 # random number
        else:
            self.current_x = self.seed
    
    def next_random_x(self):
        self.current_x = (self.a * self.current_x) % self.m
        return self.current_x / self.m
    
class Xorshift:
    def __init__(self):
        current_time = time.time()
        self.seed = int(current_time - math.floor(current_time)) * 1000000 & 0xFFFFFFFF

        if self.seed == 0:
            self.seed = 222222222
        else :
            self.num = self.seed
    
    def next_random_x(self):
        x = self.num
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17) & 0xFFFFFFFF
        x ^= (x << 5) & 0xFFFFFFFF
        self.num = x
        return x / 4294967296.0


