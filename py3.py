from py1 import isqrt, cisqrt, sieve
import asyncio

def dzielnik(x):
	for i in range(2, isqrt(x) + 1):
		if x % i == 0:
			return i
	return 1


mod64 = {0, 1, 4, 9, 16, 17, 25, 33, 36, 41, 49, 57}

async def myrange(start, stop=None, step=1):
    if stop:
        range_ = range(start, stop, step)
    else:
        range_ = range(start)
    for i in range_:
        yield i
        await asyncio.sleep(0)

def f(p):
	return set([x**2 % p for x in range(p)])

def f2(p):
	return set([x**2 % (p**3) for x in range(p**3)])


def fermat(n):
	x = cisqrt(n)
	for x in range(x//64,(n+1)//2,64):
		for k in mod64:
			xw = x+k
			y2 = xw**2 - n 
			#print(f'x={xw}, y={y2}')
			if y2 == 0:
				return xw
			if (y2 & 63 in mod64) and (y := isqrt(y2))**2 == y2:
				return xw-y
	return 1


def fermat2(n):
	if (n % 2 == 0): return 2
	x = cisqrt(n)
	for jump in primes:
		for x in range(x//jump,(n+1)//2,jump):
			for index in range(len(modulos)):
				if modulos[index][0] == jump:
					for m in modulos[index][1]:
						xw = x+m
						y2 = xw**2 - n 
						#print(f'x={xw}, y={y2}')
						if y2 == 0:
							return xw
						if (y2 & (jump - 1) in modulos[index][1]) and (y := isqrt(y2))**2 == y2:
							return xw-y
	return 1

def fermat3(n):
	if (n % 2 == 0): return 2
	x = cisqrt(n)
	for jump in primes:
		for x in range(x//jump,(n+1)//2,jump**3):
			for index in range(len(modulos)):
				if modulos[index][0] == jump:
					for m in modulos[index][1]:
						xw = x+m
						y2 = xw**2 - n 
						#print(f'x={xw}, y={y2}')
						if y2 == 0:
							return xw
						if (y2 & (jump - 1) in modulos[index][1]) and (y := isqrt(y2))**2 == y2:
							return xw-y
	return 1

from time import time
from random import randint


if __name__ == '__main__':
	#x = randint(10**5,10**6)
	#x = 2*x+1
	#print(x,fermat(x))

	#print(modulos)
	#print(f(61))

	#args = sieve(3000)
	#modulos = [(x[0], f(x[0])) for x in enumerate(args) if x[1] is True] #and x[0] > 2500]
	#primes, _ = zip(*modulos)



	#print(dzielnik(9))

	#sdata = set()
	#sdata.update(*data)
	#x = randint(10**5,10**6)
	#print(x)

	##t=time()
	###print(fermat(1872929))
	###print(fermat(189521))
	##print(fermat(x))
	##print(time()-t)

	#args = sieve(10)
	#modulos = [(x[0], f(x[0])) for x in enumerate(args) if x[1] is True] #and x[0] > 2500]
	#print(modulos)
	#primes, _ = zip(*modulos)


	#t=time()
	##print(fermat(1872929))
	##print(await fermat2(189521))
	#print(fermat2(x))
	#print(time()-t)
	#print('#'*40)

	#args = sieve(10)
	#modulos = [(x[0], f2(x[0])) for x in enumerate(args) if x[1] is True] #and x[0] > 2500]
	#print(modulos)
	#primes, _ = zip(*modulos)

	#t=time()
	##print(fermat(1872929))
	##print(await fermat2(189521))
	#print(fermat2(x))
	#print(time()-t)
	#print('#'*40)
	
	#import matplotlib.pyplot as plt
	#plt.plot(*zip(*[(n,len(set([x**2 % n for x in range(n)]))) for n in range(2,65)]),'.')
	#plt.show()
	print(set([x**2 % 8 for x in range(8)]))
