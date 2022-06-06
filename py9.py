from math import gcd, isqrt
from py8 import gcdExtended
from time import time

def log(b, a, n): #a podstawa
    if gcd(b, n) != 1:
        raise ValueError("Math domain error")
    wyk = 0
    pot = 1
    t = []
    for i in range(n):
        wyk += 1
        pot = (pot * a) % n
        if pot == b:
            return wyk
        if pot == 1:
            raise ValueError('Base Error')
    return -1

# for p in range(2, 23):
#     print(log(7, p, 23))
    
    
# def shanks(p, n):
#     if gcd(p, n) != 1:
#         raise ValueError('Base Error')
    
    
def shanks(base, arg, prime):
    result = 0
    N = prime - 1
    n = isqrt(N) + 1
    firstList = {1: 0}
    current = 1
    for i in range(1, n + 1):
        current = current*base % prime
        if not current in firstList:
            firstList[current] = i
    if arg in firstList:
        return firstList[arg]
    else:
        multiplier = gcdExtended(pow(base, n, prime), prime)[1] % prime
        for i in range(1, n+1):
            arg = (arg * multiplier) % prime
            if arg in firstList:
                return(firstList[arg]+n*i)
    return -1

# print(shanks(5, 2, 41))

def baby_step_giant_step(base, arg, prime):
    m = isqrt(prime - 1) + 1
    hash_tab = {1: 0}
    current = 1
    for j in range(1, m):
        current = current * base % prime
        if not current in hash_tab:
            hash_tab[current] = j
    if arg in hash_tab:
        return hash_tab[arg]
    mul = gcdExtended(pow(base, m, prime), prime)[1] % prime
    for i in range(m):
        if arg in hash_tab:
            return hash_tab[arg] + i * m
        arg = (arg * mul) % prime
    return -1

t = time()
print(shanks(7894352216, 355407489, 604604729))
print(time() - t)

t = time()
print(baby_step_giant_step(7894352216, 355407489, 604604729))
print(time() - t)