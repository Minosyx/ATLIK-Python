from random import randint



def fermat(p, a=None):
    return pow(a if a else randint(2, p - 1), p - 1, p) == 1

p = 65
for a in range(2, p):
    print(a, fermat(p, a))

n = 4
podstawy = [2,3,5,7]
while any(n <= a for a in podstawy) or dzielnik(n) == 1 or not all(fermat(n,a) for a in podstawy):
    n += 1
print(n)

