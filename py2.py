from typing import List
from py1 import sieve
import matplotlib.pyplot as plt
from math import log

"""
print(sieve(20))

x = [1,2,3,4]
y = [4,7,2,5]
plt.plot(x,y, '.')
plt.show()
"""

def pi(N):
	s = 0
	#primes = sieve(N)
	#x = list(range(N))
	#y = [s:= (s+1 if p else s) for p in primes]	
	"""
	plt.plot(x, y, '.')
	plt.show()
	"""

def li(N, dx=.001) -> 'List[List[0], List[1], ... , List[n-1]]':
	s = 0
	return [0]+[s:= s + sum(1/log(k + dx * i) * dx for i in range(1, 1000)) for k in range(N-1)]

"""
def li(n):
	return sum(1/log(i * .001) * .001 for i in range(1, 1000)) + sum(1/log(i * .001) * .001 for i in range (1001,1000))
"""
"""
primes = sieve(x)
lulz = sum(primes)
y = len(list(filter(lambda x: x is True, primes)))

plt.plot(x,y, '.')
plt.show()
"""

"""
N = 10000
#pi(100)
plt.plot(range(N), li(N), [0,0] + [n/log(n) for n in range(2,N)])
plt.show()
"""

#print(100000/log(100000) / li(100000))

pi = lambda N, s=0: [s:= (s+1 if p else s) for p in sieve(N)]

N = 100
plt.plot(range(N), pi(N), '.')
plt.plot([0,0] + [n/log(n) for n in range(2,N)])
plt.plot(li(N), 'r')
plt.show()