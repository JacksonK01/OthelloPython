import random

# Index 0 = Y
# Index 1 = X
DIRECTIONS = [[0, 1], [1, 1],
              [1, 0], [1, -1],
              [0, -1], [-1, -1],
              [-1, 0], [-1, 1]]

COLORS = {"white": 1,
          "black": 2}


def getHeightOfBoard(board):
    """
        Description:
            This function gets the height of the input board

        Args:
            board (List): Given board.

        Returns:
            int: height of board
    """
    return len(board)


def getWidthOfBoard(board):
    """
        Description:
            This function gets the width of the input board

        Args:
            board (List): Given board.

        Returns:
            int: width of board
        """
    return len(board[0])


def isInBounds(board, r, c):
    """
        Description:
            This function checks to see if the coordinates
            are within the board's limits

        Args:
            board (List): Given board
            r (int): Selected Row
            c (int): Selected Column

        Returns:
            boolean: result of the condition
        """
    return getHeightOfBoard(board) > r >= 0 and getWidthOfBoard(board) > c >= 0


def getSpot(board, r, c):
    """
        Description:
            This function checks if the given row and column
            are in bounds first to prevent a crash, and
            returns the requested spot on the board.

        Args:
            board (List): Given board
            r (int): Selected Row
            c (int): Selected Column

        Returns:
            int: spot on the board or 0 if
            it's out of bounds as a safety measure
        """
    if not isInBounds(board, r, c):
        return 0
    return board[r][c]


def setSpot(board, r, c, color):
    """
        Description:
            This function checks if the given row and column
            are in bounds first to prevent a crash, and
            sets the requested spot on the board.

        Args:
            board (List): Given board
            r (int): Selected Row
            c (int): Selected Column
        """
    if isInBounds(board, r, c):
        board[r][c] = COLORS[color]


def isSpotEqualToColor(board, r, c, color):
    """
        Description:
            This function checks if the given row and column
            are in bounds first to prevent a crash, and
            will check to see if the input color is equal
            to the spot it is checking. This is useful
            later in the code to make the conditions
            more readable.

        Args:
            board (List): Given board
            r (int): Selected Row
            c (int): Selected Column
            color (Str): Key for COLORS constant

        Returns:
            boolean: True or False based on the condition
            """
    return getSpot(board, r, c) == COLORS[color]


def isSpotEmpty(board, r, c):
    """
        Description:
            This function checks if the given row and column
            are in bounds first to prevent a crash,
            and checks whether the spot is empty
            aka if the spot is 0 on the grid

        Args:
            board (List): Given board
            r (int): Selected Row
            c (int): Selected Column

        Returns:
            boolean: True or False based on condition
            """
    return getSpot(board, r, c) == 0


def getAmountOfAColor(board, color):
    """
        Description:
            This function counts the amount of
            color pieces on the board based on
            the color input.

        Args:
            board (List): Given board
            color (Str): Key for the constant COLOR

        Returns:
            int: Amount of given color
                """
    amount = 0
    for r in range(getHeightOfBoard(board)):
        for c in range(getWidthOfBoard(board)):
            if isSpotEqualToColor(board, r, c, color):
                amount += 1
    return amount


