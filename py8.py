from random import randbytes, randint, randrange
from secrets import randbelow, randbits
from py1 import isqrt
from py7 import mr

def dzielnik(x):
	for i in range(2, isqrt(x) + 1):
		if x % i == 0:
			return i
	return 1

def sieve(N):
    primes = [False] * 2 + [True] * (N-2)
    for i in range(2, N):
        if i * i >= N:
            return primes
        if primes[i]:
            primes[i*i::i] = [False for _ in primes[i*i::i]]
    return primes

def gcd(a, b):
    if b > a:
        a, b = b, a
    while b:
        a, b = b, a % b
    return a


def gcdRec(a, b):
    if b > a:
        a, b = b, a
    return gcd(b, a % b) if b else a


def gcdExtended(a, b):
    xa, ya = 1, 0
    xb, yb = 0, 1
    while b:
        q, r = divmod(a, b)
        xa, ya, xb, yb = xb, yb, xa - q * xb, ya - q * yb
        a, b = b, r
    return a, xa, ya
    

def gcdExtendedRec(a, b): 
    if a == 0:  
        return b, 0, 1
    
    gcd, x1, y1 = gcdExtendedRec(b % a, a) 
     
    x = y1 - (b // a) * x1 
    y = x1 
     
    return gcd, x, y


def gcdExtendedR(a, b, xa=1, ya=0, xb=0, yb=1):
    return gcdExtendedR(b , (d:=divmod(a, b))[1], xb, yb, xa - d[0] * xb, ya - d[0] * yb) if b else (a, xa, ya)

def szyfrowanie(blok, klucz_publiczny):
    n, d = klucz_publiczny
    return pow(blok, d, n)

def deszyfrowanie(blok, klucz_prywatny):
    n, e = klucz_prywatny
    return pow(blok, e, n)

s = 'Kryptografia asymetryczna została oficjalnie wynaleziona przez cywilnych badaczy Martina Hellmana, Whitfielda Diffie w 1976 roku. Prawie równolegle prototyp podobnego systemu stworzył Ralph Merkle – w 1974 roku zaproponował algorytm wymiany kluczy nazwany puzzlami Merkle’a[1]. Dopiero pod koniec XX wieku brytyjska służba wywiadu elektronicznego GCHQ ujawniła, że pierwsza koncepcja systemu szyfrowania z kluczem publicznym została opracowana przez jej pracownika Jamesa Ellisa już w 1965 roku, a działający system stworzył w 1973 roku Clifford Cocks, również pracownik GCHQ[2]. Odkrycia te były jednak objęte klauzulą tajności do 1997 roku. Obecnie kryptografia asymetryczna jest szeroko stosowana do wymiany informacji poprzez kanały o niskiej poufności, jak np. Internet. Stosowana jest także w systemach elektronicznego uwierzytelniania, obsługi podpisów cyfrowych, do szyfrowania poczty (OpenPGP) itd.'.encode('utf-8')


# # print(gcd(14, 46))
# # print(gcdRec(14, 46))
# # print(gcdExtendedRec(14, 46))
# print(gcdExtended(5, 12))
# # print(gcdExtendedR(14, 46))

# print(list(map(ord, "Ala ma kota")))

# p = 13
# q = 23

# n = p * q
# phi = (p-1)*(q-1)

# while (ex:= gcdExtended(phi, e:= randint(2, phi - 1)))[0] != 1:
#     pass
# d = ex[2] % phi
# print(e, d, e * d % phi)

# klucz_publiczny = (n, d)
# klucz_prywatny = (n, e)



# sz = [szyfrowanie(blok, klucz_publiczny) for blok in s]
# dsz = bytes([deszyfrowanie(blok, klucz_prywatny) for blok in sz]).decode('utf-8')



# print(sz)
# print(dsz)

N = 256 # liczba bajtów w bloku
# wylosujmy liczby pierwsze p i q takie, że n > 256**N
#generujemy klucze

def keygen():
    while True:
        # p = randrange(16 ** N + 1, 2 * 16 ** N, 2)
        p = 16**N + 2*randbits(4*N-1)+1
        if mr(p, 20) is True:
            break
    while True:
        q = randrange(16 ** N + 1, 2 * 16 ** N, 2)
        if mr(q, 20) is True:
            break
    n = p * q
    phi = (p - 1) * (q - 1)
    while (ex:= gcdExtended(phi, e:= randint(2, phi - 1)))[0] != 1:
        pass
    d = ex[2] % phi
    public = (n, d)
    private = (n, e)
    return (public, private)
        
def tuple2int(t):
    if (l:=len(t)) == 1: return t[0]
    return t[0] << 8 * (l - 1) | tuple2int(t[1:])

def list2int(t): #schemat Hornera
    return list2int(t[:-1]) << 8 | t[-1] if len(t) > 1 else t[0]

def int2list(i):
    return i.to_bytes(N, 'big', signed=False)

def int2list2(i, n=N):
    # if i < 256:
    #     return [i]
    # else:
    #     x,y = divmod(i, 256)
    #     return int2list2(x) + [y]
    return [i] if n==1 else int2list2((dm := divmod(i, 256))[0], n-1) + [dm[1]]
    
def int2list3(i):
    return int2list3(i >> 8) + [i] if i >= 256 else [i]

def bytes2block(s):  #N - zmienna globalna
    return [list2int(s[N*i:N*(i+1)]) for i in range(len(s)//N)] # nie wycina pełnej Nki

def block2bytes(l):
    return b''.join([bytes(int2list2(i)) for i in l])

# from time import time

# t = time()
# print(tuple2int((11, 137, 53, 1)))
# print(time() - t)
# t = time()

# res = list2int((11, 137, 53, 1))
# print(res)
# print(block2bytes([res])) 
# print(block2bytes([res]))
# print(int2list2(res))
# print(int2list3(res))

# print(time() - t)


if __name__ == '__main__':
    if b:= len(s) % N:
        s += b' '*(N - b)

    public, private = keygen()
    # print(bytes2block(s))
    x = [szyfrowanie(i, public) for i in bytes2block(s)]
    # print(x)
    y = [deszyfrowanie(i, private) for i in x]
    s = block2bytes(y)
    print(s[:-(N - b)])
