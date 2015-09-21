# Just a test
import numpy
import numpy.fft as nfft
import pylab
import scipy
import scipy.io as sio

# The sample rate of the input matrix (Hz)
SAMPLE_RATE=44100
# Frequency range to display (audible is 16-16384Hz)
DISPLAY_FREQ=(16, 2000)
# FPS of output (Hz)
OUT_FPS = 30
# Size of the moving average (s)
MV_AVG_SIZE=1

def bin_approx_search(lst, tg):
    """
    Find the index of the element in lst which is closest to the number tg
    """
    top = len(lst) - 1
    bottom = 0
    while top > bottom:
        curri = (top - bottom)//2 + bottom
        if lst[curri] < tg:
            bottom = curri
        else:
            top = curri
        if top - bottom == 1:
            if abs(lst[top] - tg) < abs(lst[bottom] - tg):
                return top
            else:
                return bottom
    return top

def plotSpectrum(y,samplerate):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)
    """
    n = len(y) # length of the signal
    k = scipy.arange(n)
    T = n/samplerate
    frq = k/T # two sides frequency range
    frq = frq[range(n//2)] # one side frequency range

    Y = nfft.fft(y)/n # fft computing and normalization
    Y = Y[range(n//2)]

    bottomindex = bin_approx_search(frq, DISPLAY_FREQ[0])
    topindex = bin_approx_search(frq, DISPLAY_FREQ[1])

    frq = frq[bottomindex:topindex]
    Y = Y[bottomindex:topindex]

    # We want to plot frequencies in the audible range
    
    pylab.plot(frq,abs(Y),'r') # plotting the spectrum
    pylab.xlabel('Freq (Hz)')
    pylab.ylabel('|Y(freq)|')
    pylab.ylim((0, 0.018))

x=[1,4,5,7,8]
print(bin_approx_search(x, 3))

audio = sio.loadmat("song1.mat")['x']

frame_increment = SAMPLE_RATE // OUT_FPS
avg_len = MV_AVG_SIZE * SAMPLE_RATE
frame = 0
for start in range(0, audio.shape[0] - avg_len, frame_increment):
    print(start, start+avg_len)
    plotSpectrum(audio[start:start + avg_len, 0], SAMPLE_RATE)
    pylab.savefig('frame_'+str(frame).zfill(4)+'.png', bbox_inches='tight')
    frame += 1
