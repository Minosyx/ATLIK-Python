from math import isqrt
from time import time
from random import randrange

def mr(n, k):
    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s & 1 == 0:
        r += 1
        s >>= 1
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def gcdExtended(a, b):
    xa, ya = 1, 0
    xb, yb = 0, 1
    while b:
        q, r = divmod(a, b)
        xa, ya, xb, yb = xb, yb, xa - q * xb, ya - q * yb
        a, b = b, r
    return a, xa, ya


def baby_step_giant_step(base, power, prime):
    if mr(prime, 10) is False:
        raise ValueError("Argument not a prime")
    m = isqrt(prime - 1) + 1
    hash_tab = {1: 0}
    current = 1
    for j in range(1, m):
        current = current * base % prime
        if not current in hash_tab:
            hash_tab[current] = j
    if power in hash_tab:
        return hash_tab[power]
    mul = gcdExtended(pow(base, m, prime), prime)[1] % prime
    for i in range(m):
        if power in hash_tab:
            return hash_tab[power] + i * m
        power = (power * mul) % prime
    raise ValueError('Base Error')


t = time()
print(baby_step_giant_step(5, 22, 107))
print(time() - t)