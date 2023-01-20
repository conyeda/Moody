"""Main file for the Moody app."""

import pathlib
import sys

PATH = str(pathlib.Path(__file__).parent.resolve())
sys.path.insert(1, '/'.join((PATH, 'ImageAnalyser')))
sys.path.insert(1, '/'.join((PATH, 'ModelLibrary')))

from UI.MoodyApp import MoodyApp

if __name__ == "__main__":
    MoodyApp().run()