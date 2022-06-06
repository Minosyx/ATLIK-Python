from secrets import randbelow
from random import randrange
import argparse
import pickle
from elliptic_curve import EC

def mr(n, k):
    if n in (2, 3):
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


def serialize(public, private):
    with open("public_key", "wb") as f:
        pickle.dump(public, f)
    with open("private_key", "wb") as f:
        pickle.dump(private, f)


def keygen(N):
    while True:
        n = 2**(8*N+5) + 2*randbelow(2**(8*N+4)) + 1
        if mr(n, 20) is True:
            break
    while True:
        a = randbelow(n)
        b = randbelow(n)
        if (4 * (a ** 3) + 27 * (b ** 2)) % n != 0:
            break
        
    ec = EC(a, b, n)
    B = ec.random()
    m = randbelow(n)
    C = m*B
    public = (ec, B, C, N)
    private = (ec, m, N)
    
    return (public, private)


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
