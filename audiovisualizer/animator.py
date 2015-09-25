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

import PIL.Image
import PIL.ImageDraw

def make_frames(visualizers, numframes, outdimen, background=None):
    """
    Returns an iterator over antialiased output images

    Args:
        visualizers: An iterable of visualizer widgets
        numframes: The number of output frames to generate
        outdimen: (width, height) tuple of the output image size
        background: An optional background image
    """
    # The initial size of the image before it is resampled for antialiasing
    gensize = (outdimen[0] * 2, outdimen[1] * 2)

    # Default background is solid black
    if background is None:
        background = PIL.Image.new("RGBA", gensize)
        PIL.ImageDraw.Draw(background).rectangle([(0,0), gensize], fill=(0,0,0,255))

    # Generate frames
    for frame in range(numframes):
        image = PIL.Image.new("RGBA", gensize)
        imgdr = PIL.ImageDraw.Draw(image)
        for vis in visualizers:
            vis.display(frame, imgdr)
        composite = PIL.Image.alpha_composite(background, image)
        # Resample for nice antialiasing
        yield composite.resize(outdimen, resample=PIL.Image.ANTIALIAS)
