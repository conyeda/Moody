#!/bin/bash

# Virtual environment
pip install virtualenv
python -m venv environment
source environment/bin/activate

# Install dependencies
pip install "kivy[full]"
pip install Pillow
pip install numpy
pip install tensorflow-macos
pip install librosa
pip install matplotlib