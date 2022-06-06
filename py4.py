import matplotlib.pyplot as plt
from time import time

def isqrt(N, x0=None):
    x0 = N if x0 is None else x0
    return x0 if (x1 := (x0**2 + N) // (2*x0)) >= x0 else isqrt(N, x1)

def dzielnik(x):
	for i in range(2, isqrt(x) + 1):
		if x % i == 0:
			return i
	return 1

def Gaussian_Int(n):
    t = time()
    zespolone = [(a, b) for a in range(2, n) for b in range(1, a)]
    pierwsze = [
        [(a, b), (b, a)]
        for (a, b) in zespolone
        if (z2 := a ** 2 + b ** 2) % 4 == 1 and dzielnik(z2) == 1
    ]
    pierwsze = sum(pierwsze, [])
    przekatna = [(1, 1)]

    osie = [[(a, 0),(0, a)] for a in range(2, n) if a % 4 == 3 and dzielnik(a) == 1]
    osie = sum(osie, [])
    X, Y = zip(*(pierwsze + przekatna + osie))
    X = X + (x_neg := tuple(map(int.__neg__, X))) + X + x_neg
    Y = Y + Y + (y_neg :=tuple(map(int.__neg__, Y))) + y_neg

    plt.plot(X, Y, ".")
    print(time() - t)
    plt.show()


def Gaussian_sieve(N):
    assert N >= 2
    primes = [x[:] for x in [[True] * N] * N]
    primes[0][0] = False
    primes[1][0] = False
    primes[0][1] = False

    for a in range(0, N):
        for b in range(0, a + 2):
            if a ** 2 + b ** 2 > N * N:
                break
            if primes[a][b]:
                for c in range(1, (end:=N - a - b + 1)):
                    for d in range(0, end - c + 1):
                        x = a*c-b*d
                        y = a*d+b*c
                        if x >= 0 and x < N and y >= 0 and y < N and (c**2 + d**2) >= 2:
                            primes[x][y] = False
                            primes[y][x] = False
    return primes


def Gauss_plot(N):
    t = time()
    ret = Gaussian_sieve(N)
    tab = [(i, j) for i, tab in enumerate(ret) for j, _ in enumerate(tab) if ret[i][j] == True]
    X, Y = zip(*tab)
    X = X + (x_neg := tuple(map(int.__neg__, X))) + X + x_neg
    Y = Y + Y + (y_neg :=tuple(map(int.__neg__, Y))) + y_neg
    plt.plot(X, Y, ".")
    print(time() - t)
    plt.show()


Gaussian_Int(125)
Gauss_plot(125)
