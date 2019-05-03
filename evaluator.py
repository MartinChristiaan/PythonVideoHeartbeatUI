
import numpy as np

import scipy.stats as st
from numpy.linalg import norm

def dbv(x):
    return 20*np.log10(np.abs(x))

def calculateSNR(hwfft, f, nsig=1):
    hwfft = hwfft.squeeze()
    signalBins = np.arange(f - nsig + 1, f + nsig + 2, dtype='int64')
    signalBins = signalBins[signalBins > 0]
    signalBins = signalBins[signalBins <= max(hwfft.shape)]
    s = norm(hwfft[signalBins - 1]) # *4/(N*sqrt(3)) for true rms value;
    noiseBins = np.arange(1, max(hwfft.shape) + 1, dtype='int64')
    noiseBins = np.delete(noiseBins, noiseBins[signalBins - 1] - 1)
    n = norm(hwfft[noiseBins - 1])
    if n == 0:
        snr = np.Inf
    else:
        snr = dbv(s/n)
    return snr

class Evaluator():
    def __init__(self,fs,fftlength=300):
        self.curbpm = 0
        self.cursnr = 0
        self.f = np.linspace(0,fs/2,fftlength/2 + 1) * 60
        self.normalized_amplitude = np.zeros_like(self.f)
        
    def evaluate(self,fs,normalized_amplitude,fftlength = 300):
        self.f = np.linspace(0,fs/2,fftlength/2 + 1) * 60
        if len(normalized_amplitude) > 0:
            self.normalized_amplitude = normalized_amplitude
            bpm_id = np.argmax(normalized_amplitude)
            self.curbpm = self.f[bpm_id]
            self.cursnr = calculateSNR(normalized_amplitude,bpm_id)
            

