from Q1connect8l import Connect8L
import multiprocessing as mp
from jpype import *
import numpy as np
import sys 
import matplotlib.pyplot as plt
import numpy.random as rn

jarlocation = "./infodynamics.jar"
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarlocation)

INHIB = 8 
def run20times():
	xs = []
	ys = []
	op = mp.Queue()
	ps = []
	for i in range(20):
		ps.append(mp.Process(target=runfor60))

	for p in ps:
		p.start()

	for p in ps:
		p.join()

	for i in range(0,20):
		res = op.get()
		ys.append(res[0])
		xs.append(res[1])
		
	plt.figure(1)
	plt.title("Random graph calc of MI")
	plt.scatter(xs, ys, marker='.')
	plt.xlabel("Random number")
	plt.ylabel("Mi calculation")
	plt.xlim(0, 1)
	plt.ylim(0, 7)
	plt.show()

def runfor60():
	T = 60000
	randy = rn.rand()
	net = Connect8L([100, 100, 100, 100, 100, 100, 100, 100, 200], randy)

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

	miCalcClass = JPackage('infodynamics.measures.continuous.kraskov').MultiInfoCalculatorKraskov2
	miCalc = miCalcClass()
	#8 lines
	miCalc.initialise(8)

	yss = np.zeros([2950, 8])
	offset = 50
	for i in range(no_layers - 1):
		ys = np.array([])
		for t in range(0, T, 20):
			count = 0
			if net.layer[i].firings.size != 0:
				nts = []
				nts.extend(net.layer[i].firings[:,0])
				for nt in nts: 
					if nt > t and nt < (t + 50):
						count = count + 1
				final = float(count) / 50
				if t >= 1000:
					yss[t/20 - offset][i] = final * 1.433

	miCalc.startAddObservations()
	miCalc.addObservations(yss)
	miCalc.finaliseAddObservations()
	res = miCalc.computeAverageLocalOfObservations()
	return [res, randy]


run20times()



