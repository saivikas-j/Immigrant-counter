import matplotlib.pyplot as plt
import simpy
import random
import numpy as np
import math
import scipy.stats as stats

plane_arrival_rate = 1/60
capacity_min = 100
capacity_max = 200
local_min = 0.5
local_max = 1
foreign_min = 2
foreign_max = 3
local_len = 0
foreign_len = 0
local_arr = []
foreign_arr = []
time = []
total_time = 0
count = 0

class Local():
	def __init__(self, env, name, m):
		self.env = env
		self.name = name
		self.m = m
		self.walk_time = random.uniform(5,10)
		self.check_time = random.uniform(0.5,1.0)
		
	def local(self):
		global foreign_len,foreign_arr,local_len,local_arr,time,total_time,count
		yield env.timeout(self.walk_time)
		temp = self.env.now
		local_len = local_len + 1
		local_arr.append(local_len)
		foreign_arr.append(foreign_len)
		time.append(self.env.now)
		counter = self.m.request()
		yield counter
		total_time = total_time + self.env.now - temp		
		yield self.env.timeout(self.check_time)
		count = count + 1
		self.m.release(counter)
		local_len = local_len - 1
		local_arr.append(local_len)
		foreign_arr.append(foreign_len)
		time.append(self.env.now)
		
class Foreigner:
	def __init__(self, env, name, n):
		self.env = env
		self.name = name
		self.n = n
		self.walk_time = random.uniform(5,10)
		self.check_time = random.uniform(2.0, 3.0)
		
	def foreign(self):
		global foreign_len,foreign_arr,local_len,local_arr,time,total_time,count
		yield self.env.timeout(self.walk_time)
		temp = self.env.now
		foreign_len = foreign_len + 1
		local_arr.append(local_len)
		foreign_arr.append(foreign_len)
		time.append(self.env.now)
		counter = self.n.request()
		yield counter
		total_time = total_time + self.env.now - temp
		yield self.env.timeout(self.check_time)
		count = count + 1
		self.n.release(counter)
		foreign_len = foreign_len - 1
		local_arr.append(local_len)
		foreign_arr.append(foreign_len)
		time.append(self.env.now)

		
class Plane:
	def __init__(self, name):
		self.capacity = random.randint(100,200)
		self.num_foreigner =  self.capacity // 3
		self.num_local = self.capacity - self.num_foreigner
		self.name = name

def plane_arrival(env,plane_arrival_rate,m,n):
	flag = 0
	while True:
		flag = flag + 1
		p = Plane(flag)
		for i in range(1, p.num_local + 1):
			name = "Plane "+str(flag)+"-local "+str(i)
			l = Local(env, name, m)
			env.process(l.local())
		for j in range(1, p.num_foreigner + 1):
			name = "Plane "+str(flag)+"-foreigner "+str(j)
			f = Foreigner(env, name, n)
			env.process(f.foreign())
		inter_arrival_time = random.expovariate(plane_arrival_rate)
		yield env.timeout(inter_arrival_time)

env = simpy.Environment()
m = simpy.Resource(env, capacity = int(input("Enter number of local counters:")))
n = simpy.Resource(env, capacity = int(input("Enter number of foreign counters:")))

env.process(plane_arrival(env,plane_arrival_rate,m,n))

env.run(until = 1440)

plt.plot(time,local_arr,label = "locals")
plt.plot(time,foreign_arr,label = "foreigners")
plt.show()

W = 0
number = int(input("Enter number of simulations to be made: "))
for i in range(0,number):
	total_time = 0
	count = 0
	env = simpy.Environment()
	m = simpy.Resource(env, capacity=2)
	n = simpy.Resource(env, capacity=2)
	env.process(plane_arrival(env,plane_arrival_rate,m,n))
	env.run(until = 1440)
	W = W + total_time/count

W = W / number
print("Average is",W)
