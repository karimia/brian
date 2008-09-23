'''
Example with Tsodyks STP model
Neurons with regular inputs and depressing synapses
'''
from brian import *

U_SE=.67
tau_e=3*ms
taum=50*ms
tau_rec=800*ms
A_SE=250*pA
Rm=100*Mohm
N=10

eqs='''
dx/dt=rate : 1
dR/dt=(1-R)/tau_rec : 1
rate : Hz
'''

def reset_STP(P,spikes):
    P.R_[spikes]-=U_SE*P.R_[spikes]
    P.x[spikes]=0
    
input=NeuronGroup(N,model=eqs,threshold=1.,reset=reset_STP)
MR=StateMonitor(input,'R',record=[0,N-1])
input.R=1
input.rate=linspace(5*Hz,30*Hz,N)

eqs_neuron='''
dv/dt=(Rm*i-v)/taum:volt
di/dt=-i/tau_e:amp
'''
neuron=NeuronGroup(N,model=eqs_neuron)

C=Connection(input,neuron,'i',modulation='R')
C.connect_one_to_one(input,neuron,A_SE*U_SE)
trace=StateMonitor(neuron,'v',record=[0,N-1])

run(1000*ms)
subplot(221)
plot(MR.times/ms,MR[0])
title('R')
subplot(223)
plot(trace.times/ms,trace[0]/mV)
title('Vm')
subplot(222)
plot(MR.times/ms,MR[N-1])
title('R')
subplot(224)
plot(trace.times/ms,trace[N-1]/mV)
title('Vm')
show()
