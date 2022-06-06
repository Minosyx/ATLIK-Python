from random import randrange
import itertools
from time import time

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


def fermat(n): 
    x = cisqrt(n)
    if x**2 == n: return n
    if n % 2 == 0: return 2

    for vals in itertools.product(*mods):
        for z in range(x, n//2, skip:=min(args)):
            tmp = z
            for j in range(len(args)):
                tmp += args[j] * vals[j]
            a = tmp // skip
            y2 = a**2 - n
            if (all(cond(y2, args[k], mods[k]) for k in range(len(args)))) and (y := isqrt(y2))**2 == y2:
                return a - y

    # ify mozna rowniez wstawic na poczatku algorytmu,
    # lecz wtedy nie uzyskamy wyzszych wartosci p i q podzielnych przez wskazane nizej liczby,
    # ale za to szybciej dowiemy sie czy rzeczywiscie jest faktoryzowalna
    # ify zostaly dodane, poniewaz kod ten pozwala pominac znaczna ilosc iteracji wykorzystujac
    # przeskok rowny najmniejszej liczbie z poteg liczb pierwszych, lecz nie rozpatrujemy wtedy poprzedzajacych liczb pierwszych
    # jako potencjalnych dzielnikow
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


mods = [f(2, 3), f(3, 2)]
args = [8,9]
# dodanie do mods f(5, 2) i 25 do args skutkuje przyspieszeniem algorytmu jesli liczba jest faktoryzowalna
# jednak w przypadku liczby pierwszej liczba iteracji zwieksza sie i informacje o pierwszosci uzyskamy pozniej 
# niz przy aktualnych danych wejsciowych

cond = lambda x, prime, tab : x % prime in tab

x = randrange(10**5 + 1, 10**6, 2) # generowanie tylko liczb nieparzystych z danego przedzialu

print(x)

# do porownania wynikow uzylem dwoch innych zmodyfikowanych implementacji algorytmu Fermata, ktore znane sa ze swojej szybkosci

t = time()
print(mn_ffa(x))
print(time() - t)

t = time()
print(foe(x))
print(time() - t)

t = time()
print(fermat(x))
print(time() - t)