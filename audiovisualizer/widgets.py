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
from PIL import Image, ImageDraw

class Widget:
    def _ampl_color(self, amplitude, frame):
        """
        Get the appropriate color with alpha for the given amplitude

        Args:
            amplitude: The amplitude at the time
        """
        color=(0,0,0)
        for col in self._color:
            if frame >= col[0]:
                color = col[1]
        return color + (int(self._amplfactor * amplitude),)

class DrumCircle(Widget):
    """
    Visualizer for percussive sounds with a solid circle in 
    the middle and concentric rings for past data.

    Takes a preprocessed 1D array for input.  The extract_frequency() 
    method in the movingfft module may be useful for getting this type 
    of data.
    """

    def __init__(self, amplitude, centerpt, inner_rad, outer_rad, color):
        """
        Create a DrumCircle visualization widget

        Args:
            amplitude: 1D array of amplitude data to display
            centerpt: (x,y) tuple for the location of the circle's center
            inner_rad: The radius of the circle displaying the current amplitude
            out_rad: The number of additional circles displaying past amplitude
            color: The circle color in RGB
        """
        self._amplitude = amplitude
        self._centerpt = centerpt
        self._inner_rad = inner_rad
        self._outer_rad = outer_rad
        self._color = color
        # Find the amplitude -> alpha conversion factor
        maxampl = numpy.nanmax(amplitude)
        self._amplfactor = 256 / maxampl * 50

    def display(self, framenum, target):
        # Draw the center circle
        currampl = self._amplitude[framenum]
        _draw_circle(target, self._centerpt, self._inner_rad, 
                fill=self._ampl_color(currampl, framenum))
        # Draw concentric circles from previous frames
        for nframes in range(0, (self._outer_rad - self._inner_rad) // 2):
            ampl = self._amplitude[framenum - nframes]
            _draw_circle(target, self._centerpt, self._inner_rad + nframes*2, 
                    outline=self._ampl_color(ampl, framenum - nframes))
            _draw_circle(target, self._centerpt, self._inner_rad + nframes*2 + 1, 
                    outline=self._ampl_color(ampl, framenum - nframes))

class FrequencyPoints(Widget):
    """
    Shows the frequency data on the x axis and time on the y axis, with 
    the current time in the center.  Looks kind of like rain.
    """

    def __init__(self, fftmatrix, bounds, color, visframes=20):
        self._fftmatrix = fftmatrix
        self._bounds = bounds
        self._color = color
        self._visframes = visframes
        self._amplfactor = 256*5000

    def display(self, framenum, target):
        # Start with a size that matches what we'll draw
        isize = (self._fftmatrix.shape[1], self._visframes)
        iimg = Image.new("RGBA", isize)
        iimgdr = ImageDraw.Draw(iimg)
        for x in range(isize[0]):
            for y in range(isize[1]):
                color = self._ampl_color(
                        abs(self._fftmatrix[framenum - y, x]), framenum - y)
                iimgdr.point((x,y), color)
        rectimg = iimg.resize(self._rect_size(), resample=Image.BICUBIC)
        target.bitmap(self._bounds[0], rectimg, fill=self._ampl_color(1/5000, framenum))

    def _rect_size(self):
        """Returns the (width, height) of the draw rect"""
        bnd = self._bounds
        return (bnd[1][0] - bnd[0][0], bnd[1][1] - bnd[0][1])

class MeterDisplay:
    def __init__(self, fftmatrix, fpb, center, radius, color):
        """
        Create a new meter display
        Args:
            fftmatrix: The fft data
            fpb: Frames per beat
            center: Center of the circle
            radius: Radius of the circle
            color: Color data
        """
        self._fftmatrix = fftmatrix
        self._fpb = fpb
        self._center = center
        self._radius = radius
        self._color = color

    def display(self, framenum, target):
        left = (self._center[0] - self._radius, self._center[1] - self._radius)
        right = (self._center[0] + self._radius, self._center[1] + self._radius)
        beatnum = ((framenum - 11) // self._fpb) % 4 + 1
        target.pieslice([left, right], 0, beatnum * 90, fill=self._color)

def _draw_circle(target, center, radius, fill=None, outline=None):
    left = (center[0] - radius, center[1] - radius)
    right = (center[0] + radius, center[1] + radius)
    target.ellipse([left, right], fill, outline)
