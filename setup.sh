#!/bin/bash

# Virtual environment
pip install virtualenv
python m- venv environment
source environment/bin/activate

# Install dependencies
pip install "kivy[full]"
pip install Pillow
pip install numpy
pip install tensorflow
pip install librosa
pip install matplotlib
pip install sphinx
pip install sphinx_rtd_theme