import numpy as np
import scipy.io as sio
from scipy import signal
from rppgsensor import PPGSensor
# Params
R = 0
G = 1
B = 2

# self.f = np.linspace(0,self.fs/2,self.fftlength/2 + 1) * 60


    
def extract_pulse_chrominance(fs,rPPG,fftlength = 300):
    
 
    if(rPPG.shape[1] <= fftlength):
        return []
    else:

        fft_roi = range(int(fftlength/2+1)) # We only care about this part of the fft because it is symmetric anyway
        bpf_div= 60 * fs / 2
        b_BPF40220,a_BPF40220 = signal.butter(10, ([40/bpf_div, 220/bpf_div]),  'bandpass') 
        
        col_c = np.zeros((3,fftlength))
        skin_vec = [1,0.66667,0.5]
        for col in [R,G,B]:
            col_stride = rPPG[col,-fftlength:]# select last samples
            y_ACDC = signal.detrend(col_stride/np.mean(col_stride))
            col_c[col] = y_ACDC * skin_vec[col]
        X_chrom = col_c[R]-col_c[G]
        Y_chrom = col_c[R] + col_c[G] - 2* col_c[B]
        Xf = signal.filtfilt(b_BPF40220,a_BPF40220,X_chrom) # Applies band pass filter
        Yf = signal.filtfilt(b_BPF40220,a_BPF40220,Y_chrom)
        Nx = np.std(Xf)
        Ny = np.std(Yf)
        alpha_CHROM = Nx/Ny
        x_stride_method = Xf- alpha_CHROM*Yf
        STFT = np.fft.fft(x_stride_method,fftlength)[fft_roi]
        return np.abs(STFT)/np.max(np.abs(STFT)) #  Normalized Amplitude

def extract_pulse_PBV(fs,rPPG,fftlength = 300):
        
        if(rPPG.shape[1] < fftlength):
            return []
        else:
            
            pbv = np.array([0.307737615161693,0.436069490554354,0.236745815212185])    
            fft_roi = range(int(fftlength/2+1)) # We only care about this part of the fft because it is symmetric anyway
            bpf_div= 60 * fs / 2
            b_BPF40220,a_BPF40220 = signal.butter(10, ([40/bpf_div, 220/bpf_div]),  'bandpass') 
            
            col_c = np.zeros((3,fftlength)) 
            for col in [R,G,B]:
                col_stride = rPPG[col,-fftlength:]# select last samples
                y_ACDC = signal.detrend(col_stride/np.mean(col_stride))
                col_c[col,:] = signal.filtfilt(b_BPF40220,a_BPF40220,y_ACDC)
            S = np.matmul(col_c ,np.transpose(col_c))
            W = np.linalg.solve(S,pbv)
            x_stride_method = np.matmul(col_c.T,W)/(np.matmul(pbv.T,W)) 
            STFT = np.fft.fft(x_stride_method,fftlength)[fft_roi]
            normalized_amplitude = np.abs(STFT)/np.max(np.abs(STFT))
            return normalized_amplitude
    
