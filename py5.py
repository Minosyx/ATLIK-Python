from math import gcd, sqrt
from random import randint, randrange
import matplotlib.pyplot as plt

def rho_Pollard(n):
	if n == 1:
		return n
	if n % 2 == 0:
		return 2
		
	g = lambda x : (x ** 2 + 1) % n
	x = randint(2, n-1)
	y = g(x)
	#maxIt = 10000
	i = 1
	while True: 
		x = g(x)		# x2
		y = g(g(y))		# x4
		
		d = gcd(abs(x-y), n)
		if d != 1:
			return d, i
		i += 1
			

def analize(N, start, end, isLog=False, checkOne=False):
	prop = []
	if checkOne:
		x = randrange(start, end, 2)
	for _ in range(N):
		if not checkOne:
			x = randrange(start, end, 2)
		res, steps = rho_Pollard(x)
		if res != x and ((sq:=sqrt(res)), steps) not in prop:
			prop.append((sq, steps))

	#for item in prop:
	#	print(item[0], item[1])
	if len(prop) == 0: return

	X, ITS = zip(*prop)

	if isLog:
		plt.yscale('log')
		plt.xscale('log')
	plt.plot(X, ITS, '.')
	plt.show()

analize(10000, 10**5 + 1, 10**6)