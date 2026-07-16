import math 
import time
import os
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
            u *= self.rnd.next_random_x()
            while u==0:
                u = self.rnd.next_random_x()
            p *= u
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
    

class StatisticalAnalyzer:
    def __init__(self, dist_name, dist_instance, M=100000):
        self.dist_name = dist_name
        self.dist_instance = dist_instance
        self.M = M
        self.samples = []
        # Empirical indicators
        self.empirical_mean = 0.0
        self.emprical_var = 0.0
        # Theoretical indicators
        self.theoretical_mean = 0.0
        self.theoretical_mean = 0.0
    
    def run_simulation(self):
        self.samples = [self.dist_instance.generate_sample() for i in range(self.M)]
        self._calculate_empirical_metrics()
        self._calculate_theoretical_metrics()

    def _calculate_empirical_metrics(self):
        # empirical mean
        total_sum = sum(self.samples)
        self.empirical_mean = total_sum / self.M

        # empirical variance
        sum_sq_diff = sum((x - self.empirical_mean) ** 2 for x in self.samples)
        self.empirical_var = sum_sq_diff / (self.M - 1)

    
    def _calculate_theoretical_metrics(self):

        if self.dist_name == 'Bernolli':
            p = self.dist_instance.p
            self.theoretical_mean = p
            self.theoretical_var = p * (1 - p)
        
        elif self.dist_name == 'Binomial':
            n = self.dist_instance.n
            p = self.dist_instance.p
            self.theoretical_mean = n * p
            self.theoretical_var = n * p  * (1 - p)

        elif self.dist_name == 'Geometric':
            p = self.dist_instance.p
            self.theoretical_mean = 1 / p
            self.theoretical_var = (1 - p) / (p ** 2)
        
        elif self.dist_name == 'Poisson':
            lam = self.dist_instance.lam
            self.theoretical_mean = lam
            self.theoretical_var = lam

        elif self.dist_name == 'Exponential':
            lam = self.dist_instance.lam
            self.theoretical_mean = 1 / lam
            self.theoretical_var = 1 / (lam ** 2)

        elif self.dist_name == 'Normal':
            mu = self.dist_instance.mu
            sigma = self.dist_instance.sigma
            self.theoretical_mean = mu 
            self.theoretical_var = sigma ** 2
        
    def calculate_error(self, theoretical, empirical):
        if theoretical == 0:
            return 0.0 if empirical == 0 else float('inf')
        return abs((theoretical - empirical) / theoretical) * 100
    def generate_report(self):
        mean_error = self.calculate_error(self.theoretical_mean, self.empirical_mean)
        var_error = self.calculate_error(self.theoretical_var, self.empirical_var)
        
        print("=" * 60)
        print(f" STATISTICAL ANALYSIS REPORT FOR: {self.dist_name.upper()}")
        print(f" Number of Simulations (M): {self.M:,}")
        print("=" * 60)
        
        # Mean part
        print(f" Theoretical Mean (E[X]):  {self.theoretical_mean:.6f}")
        print(f" Empirical Mean (X_bar):  {self.empirical_mean:.6f}")
        print(f" Absolute Error (Mean):    {mean_error:.4f}%")
        print("-" * 60)
        
        # varians part
        print(f" Theoretical Variance:    {self.theoretical_var:.6f}")
        print(f" Empirical Variance (S²): {self.empirical_var:.6f}")
        print(f" Absolute Error (Var):     {var_error:.4f}%")
        print("=" * 60)   

