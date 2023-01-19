from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout


class LoadDialog(FloatLayout):
    """class which represent the screen use to select the image
    """    
  
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = StringProperty(None)
