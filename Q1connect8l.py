from IzNetwork import IzNetwork
import numpy as np
import numpy.random as rn


def Connect8L(layers, p):
	"""
	I will construct 9 layers. 8*100 of excitatory neurons
	and 1 * 200 of inhibitory neurons. Each inhibitory neuron
	will be connected to by 4 excitatory neurons. And each inhibitory 
	neuron connected to every neuron in the network (diffuse). On set
	up there are 1000 one way connections from ex to ex neurons in each
	module.
	"""
	NO_EX_NUERONS_PER_MODULE = 100
	NO_INHIB_NUERONS = 200
	INHIB = 8
	Dmax = 20
	net = IzNetwork(layers, Dmax)
	rii = rn.rand()
	#inhibitory layer
	net.layer[INHIB].N = NO_INHIB_NUERONS
	net.layer[INHIB].a = (0.02 + 0.08*rii) * np.ones(NO_INHIB_NUERONS)
	net.layer[INHIB].b = (0.25 - 0.05*rii) * np.ones(NO_INHIB_NUERONS)
	net.layer[INHIB].c = -65 * np.ones(NO_INHIB_NUERONS) 
	net.layer[INHIB].d = 2 * np.ones(NO_INHIB_NUERONS)
	#set inhib neurons to each other
	net.layer[INHIB].S[INHIB] = -(rn.rand(NO_INHIB_NUERONS, NO_INHIB_NUERONS))
	for i in range(200):
		for j in range(200):
			if i == j:
				net.layer[INHIB].S[INHIB][i][j] = 0

	net.layer[INHIB].factor[INHIB] = 1
	net.layer[INHIB].delay[INHIB] = np.ones([NO_INHIB_NUERONS, NO_INHIB_NUERONS])
		
	no_layers = len(net.layer)
	#used to count connection from ex to inhib
	inhib_conn = 0
	#setting up the connection matrices before so i access them later
	for k in range(8):
		for m in range(8):
			net.layer[k].S[m] = np.zeros([NO_EX_NUERONS_PER_MODULE,
										 	  NO_EX_NUERONS_PER_MODULE])
			net.layer[k].delay[m] = rn.randint(1, 20, size=(NO_EX_NUERONS_PER_MODULE, 
													NO_EX_NUERONS_PER_MODULE))
			net.layer[k].factor[m] = 17 


	re = rn.rand()
	#first 8 layers will be excitatory modules
	for idx in range(no_layers-1):
	
		#DEALS WITH INHIB TO EX (THIS LAYER)
		net.layer[idx].S[INHIB] = -(rn.rand(NO_EX_NUERONS_PER_MODULE,
										NO_INHIB_NUERONS))
		net.layer[idx].factor[INHIB] = 2
		net.layer[idx].delay[INHIB] = np.ones([NO_EX_NUERONS_PER_MODULE,
												NO_INHIB_NUERONS])
		##############################################################################
		net.layer[idx].N = NO_EX_NUERONS_PER_MODULE
		# decay rate for ex modules
		net.layer[idx].a = 0.02 * np.ones(NO_EX_NUERONS_PER_MODULE)
		# sensitivity for ex modules
		net.layer[idx].b = 0.20 * np.ones(NO_EX_NUERONS_PER_MODULE)
		#resets for modules
		net.layer[idx].c = (-65 + 15 * re**2) * np.ones(NO_INHIB_NUERONS)
		net.layer[idx].d = (8 - 6*re**2) *  np.ones(NO_INHIB_NUERONS) 
		##############################################################################
		#Configure connection matrix to inhib. Connect to 25 inhib neurons.
		#deals with connections coming from this layer into the inhib layer
		net.layer[INHIB].S[idx] = np.zeros([NO_INHIB_NUERONS,
										  NO_EX_NUERONS_PER_MODULE])
		#weight is 1 to inhib neurons (4 ex to 1 inhib) with factor 50
		net.layer[INHIB].factor[idx] = 50
		net.layer[INHIB].delay[idx] = np.ones([NO_INHIB_NUERONS,
											    NO_EX_NUERONS_PER_MODULE])

		for i in range(0, NO_EX_NUERONS_PER_MODULE, 4):
			for n in range(4):
				r = rn.rand()
				net.layer[INHIB].S[idx][inhib_conn][i+n] = r

			inhib_conn = inhib_conn + 1
		#############################################################################
		#Make 1000 random connections within the module
		floatp = float(p)
		for conn in range(1000):
			#so we choose two random numbers
			#if that number is not 1 set it and it isn't connected to itself
			n1 = rn.randint(100)
			n2 = rn.randint(100)
			val = net.layer[idx].S[idx][n1][n2]
			#so if the value is already set or we try to connect to ourself
			#we will keep looking for an empty space
			if val == 1:
				while(net.layer[idx].S[idx][n1][n2] == 1  and n1 != n2):
					n1 = rn.randint(100)
					n2 = rn.randint(100)
					if net.layer[idx].S[idx][n1][n2] == 0:
						net.layer[idx].S[idx][n1][n2] = 1
						break
			else:
				net.layer[idx].S[idx][n1][n2] = 1
		
		for i in range(100):
			for j in range(100):
				if net.layer[idx].S[idx][i][j] == 1:
					rewire = rn.rand()
					if rewire < floatp:
						net.layer[idx].S[idx][i][j] = 0
						rm = rn.randint(8)
						rnint = rn.randint(100)
						net.layer[rm].S[idx][rnint][j] = 1
						
						
	return net


