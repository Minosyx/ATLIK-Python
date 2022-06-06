from random import randrange

from py3 import dzielnik


def Miller_Rabin(n, a=None):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    q = 0
    r = n - 1
    while r & 1 == 0:
        r >>= 1
        q += 1

    a = a if a else randrange(2, n - 1)
    x = pow(a, r, n)
        
    if x == 1:
        return True
    for _ in range(q - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
        if x == 1:
            return False
    return False


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


if __name__ == '__main__':
    #x = randrange(10**5 + 1, 10**6, 2)
    #print(Miller_Rabin(11))

    n = 4
    podstawy = [2,3,5]
    while any(n <= a for a in podstawy) or dzielnik(n) == 1 or not all(Miller_Rabin(n,a) for a in podstawy):
        n += 1
    print(n)
