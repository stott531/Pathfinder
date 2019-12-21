from enum import Enum
from math import floor

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget


class ControlPanel(StackLayout):
    pass


class Tile(Button):
    def __init__(self, length: int, x: int, y: int, **kwargs):
        super().__init__(**kwargs)
        self.size = (length, length)
        self.x = x
        self.y = y


class TileMap(GridLayout):
    def __init__(self, width: int, height: int, length: int, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.75, 1)
        self.rows = floor(height / length)
        self.cols = floor(width / length)
        for i in range(self.rows):
            for j in range(self.cols):
                self.add_widget(Tile(length, j, i))



class PathfinderApp(App):
    def build(self):
        parent = BoxLayout(orientation='horizontal', spacing=5, padding=5)
        parent.add_widget(ControlPanel(size_hint=(0.25, 1)))
        parent.add_widget(TileMap(parent.width, parent.height, 5, size_hint=(0.75, 1)))
        return parent


if __name__ == '__main__':
    PathfinderApp().run()
