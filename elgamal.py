from random import randbytes, randint, randrange
from secrets import randbelow, randbits
from py1 import isqrt
from py7 import mr

s = 'Kryptografia asymetryczna została oficjalnie wynaleziona przez cywilnych badaczy Martina Hellmana, Whitfielda Diffie w 1976 roku. Prawie równolegle prototyp podobnego systemu stworzył Ralph Merkle – w 1974 roku zaproponował algorytm wymiany kluczy nazwany puzzlami Merkle’a[1]. Dopiero pod koniec XX wieku brytyjska służba wywiadu elektronicznego GCHQ ujawniła, że pierwsza koncepcja systemu szyfrowania z kluczem publicznym została opracowana przez jej pracownika Jamesa Ellisa już w 1965 roku, a działający system stworzył w 1973 roku Clifford Cocks, również pracownik GCHQ[2]. Odkrycia te były jednak objęte klauzulą tajności do 1997 roku. Obecnie kryptografia asymetryczna jest szeroko stosowana do wymiany informacji poprzez kanały o niskiej poufności, jak np. Internet. Stosowana jest także w systemach elektronicznego uwierzytelniania, obsługi podpisów cyfrowych, do szyfrowania poczty (OpenPGP) itd.'.encode(
    'utf-8')


def list2int(t):  # schemat Hornera
    return list2int(t[:-1]) << 8 | t[-1] if len(t) > 1 else t[0]


def int2list(i):
    return i.to_bytes(N, 'big', signed=False)


def bytes2block(s):  # N - zmienna globalna nie wycina pełnej Nki
    return [list2int(s[N*i:N*(i+1)]) for i in range(len(s)//N)]


def block2bytes(l):
    return b''.join([bytes(int2list(i)) for i in l])


N = 4 # liczba bajtów w bloku

def keygen():
    while True:
        p = 2**(8*N-1) + 2*randbelow(2**(8*N-1)) + 1 # losowa liczba nieparzysta z przedziału [256^N/2, 256^N)
        n = 2*p + 1

        if all([mr(p, 20), mr(n, 20)]):
            print(p, n)
            break
        
    while True:
        B = randbelow(n - 2) + 2
        if pow(B, 2, n) != 1 and pow(B, p, n) != 1:
            break
            
    m = randbelow(n - 3) + 2
    C  = pow(B, m, n)
    
    public = (B, C, n)
    private = (m, n)
    
    return (public, private)


public, private = keygen()
B, C, n = public
m, n = private


sz = [(pow(B, r:=(randbelow(n - 3) + 2), n), blok * pow(C, r, n) % n) for blok in bytes2block(s)]
print(sz)
t = block2bytes([X2 *pow(X1, n - 1 - m, n) % n for X1, X2 in sz])
print(t)