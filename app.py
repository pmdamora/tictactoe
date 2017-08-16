from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication,
                             QMessageBox, QStackedWidget, QVBoxLayout, QLabel)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor

from game import TicTacToe
import constants
import view


class App(QWidget):
    """
    This class is intended to contain other classes and functions that are
    relevant to running the application on a high level. Primarily, it
    initializes the game, and contains that functions that respond to user
    interaction with the UI during gameplay, without actually altering the UI.
    """
    def __init__(self):
        """Creates the game object as well as the UI, and displays it."""
        super().__init__()

        # Create the game model object
        self.tictactoe = TicTacToe()
        self.turn = self.tictactoe.player1  # player1 goes first

        # Load the UI
        self.win = view.Magic(self)
        self.win.show()

    def switch_turns(self):
        """Switches the active player."""
        # TODO: This can be a one-liner, too lazy to do it now. Somehow it's
        # easier to write a comment about something that would take 10 seconds
        # to do than actually doing it
        if self.turn == self.tictactoe.player1:
            self.turn = self.tictactoe.player2
        else:
            self.turn = self.tictactoe.player1

    def play_round(self, tile):
        """
        This function plays a single round of the game. It is called when a
        tile is pressed by the user, and essentially just calls tests to
        determine the current status of the game, and takes action accordingly.

        :param tile: A Tile object, which most important has a player attribute
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)  # waiting cursor
        status = self.tictactoe.play(tile, self.turn)
        QApplication.restoreOverrideCursor()  # cursor is back to normal

        # If the game has ended, display a message with the result
        if status != 0:
            if status == 1:  # player has won the game
                QMessageBox.information(self, self.tr("Victory!"),
                                        self.tr(self.turn.symbol + " won :)"),
                                        QMessageBox.Ok)
            elif status == 2:  # there is a tie
                QMessageBox.warning(self, self.tr("Tie!"),
                                    self.tr("You tied"), QMessageBox.Ok)
            else:  # something impossible happened
                QMessageBox.critical(self, self.tr("Error"),
                                     self.tr("You should never see this"),
                                     QMessageBox.Ok)
            # Restart the game
            self.tictactoe.reset()
            self.turn == self.tictactoe.player1
        else:
            self.switch_turns()  # switch turns
