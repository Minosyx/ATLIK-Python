from random import randint, randrange
import itertools
from math import prod
from time import time

def sieve(N):
    primes = [False] * 2 + [True] * (N-2)
    for i in range(2, N):
        if i * i >= N:
            return primes
        if primes[i]:
            primes[i*i::i] = [False for _ in primes[i*i::i]]
    return primes

def isqrt(N):
    def internal(N, x0):
        return x0 if (x1 := (x0**2 + N) // (2*x0)) >= x0 else internal(N, x1)
    return internal(N, N)

def cisqrt(N):
    def internal(N, x0):
        return x0 if (x1 := (x0**2 + N) // (2*x0)) >= x0 and x0 * x1 == N else x0 + 1 if x1 >= x0 else internal(N, x1)
    return internal(N, N)

def f(p, power):
	return sorted(set([x**2 % (p**power) for x in range(p**power)]))

mod64 = {0, 1, 4, 9, 16, 17, 25, 33, 36, 41, 49, 57}

def fermat(n):
    x = cisqrt(n)
    if x**2 == n: return n
    if n % 2 == 0: return 2
    y2 = x**2 - n
    for x in range(x, n//2):
        if (y := isqrt(y2))**2 == y2:
            return x - y
        y2 += 2*x + 1
    return 1

def ff(n):
    x = cisqrt(n)
    if x**2 == n: return n
    if n % 2 == 0: return 2
    y2 = x**2 - n
    while (y:= isqrt(y2))**2 != y2:
        y2 += 2*x + 1
        x += 1
    return x - y

#def fermat2(n):
#    x = cisqrt(n)
#    if x**2 == n: return n
#    if n % 2 == 0: return 2
#    y2 = x**2 - n
#    for x in range(x, n//2):
#        for vals in itertools.product(*mods):
#            z = prod(primes) * x
#            for j in range(len(primes)):
#                z += primes[len(primes) - 1 - j] * vals[j]
#            if (all(cond(z, primes[k], mods[k]) for k in range(len(primes)))) and (y := isqrt(y2))**2 == y2:
#                return x - y
#        y2 += 2*x + 1
#    return 1

def fermat2(n):
    x = cisqrt(n)
    if x**2 == n: return n
    if n % 2 == 0: return 2
    y2 = x**2 - n
    for x in range(x, n//2):
        for vals in itertools.product(*mods):
            z = prod(primes) * x
            for j in range(len(primes)):
                #z += primes[len(primes) - 1 - j] * vals[j]
                z += primes[j] * vals[j]
            if (all(cond(y2, primes[k], mods[k]) for k in range(len(primes)))) and (y := isqrt(y2))**2 == y2:
                return x - y
        y2 += 2*x + 1
    return 1

def fermat3(n): 
    x = cisqrt(n)
    if x**2 == n: return n
    if n % 2 == 0: return 2

    for vals in itertools.product(*mods):
        for z in range(x, n//2, skip:=min(primes)):
            tmp = z
            for j in range(len(primes)):
                tmp += primes[len(primes) - 1 - j] * vals[j]
            a = tmp // skip
            y2 = a**2 - n
            if (all(cond(y2, primes[k], mods[k]) for k in range(len(primes)))) and (y := isqrt(y2))**2 == y2:
                return a - y

    # if mozna rowniez wstawic na poczatku algorytmu lecz wtedy nie uzyskamy, 
    # lecz wtedy nie uzyskamy wyzszych wartosci p i q podzielnych przez wskazane nizej liczby
    if n % 3 == 0: return 3
    if n % 5 == 0: return 5
    if n % 7 == 0: return 7
    return 1

def mn_ffa(n):
    x = cisqrt(n)
    if x**2 == n: return n
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3
    if n % 5 == 0: return 5
    a, b, c = (n % 4, n % 6, n % 20)
    res = d.get((a,b,c))
    pattern = lambda x : (x % 3 == 0) == res[0] and x % 10 in res[1]
    while pattern(x) is False:
        x += 1
    y2 = x**2 - n
    while (y:=isqrt(y2))**2 != y2:
        x += 1
        while pattern(x) is False:
            x += 1
        y2 = x**2 - n
    return x - y

def foe(n):
    x = isqrt(n) + 1
    r = n % 4
    if (r == 1 and x % 2 == 0) or (r != 1 and x % 2 == 1):
        x += 1
    y2 = x**2 - n
    while (y:=isqrt(y2))**2 != y2:
        x += 2
        y2 = x**2 - n
    return x - y

d = {
    (1, 1, 1) : (False, [1,5,9]),
    (1, 1, 9) : (False, [3,5,7]),
    (1, 1, 13) : (False, [3,7]),
    (1, 1, 17) : (False, [1,9]),
    (1, 5, 1) : (True, [1,5,9]),
    (1, 5, 9) : (True, [3,5,7]),
    (1, 5, 13) : (True, [3,7]),
    (1, 5, 17) : (True, [1,9]),
    (3, 1, 3) : (False, [2,8]),
    (3, 1, 7) : (False, [4,6]),
    (3, 1, 11) : (False, [0,4,6]),
    (3, 1, 19) : (False, [0,2,8]),
    (3, 5, 3) : (True, [2,8]),
    (3, 5, 7) : (True, [4,6]),
    (3, 5, 11) : (True, [0,4,6]),
    (3, 5, 19) : (True, [0,2,8]),
    }

mods = [f(2, 3), f(3, 2)]
primes = [8,9]
#mods = [f(2, 3), f(3, 3), f(5, 2), f(7, 2), f(11, 3)]
#primes = [8,27,25,49,1331]
krotka = zip(primes, mods)
#print(*krotka)

cond = lambda x, prime, tab : x % prime in tab

#conds = any([cond(4, mods[i]) for i in range(len(primes))]) # generowanie warunkow

#print(conds)

#for val in itertools.product(*mods): # zagniezdzanie x-ow
#    print(f"{prod(primes)} * i")
#    for x in range(len(primes)):
#        print(f"{primes[x]} * {val[x]}")

x = randrange(10**5 + 1, 10**6, 2)
#x = randint(10**5, 10**6)
print(x)

#t = time()
#print(fermat(x))
#print(time() - t)

#t = time()
#print(ff(x))
#print(time() - t)

t = time()
print(mn_ffa(x))
print(time() - t)

#t = time()
#print(foe(x))
#print(time() - t)

t = time()
print(fermat3(x))
print(time() - t)

t = time()
print(fermat2(x))
print(time() - t)