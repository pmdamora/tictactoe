from tictactoe import constants


class TicTacToe:
    """
    TicTacToe is the main game model. It contains any classes and functions
    necessary to the game, aside from the UI itself.
    """
    class Tile:
        def __init__(self, row, column, number, player=None):
            """
            :param row: an integer row number
            :param column: an integer column number
            :param number: an integer tile number
            :param player: the player currently occupying the tile
            """
            self.row, self.column = row, column
            self.player = player
            self.number = number
            self.delegate = None

        def __str__(self):
            """Overload the toString method to get a prettier output"""
            return str(self.player) if self.player is not None else "☐"

        def update(self):
            """
            If there is a change to a Tile, updated the corresponding delegate
            """
            if self.delegate is not None:
                self.delegate.updateButton(self)

        def set(self, player):
            """
            Set a new player to the Tile.

            :param player: the player currently occupying the tile
            """
            self.player = player
            self.update()

        def reset(self):
            """Reset the Tile to its default state"""
            self.player = None
            self.update()

    class Player:
        """
        Player defines any properties and function associated with players in
        the game.
        """
        def __init__(self, symbol):
            """
            :param symbol: the text symbol the belong to the Player
            """
            self.symbol = symbol
            self.name = ""

        def __str__(self):
            """Overload the toString method to get a prettier output"""
            return self.name + " (" + self.symbol + ")"

    def __init__(self):
        self.size = 3

        # Create instances of the Player class for each player
        self.player1 = TicTacToe.Player(constants.PLAYER_SYMBOLS[1])
        self.player2 = TicTacToe.Player(constants.PLAYER_SYMBOLS[2])

        self.board = {}
        num = 0

        # Fill the board with empty tiles
        for row in range(self.size):
            for column in range(self.size):
                self.board[row, column] = TicTacToe.Tile(row, column, num)
                num += 1

    def __contains__(self, tile):
        """
        Overrides 'in', to iterate through tiles in the board. Determines if a
        tile is in the board.

        :param tile: an instance of the Tile class
        """
        return tile in self.board

    def __iter__(self):
        """Makes the class instance of TicTacToe iterable."""
        return self.board.values().__iter__()

    def game_status(self, player):
        """
        Returns the current status of the game.

        :param player: the currently active player
        :rval : the status of the game as an integer in [1 0 2]. 1 means the
        active player has won the game. 0 means the game is not over and will
        continue. 2 means there is a tie and the game is over.
        """
        # Sort all of the tiles in ascending order by their position
        tiles = sorted(list(self.board.values()), key=lambda tile: tile.number)

        # Simple one-liner. Returns true if any win-condition is met in the
        # current board, and false otherwise
        game_over = any(all(tiles[i-1].player == player for i in combo)
                        for combo in constants.WIN_COMBINATIONS)

        if game_over:  # the game has been won
            return 1
        elif any(t.player is None for t in tiles):  # there are moves left
            return 0
        else:  # there is a tie
            return 2

    def play(self, tile, player):
        """
        Plays a single round of TicTacToe. Expects a specific tile object
        as input.

        :param tile: an instance of the Tile class
        :param player: the currently active player
        :rval status: the status of the game as an integer in [1 0 2]. 1 means
        the active player has won the game. 0 means the game is not over and
        will continue. 2 means there is a tie and the game is over.
        """
        tile.set(player)
        status = self.game_status(player)

        return status

    def reset(self):
        """Resets the game to its default state"""
        for tile in self:  # see __contains__ override
            tile.reset()
