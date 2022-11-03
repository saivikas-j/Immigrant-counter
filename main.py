# Simulation-based Measurements and Accuracy

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

def plane_arrival(env,plane_arrival_rate,m,n):
	while True:
		capacity = random.randint(100,200)
		foreigners = capacity // 3
		locals = capacity - foreigners
		for i in range(1,locals+1):
			l = local(env,i,m)
			env.process(l)
		for j in range(1,foreigners+1):
			f = foreign(env,j,n)
			env.process(f)
		inter_arrival_time = random.expovariate(plane_arrival_rate)
		yield env.timeout(inter_arrival_time)

def local(env,name,m):
		global foreign_len,foreign_arr,local_len,local_arr,time,total_time,count
		walk_time = random.uniform(5,10)
		yield env.timeout(walk_time)
		temp = env.now
		local_len = local_len + 1
		local_arr.append(local_len)
		foreign_arr.append(foreign_len)
		time.append(env.now)
		counter = m.request()
		yield counter
		total_time = total_time + env.now - temp
		check_time = random.uniform(0.5,1.0)
		yield env.timeout(check_time)
		count = count + 1
		m.release(counter)
		local_len = local_len - 1
		local_arr.append(local_len)
		foreign_arr.append(foreign_len)
		time.append(env.now)

def foreign(env,name,n):
		global foreign_len,foreign_arr,local_len,local_arr,time,total_time,count
		walk_time = random.uniform(5,10)
		yield env.timeout(walk_time)
		temp = env.now
		foreign_len = foreign_len + 1
		local_arr.append(local_len)
		foreign_arr.append(foreign_len)
		time.append(env.now)
		counter = n.request()
		yield counter
		total_time = total_time + env.now - temp
		check_time = random.uniform(2.0,3.0)
		yield env.timeout(check_time)
		count = count + 1
		n.release(counter)
		foreign_len = foreign_len - 1
		local_arr.append(local_len)
		foreign_arr.append(foreign_len)
		time.append(env.now)

env = simpy.Environment()
m = simpy.Resource(env, capacity=2)
n = simpy.Resource(env, capacity=2)
env.process(plane_arrival(env,plane_arrival_rate,m,n))

env.run(until = 1440)

plt.plot(time,local_arr,label = "locals")
plt.plot(time,foreign_arr,label = "foreigners")
plt.show()

W = 0
number = 100
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

