from py7 import mr
from secrets import randbelow

def gcdExtended(a, b):
    xa, ya = 1, 0
    xb, yb = 0, 1
    while b:
        q, r = divmod(a, b)
        xa, ya, xb, yb = xb, yb, xa - q * xb, ya - q * yb
        a, b = b, r
    return a, xa, ya


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def tonelli_shanks(n, p):
    if legendre(n, p) != 1:
        raise ValueError
    q = p - 1
    s = 0
    while q & 1 == 0:
        q >>= 1
        s += 1
    if s == 1:
        return ((tmp:=pow(n, (p + 1) // 4, p)), -tmp % p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = pow(t, 2, p)
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = pow(t2, 2, p)
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return (r, p - r)


def EC(a, b, n):
    
    assert n > 2
    assert (4 * (a ** 3) + 27 * (b ** 2)) % n != 0
    
    class EC:
        def __init__(self, *args):
            if len(args) == 2:
                x, y = args
                if (y**2 - x**3 - a*x - b) % n == 0:
                    self.x = x
                    self.y = y
                else:
                    raise ValueError()
            elif args == ():
                self.x = None
                self.y = None
        
        @classmethod
        def at(cls, x):
            assert x < n
            y_2 = (x ** 3 + a * x + b) % n
            y, my = tonelli_shanks(y_2, n)
            return (cls(x, y), cls(x, my))

        def __neg__(self):
            return EC(self.x, -1 * self.y % n)

        def __add__(self, other):
            if self.x is None:
                return other
            if other.x is None:
                return self
            if self.x == other.x and self.y != other.y:
                return EC()
            if self.x == other.x:
                alfa = (3 * self.x * self.x + a) * gcdExtended(2 * self.y, n)[1] % n
            else:
                alfa = (other.y - self.y) * gcdExtended(other.x - self.x, n)[1] % n
            x = (alfa * alfa - self.x - other.x) % n
            y = (alfa * (other.x - x) - other.y) % n
            return EC(x, y)
        
        def __sub__(self, other):
            return self + (-other)

        def __mul__(self, m):
            res = EC()
            A = self
            while m:
                if m & 1 == 0:
                    res += A
                A += A
                m >>= 1
            return res
        
        __rmul__ = __mul__
        
        def __str__(self):
            return f"({self.x}, {self.y})"
        
        @classmethod
        def random(cls):
            while True:
                x = randbelow(n)
                y_2 = (x ** 3 + a * x + b) % n
                try:
                    y, ym  = tonelli_shanks(y_2, n)
                    return cls(x, y)
                except:
                    pass
            
    return EC


def encode(P, public):
    ec, B, C = public
    for x in range(32 * P, 32 * (P + 1)):
        try:
            p1, p2 = ec.at(x)
            break
        except:
            pass
    else:
        raise ValueError('Nie da się zaszyfrować')
    r = randbelow(n)
    return (r * B, p1 + r * C)

def decode(dane, private):
    X1, X2 = dane
    ec, m = private
    p = X2 - m*X1
    P = p.x // 32
    return P


if __name__ == "__main__":
    N = 1
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
    public = (ec, B, C)
    private = (ec, m)
    
    P = 147
    X1, X2 = encode(P, public)
    print(X1, X2)
    R = decode((X1, X2), private)
    print(R)