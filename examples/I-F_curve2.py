'''
Input-Frequency curve of a IF model
Network: 1000 unconnected integrate-and-fire neurons (Brette-Gerstner)
with an input parameter I.
The input is set differently for each neuron.
Spikes are sent to a 'neuron' group with the same size and variable n,
which has the role of a spike counter.
'''
from brian import *

N=1000
tau=10*ms
eqs='''
dv/dt=(v0-v)/tau : volt
v0 : volt
'''
group=NeuronGroup(N,model=eqs,threshold=10*mV,reset=0*mV,refractory=5*ms)
group.v=0*mV
group.v0=linspace(0*mV,20*mV,N)

counter=SpikeCounter(group)

duration=5*second
run(duration)
plot(group.v0/mV,counter.count/duration)
show()