from secrets import randbits
from random import randint, randrange
import argparse
import pickle

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


def keygen(N):
    while True:
        p = 16**N + 2*randbits(4*N-1)+1
        if mr(p, 20) is True:
            break
    while True:
        q = 16**N + 2*randbits(4*N-1)+1
        if mr(q, 20) is True:
            break
    n = p * q
    phi = (p - 1) * (q - 1)
    while (ex := gcdExtended(phi, e := randint(2, phi - 1)))[0] != 1:
        pass
    d = ex[2] % phi
    public = (n, d, N)
    private = (n, e, N)
    return (public, private)


def serialize(public, private):
    with open("public_key", "wb") as f:
        pickle.dump(public, f)
    with open("private_key", "wb") as f:
        pickle.dump(private, f)


def pow2check():
    def is_power2(arg):
        try:
            num = int(arg)
        except ValueError:
            raise argparse.ArgumentTypeError("Must be an integer")
        if num < 2 or num & (num - 1) != 0:
            raise argparse.ArgumentTypeError("Must be a power of 2")
        else: 
            return num
    return is_power2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('N', type=pow2check(), help="liczba bajtów w bloku")
    parser.description = "Generator kluczy publicznych i prywatnych"
    parser.usage = f"{parser.prog} N"
    args = parser.parse_args()
    keys = keygen(args.N)
    serialize(*keys)

if __name__ == "__main__":
    main()