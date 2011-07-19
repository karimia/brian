"""
Offline compensation example
Input current: 1 second of filtered noise
Raw trace: Rothman Mannis model of the cochlear nucleus
"""
from brian import *
from brian.experimental.modelfitting import *
import numpy

if __name__ == '__main__':

    # load input current
    input = numpy.load("compensation_I.npy")
    
    # load neuron trace
    neurontrace = numpy.load("compensation_Vm.npy")
    
    # raw trace: add electrode resistance to neuron trace
    rawtrace = neurontrace + 500 * Mohm * input
    
    # time
    t = linspace(0.0, 1.0, 10000)
    
    # compensate the raw trace using 100 particles and 20 iterations
    comp, full, electrode, results = compensate(input,
                                                rawtrace,
                                                gpu=1,
                                                popsize=100,
                                                maxiter=20)
    
    print "The procedure found an electrode resistance Re=%.1f MOhm" \
        % (results["Re"]/Mohm)
    
    # plot the input current
    subplot(211)
    plot(t, input, 'k')
    xlabel("Time (s)")
    ylabel("Input current (A)")
    
    # plot the neuron trace, the raw trace, and the compensated trace
    subplot(212)
    plot(t, rawtrace, 'k', label="raw")
    plot(t, neurontrace, 'g', label="neuron")
    plot(t, comp, 'r', label="compensated")
    xlabel("Time (s)")
    ylabel("Membrane potential (V)")
    legend()
    
    show()

    