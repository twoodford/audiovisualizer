import audiovisualizer
import PIL.Image
import PIL.ImageDraw
import pylab
import scipy
import scipy.io
import scipy.signal

# The sample rate of the input matrix (Hz)
SAMPLE_RATE=44100
# Frequency range to display (audible is 16-16384Hz)
DISPLAY_FREQ=(16, 1000)
# FPS of output (Hz)
OUT_FPS = 30
# Size of the moving average (s)
SAMPLE_TIME=0.5
# Output image size
OUT_SIZE = (1920, 1080)

audio = scipy.io.loadmat("song1.mat")['x']
mf = audiovisualizer.movingfft.moving_fft(audio, SAMPLE_TIME, OUT_FPS, SAMPLE_RATE)
mf = audiovisualizer.movingfft.isolate_freq_range(mf, DISPLAY_FREQ, SAMPLE_RATE, SAMPLE_TIME)

drum1 = audiovisualizer.movingfft.extract_freq(mf, DISPLAY_FREQ, (320,335), SAMPLE_RATE, SAMPLE_TIME)

FC=10/(0.5*SAMPLE_RATE)
N=1001
a=1
b=scipy.signal.firwin(N, cutoff=FC, window='hamming')
#lowpassed = scipy.signal.lfilter(b, a, audio)
mf2 = audiovisualizer.movingfft.moving_fft(audio, 1.5, OUT_FPS, SAMPLE_RATE)
#mf2 = audiovisualizer.movingfft.normalize_freq(mf2)
print(mf2)
fvis = audiovisualizer.movingfft.isolate_freq_range(mf2, (500, 1500), SAMPLE_RATE, SAMPLE_TIME)



visualizers = [
        audiovisualizer.widgets.DrumCircle(drum1, (200, 250), 100, 200, ((0, (50, 230, 30)), (1455, (200, 0, 200)), (1770, (50, 230, 30)))),
        audiovisualizer.widgets.FrequencyPoints(fvis, [(500, 0), (3840, 2160)], (
            (0, (0, 0, 255)), (420,(2, 255, 141)), (1380, (2, 100, 255)), 
            (1800, (2, 255, 57)), (2760, (91, 255, 181)), (3600, (63, 5, 255)),
            (3690, (221, 22, 78))
            ), 60),
        audiovisualizer.widgets.MeterDisplay(fvis, 17, (200, 700), 160, (0,240,255))
        ]

for frame, image in enumerate(audiovisualizer.animator.make_frames(visualizers, mf.shape[0], OUT_SIZE)):
    image.save(open("frame_"+str(frame).zfill(4)+".png", "wb"), "PNG")
    frame += 1
