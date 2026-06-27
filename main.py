import math 
import time

class Liner_Congruential_Generator:
    def __init__(self):
        current_time = time.time()
        self.seed = int((current_time - math.floor(current_time)) * 1000000)

        self.a = 48271
        self.m = 2**31 - 1

        if self.seed == 0:
            self.seed = 2222 # random number
        
        self.current_x = self.seed
    
    def next_random_x(self):
        self.current_x = (self.a * self.current_x) % self.m
        return self.current_x / self.m
    
class Xorshift:
    def __init__(self):
        current_time = time.time()
        self.seed = int((current_time - math.floor(current_time)) * 1000000) & 0xFFFFFFFF

        if self.seed == 0:
            self.seed = 222222222
        
        self.num = self.seed
    
    def next_random_x(self):
        x = self.num
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17) & 0xFFFFFFFF
        x ^= (x << 5) & 0xFFFFFFFF
        self.num = x
        return x / 4294967296.0


def run_comparison():
    n = 1000000
    lcg = Liner_Congruential_Generator()
    start_time = time.time()
    for i in range(n):
        lcg.next_random_x()
    end_time = time.time()
    lcg_time_left = end_time - start_time
    print(f'Engine LinerCongruentialGenerator Calculation Time: {lcg_time_left:4f}s')

    xor = Xorshift()
    start_time = time.time()
    for i in range(n):
        xor.next_random_x()
    end_time = time.time()
    xor_time_left = end_time - start_time
    print(f'Engine Xorvershift Calculation Time: {xor_time_left:.4f} s')

    if (xor_time_left > lcg_time_left) : 
        time_difference = ((xor_time_left - lcg_time_left) / xor_time_left) * 100
        print(f'Optimized engine : Liner Congruential Generator with {time_difference:.1f} %  of better performance')
    else :
        time_difference = ((lcg_time_left - xor_time_left) / lcg_time_left) * 100
        print(f'Optimized engine : Xorshift with {time_difference:.1f} %  of better performance')

if __name__ == "__main__" :
    run_comparison()
