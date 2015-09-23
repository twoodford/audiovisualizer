# audiovisualizer
# Copyright (C) 2015 Timothy Woodford
# Licensed under the Apache License, version 2.0
# You can obtain a copy of the license at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import numpy
import numpy.fft
import scipy

def _bin_approx_search(lst, tg):
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

def fft_in_range(audiomatrix, startindex, endindex, channel):
    """
    Do an FFT in the specified range of indices

    The audiomatrix should have the first index as its time domain and 
    second index as the channel number.  The startindex and endinex 
    select the time range to use, and the channel parameter selects 
    which channel to do the FFT on.

    Returns a vector of data in the frequency domain
    """
    n = endindex - startindex
    indat = audiomatrix[startindex:endindex, channel]
    outdat = (numpy.fft.fft(indat)[range(n//2)])/n
    return outdat

def get_x_axis(samplerate, samplelength):
    """
    Find the actual frequencies to include along the x axis

    The samplerate is the sample rate of the audio matrix in Hertz 
    and the samplelength is the number of samples fed to the FFT.

    Returns a matrix with the x axis numbers.
    """
    time = samplelength / samplerate # The sample time of a single fft
    return scipy.arange(samplelength // 2) / time

def moving_fft(audiomatrix, sampletime, fps, samplerate, channel=0):
    """
    Get a number of FFT samples over the time of an audio sample

    This is basically like a moving average for DFTs

    Args:
        audiomatrix: A matrix of audio data with time for the first 
            dimension and channel for the second dimension
        sampletime: The length of a sample in seconds
        fps: The number of output samples per second
        samplerate: The sample frequency of the audio in hertz
        channel: The audio channel to use
    Returns:
        A matrix where the first dimension is the frame number 
        and the second dimension is the frequency
    """
    samplelength = int(sampletime * samplerate)
    frame_increment = samplerate // fps
    frame = 0
    frames = (audiomatrix.shape[0] - samplelength) // frame_increment
    #ret = numpy.zeros((frames, frame_increment//2), numpy.complex128)
    ret = []
    for startindex in range(0, audiomatrix.shape[0] - samplelength, frame_increment):
        x = fft_in_range(audiomatrix, startindex, startindex + frame_increment, channel)
        ret.append(x)
    return numpy.array(ret)

def freq_range_graph(fftmatrix, freqrange, samplerate, sampletime):
    """
    Create a row vector of the average amplitude of a frequency range over time

    Args:
        fftmatrix: The moving_fft() output
        freqrange: A tuple of form (minimum frequency, maximum frequency)
        samplerate: The sample frequency of the audio in hertz
        sampletime: The length of a sample in seconds
    """
    frq = get_x_axis(samplerate, sampletime * samplerate)
    bottomindex = _bin_approx_search(frq, freqrange[0])
    topindex = _bin_approx_search(frq, freqrange[1])
    sliced = fftmatrix[:,bottomindex:topindex]
    return numpy.average(sliced, 1)

def isolate_freq_range(fftmatrix, freqrange, samplerate, sampletime):
    """
    Create a moving DFT matrix with only the given frequency range

    Args:
        fftmatrix: The moving_fft() output
        freqrange: A tuple of form (minimum frequency, maximum frequency)
        samplerate: The sample frequency of the audio in hertz
        sampletime: The length of a sample in seconds
    """
    frq = get_x_axis(samplerate, sampletime * samplerate)
    bottomindex = _bin_approx_search(frq, freqrange[0])
    topindex = _bin_approx_search(frq, freqrange[1])
    return fftmatrix[:,bottomindex:topindex]

def extract_freq(fftmatrix, backgroundfreq, targetfreq, samplerate, sampletime):
    """
    Extract occurrences of a specific note of drum by comparing its frequencies 
    to background frequencies

    Args:
        fftmatrix: The moving_fft() output
        backgroundfreq: Frequencies to look for background noise
        targetfreq: Frequency range of the instrument
        samplerate: The sample frequency of the audio in hertz
        sampletime: The length of a sample in seconds
    """
    target = freq_range_graph(fftmatrix, targetfreq, samplerate, sampletime)
    background = freq_range_graph(fftmatrix, backgroundfreq, samplerate, sampletime)
    return abs(target)/(abs(background) + 1E-20)

