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
OUT_SIZE = (400, 400)

audio = scipy.io.loadmat("song1.mat")['x']
mf = audiovisualizer.movingfft.moving_fft(audio, SAMPLE_TIME, OUT_FPS, SAMPLE_RATE)
print(mf.shape)
mf = audiovisualizer.movingfft.isolate_freq_range(mf, DISPLAY_FREQ, SAMPLE_RATE, SAMPLE_TIME)
print(mf.shape)

drum1 = audiovisualizer.movingfft.extract_freq(mf, DISPLAY_FREQ, (320,335), SAMPLE_RATE, SAMPLE_TIME)

visualizers = [
        audiovisualizer.widgets.DrumCircle(drum1, (100, 100), 50, 100, (50, 230, 30))
        ]

background = PIL.Image.new("RGBA", OUT_SIZE)
PIL.ImageDraw.Draw(background).rectangle([(0,0), OUT_SIZE], fill=(0,0,0,255))
frame = 0
for sindex in range(0, mf.shape[0]):
    image = PIL.Image.new("RGBA", OUT_SIZE)
    imgdr = PIL.ImageDraw.Draw(image)
    imgdr.rectangle([(0,0), (100,100)], fill=(100, 0, 0, 255))
    for vis in visualizers:
        vis.display(sindex, imgdr)
    PIL.Image.alpha_composite(background, image).save(open("frame_"+str(frame).zfill(4)+".png", "wb"), "PNG")
    frame += 1
