:: Virtual environment
pip install virtualenv
python -m venv environment
call environment/Scripts/activate

:: Install dependencies
pip install "kivy[full]"
pip install Pillow
pip install numpy
pip install tensorflow
pip install librosa
pip install matplotlib