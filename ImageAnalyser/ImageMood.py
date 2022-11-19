from threading import Thread
from threading import Lock
from ImageAnalyser import ColorMood

from PIL import Image
import numpy

class ImageMood:

    def __init__(self, image_path):
        self._frequencies_array = None
        self._image_path = image_path
        self._image = None
        self._image_data = None
        self._mood = None
        self._lock = Lock()
    
    @property
    def mood(self):
        return self._mood

    def analyse_row(self, row):
        width  = self._image_data.shape[1]
        closer_color = 0
        closer_distance = 0
        current_distance = 0
        for j in range(0, width):
            closer_color = 0
            closer_distance = numpy.sum(numpy.power(ColorMood.COLORS[0]["color"] - self._image_data[row][j], [2, 2, 2]))
            for c in range(1, len(ColorMood.COLORS)):
                current_distance = numpy.sum(numpy.power(ColorMood.COLORS[c]["color"] - self._image_data[row][j], [2, 2, 2]))
                if current_distance < closer_distance:
                    closer_distance = current_distance
                    closer_color = c
            # TODO: Race condition. Check if solved
            self._lock.acquire()
            self._frequencies_array[closer_color] += 1
            self._lock.release()

    def analyse(self):
        if not self._mood:
            self._image = Image.open(self._image_path)
            self._image_data = numpy.asarray(self._image)
            self._frequencies_array = numpy.zeros(len(ColorMood.COLORS))
            height = self._image_data.shape[0]
            for i in range(0, height):
                Thread(target=self.analyse_row, args=[i]).run()
                
            self._mood = ColorMood.COLORS[numpy.argmax(self._frequencies_array)]["mood"]