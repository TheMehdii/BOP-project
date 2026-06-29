import math 
import time

class Linear_Congruential_Generator:
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
    lcg = Linear_Congruential_Generator()
    start_time = time.time()
    for i in range(n):
        lcg.next_random_x()
    end_time = time.time()
    lcg_time_left = end_time - start_time
    print(f'Engine LinearCongruentialGenerator Calculation Time: {lcg_time_left:4f}s')

    xor = Xorshift()
    start_time = time.time()
    for i in range(n):
        xor.next_random_x()
    end_time = time.time()
    xor_time_left = end_time - start_time
    print(f'Engine Xorshift Calculation Time: {xor_time_left:.4f} s')

    if (xor_time_left > lcg_time_left) : 
        time_difference = ((xor_time_left - lcg_time_left) / xor_time_left) * 100
        print(f'Optimized engine : Linear Congruential Generator with {time_difference:.1f} %  of better performance')
    else :
        time_difference = ((lcg_time_left - xor_time_left) / lcg_time_left) * 100
        print(f'Optimized engine : Xorshift with {time_difference:.1f} %  of better performance')
    


class Distribution:
    def __init__(self, rnd_engine):
        self.rnd = rnd_engine

    def generate_sample(self):
        raise NotImplementedError("This method must be used in child class")

# Discrete distributions
    
class Bernolli(Distribution):
    def __init__(self, p, rnd_engine):
        super().__init__(rnd_engine)
        self.p = p
    def generate_sample(self):
        u = self.rnd.next_random_x()
        if u < self.p :
            return 1
        else:
            return 0
        
class Binomial(Distribution):
    def __init__(self, n, p, rnd_engine):
        super().__init__(rnd_engine)
        self.p = p
        self.n = n

    def generate_sample(self):
        result = 0 
        for i in range(self.n):
            u = self.rnd.next_random_x()
            if u < self.p:
                result += 1
        return result
    

class Geometric(Distribution) :
    def __init__(self, p, rnd_engine):
        super().__init__(rnd_engine)
        self.p = p
    
    def generate_sample(self):
        i = 1
        while self.rnd.next_random_x() >= self.p:
            i += 1
        return i

class Poisson(Distribution):
    def __init__(self, lam, rnd_engine):
        super().__init__(rnd_engine)
        self.lam = lam
    
    def generate_sample(self):
        L = math.exp(-self.lam)
        k = 0
        p = 1.0
        while p > L :
            k += 1
            p *= self.rnd.next_random_x()
        return k - 1
    
# Continuous distributions

class Exponential(Distribution):
    def __init__(self, lam, rnd_engine):
        super().__init__(rnd_engine)
        self.lam = lam
    
    def generate_sample(self):
        u = self.rnd.next_random_x()
        while u == 0:
            u = self.rnd.next_random_x()
        return -math.log(1-u) / self.lam
    

class Normal(Distribution):
    def __init__(self, mu, sigma, rnd_engine):
        super().__init__(rnd_engine)
        self.mu = mu
        self.sigma = sigma

    def generate_sample(self):
        u1 = self.rnd.next_random_x()
        u2 = self.rnd.next_random_x()

        while u1 == 0:
            u1 = self.rnd.next_random_x()
        
        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        return self.mu + (z * self.sigma)

if __name__ == "__main__":
    run_comparison()
