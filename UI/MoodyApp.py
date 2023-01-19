from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from UI.Screens.ImageAnalysisScreen.ImageAnalysisScreen import ImageAnalysisScreen
from UI.Screens.SongAnalysisScreen.SongAnalysisScreen import SongAnalysisScreen
from UI.Screens.RecommenderScreen.RecommenderScreen import RecommenderScreen

from ModelLibrary.classify import Classifier

Window.clearcolor = (1, 1, 1, 1)


class MainScreen(Screen):
    """ call to the analyse funtion at the end and realizes an analyse of the songs.
    """    
    def analyse_songs(self):
        """this method use the classifier to analyse the songs
        """
        classifier = Classifier("trained_MER.h5")
        classifier.classify()


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("UI/Screens/MainScreen/main_screen.kv")
    """loads the main screen
    """


class MoodyApp(App):
    """Class that represents all the aplication
    """    
    def build(self):
        """this method returns the principal screen

        Returns:
            Screen: main screen.
        """        
        return kv
