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
import numpy.fft
import scipy

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
    outdat = (numpy.fft.fft(indat)[range(n//2)])/y

def get_x_axis(samplerate, samplelength):
    """
    Find the actual frequencies to include along the x axis

    The samplerate is the sample rate of the audio matrix in Hertz 
    and the samplelength is the number of samples fed to the FFT.

    Returns a matrix with the x axis numbers.
    """
    time = samplelength / samplerate # The sample time of a single fft
    return scipy.arange(samplelength // 2) / time
