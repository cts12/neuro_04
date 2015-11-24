from Q1connect8l import Connect8L
import numpy as np
import sys 
import matplotlib.pyplot as plt
import numpy.random as rn

#instantiate net with 7 modules of 100 excitatory neurons and 1 inhibitory
#containing 200 
net = Connect8L([100,100,100,100,100,100,100,100, 200], sys.argv[1])
INHIB = 8 # index of inhibitory neurons
# connectionGraph ##########################################
xs = []
ys = []
for i in range(len(net.layer) - 1):
	l = net.layer[i]
	S2 = net.layer[i].S[INHIB]
	S3 = net.layer[INHIB].S[i]
	stackn = i * 100

	for j in range(len(net.layer) - 1):
		S = l.S[j]
		st = j * 100
		for d in range(100):
			for a in range(100):
				if S[d][a] != 0 :
					xs.append(stackn + d)
					ys.append(st + a)

	for d in range(100):
		for a in range(200):
			if S2[d][a] != 0:
				xs.append(800 + a)
				ys.append(stackn + d)
	
	#We know that the inhib module is connected to everything
	for d in range(200):
		for a in range(100):
			if S3[d][a] != 0:
				xs.append(stackn + a)
				ys.append(800 + d)


S = net.layer[INHIB].S[INHIB]

for d in range(200):
	for a in range(200):
		if S[d][a] != float(0):
			xs.append(800 + d)
			ys.append(800 + a)

plt.figure(1)
plt.title('Connection Matrix')
plt.scatter(xs, ys, marker='.')
plt.ylabel('Neuron Index')
plt.xlabel('Neuron Index')
plt.ylim([1000, 0])
plt.xlim([0, 1000])
######################################################################

T = 1000 # simulation time

for lr in xrange(len(net.layer)):
	net.layer[lr].v = -65 * np.ones(net.layer[lr].N)	
	net.layer[lr].u = net.layer[lr].b * net.layer[lr].v
	net.layer[lr].firings = np.array([])
vs = {}
us = {}
for i in range(len(net.layer) - 1):
	vs[i] = np.zeros([T, 100])
	us[i] = np.zeros([T, 100])

vs[INHIB] = np.zeros([T, 200])
us[INHIB] = np.zeros([T, 200])

#LETS SIMULATE
no_layers = 9
for t in xrange(T):

	#Go through each of hte layers and apply some background firing.
	for i in range(no_layers):
		if i < 8 :
			net.layer[i].I =  np.zeros(100)
			for n in range(100):
				inject = rn.poisson(0.01)
				if inject > 0 :
					net.layer[i].I[n] = 15

		else : 
			net.layer[i].I = np.zeros(200)
			for n in range(200):
				inject = rn.poisson(0.01)
				if inject > 0:
					net.layer[i].I[n] = 0
				

	net.Update(t)
	
xs = []
ys = []
plt.figure(2)
plt.title('Raster Plot') 
plt.ylabel('Neuron Index')
plt.xlabel('Time')
plt.ylim(1000,0)
plt.xlim(0, T)
xs = []
ys = []
for i in range(no_layers):
	stackn = i * 100
	if net.layer[i].firings.size != 0:
		xs.extend(net.layer[i].firings[:,0])
		ys.extend(stackn + net.layer[i].firings[:, 1])

plt.scatter(xs, ys, marker='.')

################################################################
# mean firing graph 
xss = []
yss = []

for i in range(no_layers - 1):
	xs = []
	ys = []
	for t in range(0, T, 20):
		count = 0
		if net.layer[i].firings.size != 0:
			nts = []
			nts.extend(net.layer[i].firings[:,0])
			for nt in nts: 
				if nt > t and nt < (t + 50):
					count = count + 1
					#print count
			final = float(count) / 50
			# print [t, final]
			xs.append(t)
			ys.append(final)

	xss.append(xs)
	yss.append(ys)


plt.figure(3)
plt.title('Mean firing plot2')
plt.ylabel('Mean count')
plt.xlabel('Time')
plt.ylim(0, 6)
plt.xlim(0,T)
for i in range(8):
	plt.plot(xss[i],yss[i])

plt.show()
