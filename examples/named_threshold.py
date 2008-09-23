'''
Example with named threshold and reset variables
'''
from brian import *
eqs='''
dge/dt = -ge/(5*ms) : volt
dgi/dt = -gi/(10*ms) : volt
dx/dt = (ge+gi-(x+49*mV))/(20*ms) : volt
'''
P=NeuronGroup(4000,model=eqs,threshold=Threshold(-50*mV,state='x'),\
              reset=Refractoriness(-60*mV,5*ms,state='x'))
#P=NeuronGroup(4000,model=eqs,threshold=Threshold(-50*mV,state='x'),\
#              reset=Reset(-60*mV,state='x')) # without refractoriness
P.x=-60*mV
Pe=P.subgroup(3200)
Pi=P.subgroup(800)
Ce=Connection(Pe,P,'ge')
Ci=Connection(Pi,P,'gi')
Ce.connect_random(Pe, P, 0.02,weight=1.62*mV)
Ci.connect_random(Pi, P, 0.02,weight=-9*mV)
M=SpikeMonitor(P)
run(1*second)
raster_plot(M)
show()
