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
OUT_SIZE = (500, 1000)

audio = scipy.io.loadmat("song1.mat")['x']
mf = audiovisualizer.movingfft.moving_fft(audio, SAMPLE_TIME, OUT_FPS, SAMPLE_RATE)
print(mf.shape)
mf = audiovisualizer.movingfft.isolate_freq_range(mf, DISPLAY_FREQ, SAMPLE_RATE, SAMPLE_TIME)
print(mf.shape)

# Downsample the DFT matrix
tfactor = int(mf.shape[0] / OUT_SIZE[1])
afactor = mf.shape[1] / OUT_SIZE[0]
print(tfactor, afactor)
mfd = scipy.signal.decimate(mf, tfactor, axis=0)
if afactor > 1:
    mfd = scipy.signal.decimate(mf, int(afactor), axis=1)
else:
    mfd = scipy.signal.resample(mf, 2,2)

image = PIL.Image.new("L", OUT_SIZE)
imgdr = PIL.ImageDraw.Draw(image)

for x in range(OUT_SIZE[0]):
    for y in range(OUT_SIZE[1]):
        imgdr.point((x,y), mfd[y,x]*256*10)

image.save(open("fun.png", "wb"), "PNG")
