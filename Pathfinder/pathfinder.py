import random
from datetime import datetime
from enum import Enum
from math import floor

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout


class TileStates(Enum):
    UNTOUCHED = (0.1, 0.1, 0.1, 1)
    SOURCE = (0, 1, 0, 1)
    DESTINATION = (0, 0, 1, 1)
    CANDIDATE = (1, 1, 1, 1)
    FINALIZED = (1, 1, 1, 1)
    OBSTACLE = (0, 0, 0, 1)


class Algorithms(Enum):
    DIJKSTRA = 'Dijkstra\'s'
    A_STAR = 'A*'
    BREADTH_FIRST = 'Breadth First'
    BELLMAN_FORD = 'Bellman-Ford'
    THORUP = 'Thorup'

    @staticmethod
    def get_corresponding(name: str):
        """
        Function to match a string with this corresponding enum entry

        Args:
            name (str): A string that SHOULD be one of the ones defined enum values

        Returns: An Algorithm enum entry

        """
        if name in Algorithms.get_algorithms():
            return Algorithms(name)

    @staticmethod
    def get_algorithms():
        """

        Returns: A List(str) representing the string values of the enum

        """
        return [i.value for i in Algorithms]


class ClickMode(Enum):
    DRAW = 1
    ERASE = 2
    SOURCE = 3
    DESTINATION = 4


class Tile(Button):
    def __init__(self, tile_map, length: int, x: int, y: int):
        """
        Constructor that gives us the spacial coordinates of the tile
        along with how big it should be
        Args:
            length: The length of a given edge of the tile
            x: The x coordinate within the grid
            y: The y coordinate within the grid
            **kwargs: Arguments needed by the parent constructor
        """
        # Call parent constructor
        super().__init__()
        # Initialize members
        self.tile_map = tile_map
        self.tile_map.add_widget(self)
        self.size = (length, length)
        self.x = x
        self.y = y
        self.bind(on_press=self.on_mouse_click)
        self.tile_state = TileStates.UNTOUCHED

    def on_mouse_click(self, instance):
        click_mode: ClickMode = self.tile_map.control_panel.click_mode
        if click_mode.name is ClickMode.SOURCE.name:
            self.background_color = TileStates.SOURCE.value
        elif click_mode.name is ClickMode.DESTINATION.name:
            self.background_color = TileStates.DESTINATION.value
        elif click_mode.name is ClickMode.ERASE.name:
            self.background_color = TileStates.UNTOUCHED.value
        elif click_mode.name is ClickMode.DRAW.name:
            self.background_color = TileStates.OBSTACLE.value

    def make_obstacle(self):
        self.background_color = TileStates.OBSTACLE.value
        self.tile_state = TileStates.OBSTACLE


class TileMap(GridLayout):
    def __init__(self, control_panel, width: int, height: int, length: int, **kwargs):
        """
        Constructor for the map, which allows us to calculate the number
        of rows and columns and subsequently place tiles accordingly
        Args:
            width: The width of the window
            height: The height of the window
            length: The length of a given square
            **kwargs: Arguments needed by parent constructor
        """
        # Call the parent constructor
        super().__init__(**kwargs)
        # Initialize the members
        self.control_panel = control_panel
        self.size_hint = (0.75, 1)
        self.rows = floor(height / length)
        self.cols = floor(width / length)
        self.tiles = [[Tile(self, length, x, y) for x in range(self.cols)] for y in range(self.rows)]

    def randomize_obstacles(self, seed=datetime.time()):
        number_of_obstacles = random.randint(0, self.cols * self.rows)
        while number_of_obstacles > 0:
            target: Tile = self.tiles[random.randint(0, self.rows)][random.randint(0, self.cols)]
            if target.tile_state is not TileStates.OBSTACLE:
                target.make_obstacle()
                number_of_obstacles -= 1


class ControlPanel(StackLayout):
    def __init__(self, **kwargs):
        """
        Constructor for the control panel, which accepts a reference to a TileMap
        in addition to any kwarg arguments required by the super class's constructor

        Args:
            tile_map: Reference to the grid of tiles
            **kwargs: Arguments required by the parent constructor
        """
        # Call the parent constructor with kwargs
        super().__init__(**kwargs)
        self.algo: Algorithms = Algorithms.DIJKSTRA
        self.click_mode: ClickMode = ClickMode.SOURCE

    def on_checkbox_active(self, state: bool, mode: ClickMode):
        """
        Method that runs when a radio button is pressed
        Args:
            state: Whether or not the button is active. We shouldn't be doing
                   anything if the button is inactive
            mode: The enum value representing the click mode the user is setting to
        """
        if state:
            self.click_mode = mode

    def change_algorithm(self, new_algo_name: str):
        """
        Changes the algorithm that we are going to run by matching a string with its
            corresponding Algorithm enum value
        Args:
            new_algo_name: The string we are going to match
        """
        self.algo = Algorithms.get_corresponding(new_algo_name)

    def run_search(self):
        pass

    def randomize_maze(self):
        pass


class PathfinderApp(App):
    def build(self):
        """
        Overridden method from the Kivy library that defines the root widget

        Returns: A widget, in this case a BoxLayout that defines spacing
        """
        parent = BoxLayout(orientation='horizontal', spacing=5, padding=5)
        l_control_panel = ControlPanel(size_hint=(0.25, 1))
        l_tile_map = TileMap(l_control_panel, parent.width, parent.height, 5, size_hint=(0.75, 1))
        parent.add_widget(l_control_panel)
        parent.add_widget(l_tile_map)
        return parent


if __name__ == '__main__':
    PathfinderApp().run()
