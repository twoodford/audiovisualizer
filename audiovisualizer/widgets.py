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

class DrumCircle:
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
                fill=self._ampl_color(currampl))
        # Draw concentric circles from previous frames
        for nframes in range(0, self._outer_rad - self._inner_rad):
            ampl = self._amplitude[framenum - nframes]
            _draw_circle(target, self._centerpt, self._inner_rad + nframes, 
                    outline=self._ampl_color(ampl))

    def _ampl_color(self, amplitude):
        """
        Get the appropriate color with alpha for the given amplitude

        Args:
            amplitude: The amplitude at the time
        """
        return self._color + (int(self._amplfactor * amplitude),)


def _draw_circle(target, center, radius, fill=None, outline=None):
    left = (center[0] - radius, center[1] - radius)
    right = (center[0] + radius, center[1] + radius)
    target.ellipse([left, right], fill, outline)
