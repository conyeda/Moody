from threading import current_thread
import ColorMood

from PIL import Image
import numpy

class ImageMood:

    def __init__(self, image_path):
        self._image_path = image_path
        self._image = None
        self._image_data = None
        self._frequencies_array = None
        self._mood = None
    
    def get_mood(self):
        return self._mood

    def analyse(self):
        if not self._mood:
            self._image = Image.open(self._image_path)
            self._image_data = numpy.asarray(self._image)
            self._frequencies_array = numpy.zeros(24)
            width  = self._image_data.shape[1]
            height = self._image_data.shape[0]
            closer_color = 0
            closer_distance = 0
            current_distance = 0
            for i in range(0, height):
                for j in range(0, width):
                    closer_color = 0
                    closer_distance = numpy.sum(numpy.power(ColorMood.COLORS[0]["color"] - self._image_data[i][j], [2, 2, 2]))
                    for c in range(1, len(ColorMood.COLORS)):
                        current_distance = numpy.sum(numpy.power(ColorMood.COLORS[c]["color"] - self._image_data[i][j], [2, 2, 2]))
                        if current_distance < closer_distance:
                            closer_distance = current_distance
                            closer_color = c
                    self._frequencies_array[closer_color] += 1
            self._mood = ColorMood.COLORS[numpy.argmax(self._frequencies_array)]["mood"]