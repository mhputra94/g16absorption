#!/usr/bin/env python
# coding: utf-8

# Import Python Module

import sys
import re
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scipy.fftpack import fft
from decimal import Decimal
from scipy import interpolate
from scipy.signal import find_peaks


# Read Excited State Result

ExcitedState = []
with open("struc.log","r") as file:
    for line in file:
        if re.search("Excited State", line):
           sys.stdout.write(line)
           ExcitedState.append(line)

ExcitedState = np.array(ExcitedState)
size=ExcitedState.shape


# Grab the Excitation Energy and Harmonic Oscillator

def convert(lst):
    return ([i for item in lst for i in item.split()])

energy = []
har_osc = []
for i in range(int(size[0])):
    result = re.sub('f=','',ExcitedState[i])
    lst =  [result]
    conv = convert(lst)
    ene = float(conv[4])
    har = float(conv[8])
#    result2 = re.sub('Excited State','',result)
#    result3 = re.sub(':','',result2)
#    result4 = np.char.split(result3)
    energy.append(ene)
    har_osc.append(har)

energy = np.array(energy)
har_osc = np.array(har_osc)


# Absorption Spectra Calculation

def convert(eV):
    lam = 1239.84193/eV
    return lam

sigieV  = 0.25 # Broadening Factor in eV
siginm  = convert(sigieV)
sigi = 1.0/siginm
peak = energy
osc  = har_osc


def abso(f, sig, lambd, lambdam):
    #cons = 1.3062974E8
    cons = 1.0
    isie = (lambd - lambdam)/sig
    expo = np.exp(-(isie**2.0))
    absr = ((cons*f)/sig)*expo
    return absr

freq = np.arange(0.001,10,0.001) # Variation lambda (nm)

UVVIS= []
for j in range(len(freq)):
    so = 0.0
    for i in range(len(peak)):
        asor = abso(osc[i],sigieV,freq[j],peak[i])
        so = so + asor 
    
    UVVIS.append(so)

UVVIS = np.array(UVVIS)
    

# Peak Absorption Spectra
    
UVVIS = np.array(UVVIS)
peaks, _ = find_peaks(UVVIS)
print("Peak of Absorptions are", 1239.84193/freq[peaks])
seeb = np.array(Spektrum)


Plot Spectra and Oscillator Harmonic

num_renorm = 3
plt.plot(1239.84193/freq,UVVIS/num_renorm,'b-', linewidth = 2.0)
 
for i in range(len(peak)):
    plt.vlines(1239.84193/peak[i],0,osc[i],colors='g')
    
plt.xlabel('$\lambda$ (nm)', size = 14)
plt.ylabel('Normalized Absorption', size = 14)
plt.xlim(300,900)
plt.ylim(0,1.0)

plt.show()
