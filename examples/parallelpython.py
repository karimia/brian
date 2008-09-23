'''
Example of using Parallel Python 'pp' module for running multiple jobs

See (limited) documentation for PP at their website:

    http://www.parallelpython.com/

Each job server must have an up to date copy of Brian installed on it, and
must run the pp jobserver script as follows:

    ppserver.py -a -s "He's not the Messiah, he's a very naughty boy"
    
This ppserver.py script is installed in the Scripts/ folder of your
Python installation when you install pp. The -a option sets it to
auto-discovery mode, so that nodes on your cluster running the ppserver
can be automatically found by a process submitting jobs to it. The -s
option is a shared secret, basically a password to prevent external
access.
'''

from brian import *
import pp

# We create a pp job server in one of the following ways (see pp documentation for more info):

#js = pp.Server(ppservers=('computer1.complete.domain.name','computer2.complete.domain.name')) # For running over the internet
#js = pp.Server(ppservers=('computer1','computer2')) # For running over the local network
#js = pp.Server(ppservers=('*',)) # For running with autodiscovery mode over the local network
js = pp.Server(ppservers=()) # For running only on your own computer (but using multiple CPU cores)

# Now we write a function which defines the job to be executed. Note that
# there are some annoying features of pp: functions cannot use any global
# variables, so we have to import all the Brian functions etc. inside the
# function. However, we have a function decorator @ppfunction which does
# the work for you. Unfortunately, it needs to create an external file
# which will be named modulename_functionname_parallelpythonised.py, so
# in this example it will be called:
#   parallelpython_howmanyspikes_parallelpythonised.py
# This file contains the transformed code to make it work smoothly with
# parallelpython.

@ppfunction
def howmanyspikes(excitatory_weight):
    eqs='''
    dv/dt = (ge+gi-(v+49*mV))/(20*ms) : volt
    dge/dt = -ge/(5*ms) : volt
    dgi/dt = -gi/(10*ms) : volt
    '''
    P=NeuronGroup(4000,model=eqs,threshold=-50*mV,reset=-60*mV)
    P.v=-60*mV+10*mV*rand(len(P))
    Pe=P.subgroup(3200)
    Pi=P.subgroup(800)
    Ce=Connection(Pe,P,'ge')
    Ci=Connection(Pi,P,'gi')
    Ce.connect_random(Pe, P, 0.02,weight=excitatory_weight)
    Ci.connect_random(Pi, P, 0.02,weight=-9*mV)
    M=SpikeMonitor(P)
    run(100*ms)
    return M.nspikes

# Now we submit jobs. See the pp documentation details of what is going on here.
# In short write j = js.submit(func, args, depfuncs, modules) to submit function
# func with arguments args (which should be a tuple of values), depending on
# functions depfuncs (a tuple of functions), relying on modules (another tuple
# of strings). The job is submitted. To get the result of a job, you write
# val = j(), but executing this line will wait until the job is complete.

# Single job

#f = js.submit(howmanyspikes, (1.62*mV,), (), ('brian','numpy'))
#print f()

# Multiple jobs, and results plotted

excitatory_weight_range = linspace(0,4,20)
jobs = [ js.submit(howmanyspikes, (ew*mV,), (), ('brian','numpy')) for ew in excitatory_weight_range ]
numspikes = [ j() for j in jobs ]

js.print_stats()

plot(excitatory_weight_range, numspikes)
show()