class TheoremProver:
    def __init__(self, rnd_engine):
        self.rnd = rnd_engine
        
    def _normal_cdf(self, x, mu, sigma):
        return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2.0))))
    def prove_memoryless_property(self, dist_instance, s, t, M=100000):
        print("\n" + "=" * 60)
        print(" EVALUATING MEMORYLESS PROPERTY ")
        print("=" * 60)
        
        samples = [dist_instance.generate_sample() for _ in range(M)]
        
        count_gt_t = sum(1 for x in samples if x > t)
        count_gt_s = sum(1 for x in samples if x > s)
        count_gt_s_plus_t = sum(1 for x in samples if x > (s + t))
        
        p_gt_t = count_gt_t / M
        p_gt_s = count_gt_s / M
        p_gt_s_plus_t = count_gt_s_plus_t / M
        
        if p_gt_s == 0:
            print(f"Error: No samples greater than s={s} were generated. Conditional probability cannot be calculated.")
            return
            
        p_conditional = p_gt_s_plus_t / p_gt_s
        difference = abs(p_conditional - p_gt_t)
        
        print(f" P(X > {t}) = {p_gt_t:.6f}")
        print(f" P(X > {s} + {t} | X > {s}) = {p_conditional:.6f}")
        print("-" * 60)
        print(f" Difference (Absolute Error): {difference:.6f}")
        print("=" * 60)

    def prove_binomial_normal_approximation(self, n, p, a, b, M=100000):
        print("\n" + "=" * 60)
        print(" BINOMIAL TO NORMAL APPROXIMATION THEOREM ")
        print("=" * 60)
        
        # Check standard rule of thumb for Binomial Normal Approximation
        if n < 50:
            print("Warning: For an appropriate approximation, the value of n should be at least 50.")
            
        binom_dist = Binomial(n, p, self.rnd)
        samples = [binom_dist.generate_sample() for _ in range(M)]
        
        count_in_range = sum(1 for x in samples if a <= x <= b)
        p_empirical = count_in_range / M
        
        mu = n * p
        sigma = math.sqrt(n * p * (1 - p))
        
        p_theoretical = self._normal_cdf(b + 0.5, mu, sigma) - self._normal_cdf(a - 0.5, mu, sigma)
        
        error = abs((p_theoretical - p_empirical) / p_theoretical) * 100 if p_theoretical != 0 else float('inf')
        
        print(f" Empirical P({a} <= X <= {b}) (Binomial): {p_empirical:.6f}")
        print(f" Theoretical P({a}-0.5 <= X <= {b}+0.5) (Normal): {p_theoretical:.6f}")
        print("-" * 60)
        print(f" Relative Error Percentage: {error:.4f}%")
        print("=" * 60)

    def prove_poisson_normal_approximation(self, lam, a, b, M=100000):
        print("\n" + "=" * 60)
        print(" POISSON TO NORMAL APPROXIMATION THEOREM ")
        print("=" * 60)
        
        if lam < 30:
            print("Warning: For an appropriate approximation, the value of lambda (λ) must be at least 30.")
            
        poisson_dist = Poisson(lam, self.rnd)
        samples = [poisson_dist.generate_sample() for _ in range(M)]
        
        count_in_range = sum(1 for x in samples if a <= x <= b)
        p_empirical = count_in_range / M
        
        mu = lam
        sigma = math.sqrt(lam)
        
        p_theoretical = self._normal_cdf(b + 0.5, mu, sigma) - self._normal_cdf(a - 0.5, mu, sigma)
        
        error = abs((p_theoretical - p_empirical) / p_theoretical) * 100 if p_theoretical != 0 else float('inf')
        
        print(f" Empirical P({a} <= X <= {b}) (Poisson): {p_empirical:.6f}")
        print(f" Theoretical P({a}-0.5 <= X <= {b}+0.5) (Normal): {p_theoretical:.6f}")
        print("-" * 60)
        print(f" Relative Error Percentage: {error:.4f}%")
        print("=" * 60)
