from enum import Enum
from math import floor

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout


class TileStates(Enum):
    UNTOUCHED = 1
    SOURCE = 2
    DESTINATION = 3
    CANDIDATE = 4
    FINALIZED = 5


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
    def __init__(self, length: int, x: int, y: int, **kwargs):
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
        super().__init__(**kwargs)
        # Initialize members
        self.size = (length, length)
        self.x = x
        self.y = y


class TileMap(GridLayout):
    def __init__(self, width: int, height: int, length: int, **kwargs):
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
        self.size_hint = (0.75, 1)
        self.rows = floor(height / length)
        self.cols = floor(width / length)

        # Add the tiles to the map while setting their corresponding x-y coordinates
        for y in range(self.rows):
            for x in range(self.cols):
                self.add_widget(Tile(length, x, y))


class ControlPanel(StackLayout):
    def __init__(self, tile_map: TileMap, **kwargs):
        """
        Constructor for the control panel, which accepts a reference to a TileMap
        in addition to any kwarg arguments required by the super class's constructor

        Args:
            tile_map: Reference to the grid of tiles
            **kwargs: Arguments required by the parent constructor
        """
        # Call the parent constructor with kwargs
        super().__init__(**kwargs)
        self.tile_map = tile_map
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
        l_tile_map = TileMap(parent.width, parent.height, 5, size_hint=(0.75, 1))
        parent.add_widget(ControlPanel(l_tile_map, size_hint=(0.25, 1)))
        parent.add_widget(l_tile_map)
        return parent


if __name__ == '__main__':
    PathfinderApp().run()
