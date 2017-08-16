from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QStackedWidget, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QMainWindow, QGridLayout)
from PyQt5.QtGui import QColor

import constants


class Magic(QStackedWidget):
    """
    Magic defines the main window and contains the widget stack. Any movement
    between widgets in the stack is defined here.
    """
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setWindowTitle("Tic-Tac-Toe")
        self.resize(350, 300)

        # Set window background color
        # self.setAutoFillBackground(True)
        # p = self.palette()
        # p.setColor(self.backgroundRole(), QColor(87, 82, 79))
        # self.setPalette(p)

        # Create the objects for each stack
        self.intro = Intro(self.parent)
        self.new_game_setup = NewGameSetup(self.parent)
        self.game = Game(self.parent)

        # Add the widgets to the stack
        self.addWidget(self.intro)
        self.addWidget(self.new_game_setup)
        self.addWidget(self.game)

        # Connect buttons to switch stacks
        self.intro.button.clicked.connect(lambda: self.setCurrentIndex(2))


class Intro(QWidget):
    """
    The 'Intro' page of the app. This should allow users to select options
    before they begin a new game.
    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.button = QPushButton("new game")
        layout = QVBoxLayout()

        layout.addWidget(self.button)
        self.setLayout(layout)


class NewGameSetup(QWidget):
    """
    NewGameSetup takes the user through any setup that is required before
    loading the game screen.
    """
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.label = QLabel("hello")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


class Game(QWidget):
    """
    Game contains the UI of the Tic-Tac-Toe game itself, excluding any landing
    screens, settings, or setup.
    """
    class QTilePushButton(QPushButton):
        """
        Extends the QPushButton object and defines new functionality to respond
        to user's clicking on a specific tile on the game board.
        """
        def __init__(self, parent, symbol_map):
            """
            :param parent: the parent object which is an instance of app
            :param symbol_map: a dict that maps players to their symbols
            """
            super().__init__()
            self.symbol_map = symbol_map
            self.parent = parent
            # self.setEnabled(False)  # start the game with tiles disabled

        def handleButton(self, tile):
            """
            This function is called whenever a tile is clicked and results in a
            round of the game being played.

            :param tile: an instance of the Tile class
            """
            self.parent.play_round(tile)

        def updateButton(self, tile):
            """
            If an associated tile object has been changed, than the
            QTilePushButton needs to be updated accordingly, which is done
            here.

            :param tile: an instance of the Tile class
            """
            self.setEnabled(tile.player is None)  # Disable used tiles
            self.setText(self.symbol_map[tile.player])
            self.update()

        def sizeHint(self):
            """Defines the size of the QTilePushButton object."""
            return QSize(80, 80)

    def __init__(self, parent):
        """
        Creates all of the QTilePushButton widgets linked to each Tile on the
        board and adds them to the layout. Also creates connections for each
        button and defines delegates.

        :param parent: the parent object which is an instance of app
        """
        super().__init__()

        self.parent = parent
        tic = self.parent.tictactoe

        layout = QGridLayout()
        self.setLayout(layout)

        symbol_map = {None: '',
                      tic.player1: constants.PLAYER_SYMBOLS[1],
                      tic.player2: constants.PLAYER_SYMBOLS[2]}

        # For each tile on the board, add a widget to the GridLayout
        for tile in tic:
            button = Game.QTilePushButton(parent, symbol_map)
            button.clicked.connect(lambda _, button=button,
                                   tile=tile: button.handleButton(tile))
            layout.addWidget(button, tile.row, tile.column)
            tile.delegate = button
