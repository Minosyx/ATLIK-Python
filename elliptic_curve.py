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
        return ((tmp := pow(n, (p + 1) // 4, p)), -tmp % p)
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
    return ECP(a, b, n)


class ECP:
    def __init__(self, a, b, n, *args):
        assert n > 2
        assert (4 * (a ** 3) + 27 * (b ** 2)) % n != 0
        
        self.a = a
        self.b = b
        self.n = n
        
        if len(args) == 2 and args[0] is not None and args[1] is not None:
            x, y = args
            if (y**2 - x**3 - a*x - b) % n == 0:
                self.x = x
                self.y = y
            else:
                raise ValueError()
        else:
            self.x = None
            self.y = None

    def at(self, x):
        assert x < self.n
        y_2 = (x ** 3 + self.a * x + self.b) % self.n
        y, my = tonelli_shanks(y_2, self.n)
        return (self.cr(x, y), self.cr(x, my))
    
    def cr(self, *args):
        return ECP(self.a, self.b, self.n, *args)

    def __neg__(self):
        return self.cr(self.x, -self.y % self.n) if self.y is not None else self.cr(self.x, self.y)

    def __add__(self, other):
        if self.x is None:
            return other
        if other.x is None:
            return self
        if self.x == other.x and self.y != other.y:
            return self.cr()
        if self.x == other.x:
            alfa = (3 * self.x * self.x + self.a) * \
                gcdExtended(2 * self.y, self.n)[1] % self.n
        else:
            alfa = (other.y - self.y) * \
                gcdExtended(other.x - self.x, self.n)[1] % self.n
        x = (alfa * alfa - self.x - other.x) % self.n
        y = (alfa * (other.x - x) - other.y) % self.n
        return self.cr(x, y)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, m):
        res = self.cr()
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
    
    def random(self):
        while True:
            x = randbelow(self.n)
            y_2 = (x ** 3 + self.a * x + self.b) % self.n
            try:
                y, ym = tonelli_shanks(y_2, self.n)
                return self.cr(x, y)
            except:
                pass

