from threading import Thread
from threading import Lock
import ColorMood

from PIL import Image
import numpy


class ImageMood:

    def __init__(self, image_path):
        self._image_path = image_path
        self._image = None
        self._image_data = None
        self._valence = None
        self._energy = None
        self._lock = Lock()

    @property
    def valence(self):
        return self._valence

    @property
    def energy(self):
        return self._energy

    def analyse_row(self, row, width):
        closer_color = 0
        closer_distance = 0
        for j in range(0, width):
            closer_color = 0
            closer_distance = numpy.sum(numpy.power(
                ColorMood.COLORS[0]["color"] - self._image_data[row][j], [2, 2, 2]))
            for c in range(1, len(ColorMood.COLORS)):
                current_distance = numpy.sum(numpy.power(
                    ColorMood.COLORS[c]["color"] - self._image_data[row][j], [2, 2, 2]))
                if current_distance < closer_distance:
                    closer_distance = current_distance
                    closer_color = c
            # TODO: Race condition. Check if solved
            self._lock.acquire()
            self._valence += ColorMood.COLORS[closer_color]["valence"]
            self._energy += ColorMood.COLORS[closer_color]["energy"]
            self._lock.release()

    def analyse(self):
        if not self._valence:
            self._image = Image.open(self._image_path)
            self._image_data = numpy.asarray(self._image)
            height = self._image_data.shape[0]
            width = self._image_data.shape[1]
            self._valence = 0
            self._energy = 0
            for i in range(0, height):
                Thread(target=self.analyse_row, args=[i, width]).run()

            self._valence /= (height*width)
            self._energy /= (height*width)


if __name__ == "__main__":
    image_mood = ImageMood("../images/yellow.jpeg")
    image_mood.analyse()
    print(image_mood.valence)
    print(image_mood.energy)