def set_up_board(width, height):
    """
            Description:
                This function checks sets up a board depending on
                the width and height. It also sets up the black
                and white in the center.

            Args:
                width (int): width of the board
                height (int): height of board

            Returns:
                List: List with nested Lists that represents the board
                    """
    board = []
    for r in range(height):
        dummy = []
        for c in range(width):
            dummy.append(0)
        board.append(dummy)

    board[len(board) // 2][len(board[0]) // 2] = 1
    board[len(board) // 2][len(board[0]) // 2 - 1] = 2
    board[len(board) // 2 - 1][len(board[0]) // 2] = 2
    board[len(board) // 2 - 1][len(board[0]) // 2 - 1] = 1
    return board


def is_valid_move(board, row, col, color):
    """
        Description:
            This function will check if the given row
            and column are valid spots on the board by
            using the constant DIRECTIONS which the program
            will check in all 8 possible directions. Once
            the program finds a spot that is not 0 and
            is not the same color, it'll keep moving in that
            direction until it finds the given color

        Args:
            board (List): given board
            row (int): given row
            col (int): given column
            color (Str): Key for COLORS constant

        Returns:
            boolean: whether the spot is valid
                """
    valid = False
    if isSpotEmpty(board, row, col):
        for move_check in DIRECTIONS:
            idxY = row + move_check[0]
            idxX = col + move_check[1]
            active = (not isSpotEmpty(board, idxY, idxX) and
                      not isSpotEqualToColor(board, idxY, idxX, color))
            while active:
                idxY += move_check[0]
                idxX += move_check[1]
                valid = isSpotEqualToColor(board, idxY, idxX, color)
                active = not valid and not isSpotEmpty(board, idxY, idxX)
            if valid:
                return valid
    return valid


def flip(board, row, col, color):
    """
        Description:
            Once the program runs the same process as
            is_valid_move it'll start to
            go backwards from the given color spot
            while pasting the given color along
            the way until it reaches the given spot


        Args:
            board (List): given board
            row (int): given row
            col (int): given column
            color (Str): Key for COLORS constant
                """
    for move_check in DIRECTIONS:
        idxY = row + move_check[0]
        idxX = col + move_check[1]
        active = (not isSpotEmpty(board, idxY, idxX) and
                  not isSpotEqualToColor(board, idxY, idxX, color))
        while active:
            idxY += move_check[0]
            idxX += move_check[1]
            active = not isSpotEmpty(board, idxY, idxX)
            backwards = isSpotEqualToColor(board, idxY, idxX, color)
            while backwards:
                idxY -= move_check[0]
                idxX -= move_check[1]
                backwards = not (idxY == row and idxX == col)
                setSpot(board, idxY, idxX, color)
                active = False


def get_valid_moves(board, color):
    """
        Description:
            This function uses a for loop and a
            nested for loop to evaluate every possible
            position on the board while running the
            is_valid_move function, and will append
            valid spots to a list as tuples

        Args:
            board (List): given board
            color (Str): Key for COLORS constant

        Returns:
            List: list will contain all current possible moves
                """
    valid_moves = []
    for r in range(getHeightOfBoard(board)):
        for c in range(getWidthOfBoard(board)):
            if is_valid_move(board, r, c, color):
                dummy = [r, c]
                valid_moves.append(tuple(dummy))
    return valid_moves


def select_next_play_human(board, color):
    """
        Description:
            This function asks the user for an
            input while looping until it gets a valid
            input

        Args:
            board (List): given board
            color (Str): Key for COLORS constant

        Returns:
            Tuple: Will contain a valid spot from the user
                """
    valid_moves = get_valid_moves(board, color)
    print(valid_moves)
    isInputValid = False
    if len(valid_moves) > 0:
        while not isInputValid:
            try:
                inputRow = int(input("Enter desired row (Y-axis): "))
                inputCol = int(input("Enter desired column (X-axis): "))
                isInputValid = is_valid_move(board, inputRow, inputCol, color)
                if not isInputValid:
                    print("Coordinates aren't valid")
            except ValueError:
                print("Error, not valid datatypes")
    return tuple([inputRow, inputCol])


def select_next_play_ai(board, color):
    """
        Description:
            This function is how the AI
            will choose it's next move
            which it does so by finding the
            highest net gain and returning
            that move

        Args:
            board (List): given board
            color (Str): Key for COLORS constant

        Returns:
            Tuple: Will contain a move that
            has the highest net gain
                """
    totals = []
    grid_spot_list = []
    amount = 0
    for r in range(getHeightOfBoard(board)):
        for c in range(getWidthOfBoard(board)):
            if is_valid_move(board, r, c, color):
                for move_check in DIRECTIONS:
                    idxY = r + move_check[0]
                    idxX = c + move_check[1]
                    active = (not isSpotEmpty(board, idxY, idxX) and
                              not isSpotEqualToColor(board, idxY, idxX, color))
                    valid = False
                    while active:
                        amount += 1
                        idxY += move_check[0]
                        idxX += move_check[1]
                        valid = isSpotEqualToColor(board, idxY, idxX, color)
                        active = (not valid and
                                  not isSpotEmpty(board, idxY, idxX))
                    if valid:
                        totals.append(amount)
                        spots = [r, c]
                        grid_spot_list.append(tuple(spots))
    i = totals.index(max(totals))
    return grid_spot_list[i]


def select_next_play_random(board, color):
    """
        Description:
            This function uses get_valid_moves()
            to get a list of possible moves which it
            then randomly chooses a value from the list

        Args:
            board (List): given board
            color (Str): Key for COLORS constant

        Returns:
            Tuple: Will contain a valid spot from the user
                """
    valid_moves = get_valid_moves(board, color)
    i = 0
    if len(valid_moves) > 0:
        i = random.randint(0, len(valid_moves) - 1)
    return tuple(valid_moves[i])


def human_vs_random():
    """
        Description:
            This function starts the human
            versus random game mode
                """
    colorState = "white"
    boardState = set_up_board(8, 8)
    while len(get_valid_moves(boardState, colorState)) != 0:
        print("\n" + get_board_as_string(boardState))
        if colorState == "white":
            next_move = select_next_play_human(boardState, "white")
            flip(boardState, next_move[0], next_move[1], "white")
            colorState = "black"
        else:
            next_move = select_next_play_random(boardState, "black")
            flip(boardState, next_move[0], next_move[1], "black")
            colorState = "white"
            print(f"Random picked row: {next_move[0]}"
                  f" and column: {next_move[1]}")

    player1 = getAmountOfAColor(boardState, "white")
    player2 = getAmountOfAColor(boardState, "black")
    if player1 > player2:
        print(f"White wins with a score: {player1}"
              f" \nBlack's score was: {player2}")
        return 1
    if player1 < player2:
        print(f"Black wins with a score: {player2}"
              f" \nWhite's score was: {player1}")
        return 2
    print(f"Black and white ties with {player1}")
    return 0


def ai_vs_random():
    """
         Description:
             This function starts the AI
             versus random game mode
                 """
    boardState = set_up_board(8, 8)
    colorState = "white"
    while len(get_valid_moves(boardState, colorState)) != 0:
        print("\n" + get_board_as_string(boardState))
        if colorState == "white":
            next_move = select_next_play_ai(boardState, "white")
            flip(boardState, next_move[0], next_move[1], "white")
            colorState = "black"
            print(f"Random picked row: {next_move[0]}"
                  f" and column: {next_move[1]}")
        else:
            next_move = select_next_play_random(boardState, "black")
            flip(boardState, next_move[0], next_move[1], "black")
            colorState = "white"
            print(f"Random picked row: {next_move[0]}"
                  f" and column: {next_move[1]}")

    print("\n" + get_board_as_string(boardState))
    player1 = getAmountOfAColor(boardState, "white")
    player2 = getAmountOfAColor(boardState, "black")
    if player1 > player2:
        print("Player 1 Wins")
        return 1
    if player1 < player2:
        print("Player 2 Wins")
        return 2
    print("It was a tie")
    return 0


def random_vs_random():
    """
         Description:
             This function starts the random
             versus random game mode
                 """
    boardState = set_up_board(8, 8)
    colorState = "white"
    while len(get_valid_moves(boardState, colorState)) != 0:
        print("\n" + get_board_as_string(boardState))
        if colorState == "white":
            next_move = select_next_play_random(boardState, "white")
            flip(boardState, next_move[0], next_move[1], "white")
            colorState = "black"
            print(f"Random picked row: {next_move[0]}"
                  f" and column: {next_move[1]}")
        else:
            next_move = select_next_play_random(boardState, "black")
            flip(boardState, next_move[0], next_move[1], "black")
            colorState = "white"
            print(f"Random picked row: {next_move[0]}"
                  f" and column: {next_move[1]}")

    print("\n" + get_board_as_string(boardState))
    player1 = getAmountOfAColor(boardState, "white")
    player2 = getAmountOfAColor(boardState, "black")
    if player1 > player2:
        print("Player 1 Wins")
        return 1
    if player1 < player2:
        print("Player 2 Wins")
        return 2
    print("It was a tie")
    return 0


# Could not figure out a nicer way to write this
def get_board_as_string(givenBoard):
    """
        Description:
            This function reads the board
            and interprets it into text based
            graphics

        Args:
            board (List): given board

        Returns:
            Str: Will return a graphics
            version of the board
                """
    returnBoard = ""

    # Creates the number indexes for column
    columnIndex = 0
    for index in range(getWidthOfBoard(givenBoard)):
        if index == 0:
            returnBoard += '  '
        returnBoard = returnBoard + f' {columnIndex}'
        columnIndex += 1
        if columnIndex > 9:
            columnIndex = 0
    returnBoard = returnBoard + "\n"

    # Does the same for rows
    rowIndex = 0
    for r in range(getHeightOfBoard(givenBoard)):
        # Here creates the Dividers between each row
        for top in range(getWidthOfBoard(givenBoard)):
            if top == 0:
                returnBoard = returnBoard + "  +-"
            else:
                returnBoard = returnBoard + "+-"
        returnBoard = returnBoard + "+\n"
        for c in range(getWidthOfBoard(givenBoard)):
            if c == 0:
                returnBoard = returnBoard + f'{rowIndex}' + " |"
                rowIndex += 1
                if rowIndex > 9:
                    rowIndex = 0
            else:
                returnBoard = returnBoard + "|"
            if getSpot(givenBoard, r, c) == 1:
                returnBoard = returnBoard + "○"
            elif getSpot(givenBoard, r, c) == 2:
                returnBoard = returnBoard + "●"
            else:
                returnBoard = returnBoard + " "
        returnBoard = returnBoard + "|\n"

    # This adds the bottom of the board
    for bottom in range(getWidthOfBoard(givenBoard)):
        if bottom == 0:
            returnBoard = returnBoard + "  +-"
        else:
            returnBoard = returnBoard + "+-"
    returnBoard += "+"
    return returnBoard
