import pathlib
from ImageMood import ImageMood
from os import listdir
from math import sqrt, pow
import random

PATH = str(pathlib.Path(__file__).parent.resolve())

class Recommender:
    """class with the recommender of the song based on an image
    """
    def __init__(self, image_path) -> None:
        """constructor of the class

        Args:
            image_path (PathLike): path with the image path
        """
        self._image_path = image_path
        self._image_mood = ImageMood(image_path)
        self._song = None
        self._valence = 0.0
        self._energy = 0.0
    
    def analyze(self):
        """analyze the image and return its valence and energy

        Returns:
            FloatTuple: set of two values (valence and energy)
        """
        self._image_mood.analyse()
        return ((self._image_mood.valence-1)/4, (self._image_mood.energy-1)/4)

    def search(self):
        """search the audio whose values are the nearest one to the selected image
        """    
        m_valence = self._valence
        m_energy = self._energy
        
        songs_path = '/'.join((PATH, 'ModelLibrary', 'xy_instances'))

        files = listdir(songs_path)

        selected_songs = [{'song':'','distance':1000}]

        for song in files:
            count, valence, energy, name = song.split('_',3)
            distance = sqrt(pow(m_energy - float(energy),2)+pow(m_valence - float(valence),2))

            if distance < selected_songs[0]['distance']:
                selected_songs = [{'song':song,'distance':distance}]

            elif distance == selected_songs[0]['distance']:
                selected_songs.append({'song':song,'distance':distance})
        
        selector = random.randint(0,len(selected_songs)-1)
        
        self._song = selected_songs[selector]['song']


    def recommend(self):
        """analyze the image and return the appropiate song

        Returns:
            PathLike: path of the selected and final song
        """
        if not self._image_mood.valence:
            self._valence, self._energy = self.analyze()
        self.search()
        
        return self._song