green = "\033[92m"
reset = "\033[0m"
def menu():
    print(f"{green}         Welcome to Probability and Statistics sumulation Simulator Kernel{reset}")
    time.sleep(3)
    print("Running engine motor ...")
    time.sleep(3)
    os.system('cls')
    
    print("Select avtive Random Engine for Simulation ")
    print("1. Linear Congruential Generator (LCG)")
    print("2. Xorshift")
    choice = input("Enter your choice : ").strip()

    if choice == 2:
        time.sleep(3)
        os.system('cls')
        engine = Xorshift()
        print(f"{green}Active engine set to --> Xorshift{reset}")
    else : 
        time.sleep(3)
        os.system('cls')
        engine = Linear_Congruential_Generator()
        print(f"{green}Active engine set to : LCG{reset}")

    while True:
        print("======== Main Menu ========")
        print("1. Phase 1 & 2: Run Distribution Simulation & Statistical Report")
        print("2. phase 3: Evaluate Memoryless Property (Geometric / Expoential)")
        print("3. Phase 3: Binomial to Normal Approximation Theorem")
        print("4. Phase 3: Poisson to Normal Approximation Theorem")
        print("5. Exit")

        menu_choice = input("Select an option (1-5): ").strip()


        if menu_choice == '1':
            time.sleep(3)
            os.system('cls')
            print("\nSelect Distribution:")
            print("1. Bernolli\n2. Binomial\n 3. Geometric\n4. Poisson\n5. Exponential\n6. Normal")
            dist_choice =input("Choice (1-6): ").strip()
            M = int(input("Enter number of simulations : "))

            dist_instance = None
            dist_name = ""

            if dist_choice == '1':
                p = float(input("Enter p (0 < p < 1): "))
                dist_instance = Bernolli(p, engine)
                dist_name = 'Bernolli'
            elif dist_choice == '2':
                n = int(input("Enter n (Number of trials): "))
                p = float(input("Enter p (0 < p < 1): "))
                dist_instance = Binomial(n, p, engine)
                dist_name = 'Binomial'
            elif dist_choice == '3':
                p = float(input("Enter p (0 < p < 1): "))
                dist_instance - Geometric(p, engine)
                dist_name = 'Geometric'
            elif dist_choice == '4':
                lam =  float(input("Enter lambda (λ > 0) : "))
                dist_instance = Exponential(lam, engine)
                dist_name = 'Exponential'
            elif dist_choice == '6':
                mu = float(input("Enter Mean (μ) : "))
                sigma = float(input("Enter std dev (σ): "))
                dist_instance = Normal(mu, sigma, engine)
                dist_name = 'Normal'
            else:
                print("Invalid distribution selection!")
                continue

            analyzer  = StatisticalAnalyzer(dist_name, dist_instance, M)
            analyzer.run_simulation()
            analyzer.generate_report()
        
        elif menu_choice == '2':
            print("\nMemoryless Property Evaluation:")
            print("1. Geometric\n2. Exponential")
            m_choice = input("Choice (1-2): ").strip()
            s = float(input("Enter s: "))
            t = float(input("Enter t: "))
            M = int(input("Enter M (e.g. 100000): "))
            
            
            prover = TheoremProver(engine)
            if m_choice == '1':
                p = float(input("Enter p (0 < p < 1): "))
                dist = Geometric(p, engine)
            else:
                lam = float(input("Enter lambda (λ > 0): "))
                dist = Exponential(lam, engine)
                
            prover.prove_memoryless_property(dist, s, t, M)
            
        elif menu_choice == '3':
            n = int(input("Enter n (recommended >= 50): "))
            p = float(input("Enter p (0 < p < 1): "))
            a = int(input("Enter lower bound a: "))
            b = int(input("Enter upper bound b: "))
            M = int(input("Enter M: "))
            
            prover = TheoremProver(engine)
            prover.prove_binomial_normal_approximation(n, p, a, b, M)
            
        elif menu_choice == '4':
            lam = float(input("Enter lambda (λ, recommended >= 30): "))
            a = int(input("Enter lower bound a: "))
            b = int(input("Enter upper bound b: "))
            M = int(input("Enter M: "))
            
            prover = TheoremProver(engine)
            prover.prove_poisson_normal_approximation(lam, a, b, M)
            
        elif menu_choice == '5':
            print("Goodbye!")
            break
        else:
            time.sleep(2)
            print("Invalid option. Try again.")
            time.sleep(3)
            os.system('cls')

if __name__ == "__main__":
    menu()