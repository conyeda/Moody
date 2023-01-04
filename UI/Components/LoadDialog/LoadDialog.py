from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = StringProperty(None)
