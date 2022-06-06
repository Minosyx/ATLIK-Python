def sieve(N):
    primes = [False] * 2 + [True] * (N-2)
    for i in range(2, N):
        if i * i >= N:
            return primes
        if primes[i]:
            primes[i*i::i] = [False for _ in primes[i*i::i]]
    return primes


def isqrt(N, x0=None):
    x0 = N if x0 is None else x0
    return x0 if (x1 := (x0**2 + N) // (2*x0)) >= x0 else isqrt(N, x1)

def isqrt2(N):
    def internal(N, x0):
        return x0 if (x1 := (x0**2 + N) // (2*x0)) >= x0 else internal(N, x1)
    return internal(N, N)
    
def cisqrt(N):
    def internal(N, x0):
        return x0 if (x1 := (x0**2 + N) // (2*x0)) >= x0 and x0 * x1 == N else x0 + 1 if x1 >= x0 else internal(N, x1)
    return internal(N, N)

def cisqrtSteps(N):
    def internal(N, x0, counter):
        return (x0, counter) if (x1 := (x0**2 + N) // (2*x0)) >= x0 and x0 * x1 == N else (x0 + 1, counter) if x1 >= x0 else internal(N, x1, counter + 1)
    return internal(N, N, 1)


if __name__ == '__main__':
    #print(isqrt(100))
    #print(isqrt2(362))
    #print(cisqrt(362))
    print(cisqrtSteps(1234567890)) #log_3(N) dla duzych N

    #for i in enumerate(sieve(102)):
    #    print(i)