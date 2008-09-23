# Test of amplifier module
from brian import *
from brian.library.amplifier import *
from brian.library.electrodes import *
from scipy import pi
from brian.library.AEC import *

model_clock=Clock(dt=.1*ms)
sampling_clock=Clock(dt=.1*ms)

Cm=200*pF
Re=50*Mohm
Ce=0.5*ms/Re
R=10*ms/Cm

freq=100*Hz
eqs=Equations('''
dv/dt=ie/Cm-v/(10*ms) : volt
I:amp
u=v
''')
eqs+=electrode([.6*Re,.4*Re],[Ce,Ce],'vr','v','ie','ic')
eqs+=current_clamp('vr','ic','v_bridge','I',bridge=0*ohm,capa_comp=.95*Ce)

neuron=NeuronGroup(1,model=eqs,clock=model_clock)
ampli=AcquisitionBoard(neuron,'v_bridge','I',sampling_clock)
mon=StateMonitor(neuron,'v',record=0,clock=sampling_clock)
mon_vr=StateMonitor(ampli,'V',record=0,clock=sampling_clock)
mon_I=StateMonitor(ampli,'I',record=0,clock=sampling_clock)

@network_operation(clock=sampling_clock,when='middle')
def command():
    #neuron.E=sin(sampling_clock.t*2*pi*freq)*10*mV
    ampli.command(rand()*1*nA-.5*nA)

run(1000*ms)
v=mon_vr[0]
i=mon_I[0]
K=raw_kernel(*correlations(v,i,200))
Ke,_=electrode_kernel(K,50,dt=0.1*ms,online=True)
#plot(Ke/Mohm)
print sum(Ke)
#plot(mon.times/ms,mon[0]/mV,'b')
#plot(mon.times/ms,mon_vr[0]/mV,'g')
#show()
