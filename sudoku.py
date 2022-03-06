import json
filename = "sudoku.json"

start_board = [
      [ 7, 2, 3, 0, 0, 0, 1, 5, 9 ],
      [ 6, 0, 0, 3, 0, 2, 0, 0, 8 ],
      [ 8, 0, 0, 0, 1, 0, 0, 0, 2 ],
      [ 0, 7, 0, 6, 5, 4, 0, 2, 0 ],
      [ 0, 0, 4, 2, 0, 7, 3, 0, 0 ],
      [ 0, 5, 0, 9, 3, 1, 0, 4, 0 ],
      [ 5, 0, 0, 0, 7, 0, 0, 0, 3 ],
      [ 4, 0, 0, 1, 0, 3, 0, 0, 6 ],
      [ 9, 3, 2, 0, 0, 0, 7, 1, 4 ]
    ]

def read_file(filename):
    try:
        file = open(filename, 'r')
        board_text = file.read()
        board_json = json.loads(board_text) 
        return board_json['board']

    except:
        return start_board['board']


def save_file(filename, board):
    '''This function will save the game.'''
    with open(filename, 'w') as file:
        board_json = {}
        board_json['board'] = board
        board_text = json.dumps(board_json)
        file.write(board_text)


def get_valid_move(board):
    '''This function gets a valid move from the user. This function will
       return a tuple containing the valid move with its coordinates.'''

    valid_letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')

        
    # Get valid input for column.
    valid_column = False
    while valid_column != True:
        try:
            input_column = input('Enter a column: ')

        except:
            print('Enter a valid letter. Try again. ')
            continue
        
        if input_column.upper() not in valid_letters:
            print("Enter a column between A-I: ")

        else:
            valid_column = True

    # Make sure to capitalize the column letter.
    input_column = input_column.upper()
    

    # Get valid input for row.
    valid_row = False
    while valid_row != True:
        try:
            input_row = int(input('Enter a row '))

        except:
            print('Enter an integer. Try again. ')
            continue

        if input_row not in range(1,10):
            print('Enter a row number from 1-9. ')
            
        else:
            valid_row = True
            
         # Subtract one to line up with the board(0-8).
        row = input_row -1
        column = input_column
        
        
    # Get valid input for move.
    valid_move = False
    while valid_move != True:
        try: 
            move = int(input(f'Enter a value to insert: '))
        
        except:
            print('Enter an integer. Try again. ')
        
        if move not in range(1,10):
            print('Enter a move from 1 to 9. ')

        else:
            valid_move = True

    # create a tuple of row/column. This is the postion where move will go.
    position = (row,column)

    # Return a tuple containing ((row,column), move))
    return position, move


def parse_column(column):
    '''This function converts column letter to correct number.'''

    # The correct ascii value to find difference of ord(column) - ascii_value.
    ascii_value = 65

    # Get the correct column number.
    parsed_column = (ord(column) - ascii_value)

    return parsed_column
    

def get_hint_location(board):
    '''This function will prompt the player to enter a location to get
       hints for that 9x9 square.'''

    valid_letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')

        
    # Get valid input for column.
    valid_column = False
    while valid_column != True:
        try:
            input_column = input('Enter a column: ')

        except:
            print('Enter a valid letter. Try again. ')
            continue
        
        if input_column.upper() not in valid_letters:
            print("Enter a column between A-I: ")

        else:
            valid_column = True
    
    # Make sure to capitalize the column letter.
    input_column = input_column.upper()

    # Get valid input for row.
    valid_row = False
    while valid_row != True:
        try:
            input_row = int(input('Enter a row '))

        except:
            print('Enter an integer. Try again. ')
            continue

        if input_row not in range(1,10):
            print('Enter a row number from 1-9. ')
            
        else:
            valid_row = True
            
         # Subtract one to line up with the board(0-8).
        row = input_row -1
        column = input_column

    # create a tuple of row/column. This is the postion where move will go.
    position = (row,column)

    # Return a tuple containing ((row,column), move))
    return position
    
    
def possible_solution(row, column, move, board):
    '''This function checks rows/columns/squares to see if the move is
       valid.'''

    # Check for move in the row.
    for check_row in range(0,9):
        if board[row][check_row] == move:
            return False

    # Check for move in the column.
    for check_column in range(0,9):
        if board[check_column][column] == move:
            return False

    # Check for move in given 9x9 square.
    c_coord = (column // 3) * 3
    r_coord = (row // 3) * 3

    for square_row in range(0,3):
        for square_column in range(0,3):
            if (board[r_coord + square_row][c_coord + square_column]) == move:
                return False

    return True


def update_board(position, move, board):
    '''This function takes in a move/position to update the board'''

    # Position gets passed in as a tuple(row,column).
    # Unpack the tuple to get specific row/column locations.
    pos = position
    (row,column) = pos

    # Update the board.
    board[row][column] = (move)

    check(board)

    # Return the current board.
    return board


def display_board(board):
    '''This functino will display the board.'''
    print("    ---COLUMNS---")
    print("   A B C D E F G H I")
    for row in range(len(board)):

        if row == 3 or row == 6:
            print("-------------------")

        print("", row + 1, end=' ')
           
        for column in range(len(board[0])):
            if column%3 == 0:
                print("\b|", end ="")

            print(str(board[row][column])+" ", end="")
        print("\b|")
    check(board)
        
print("-------------------")


def hint(row, column, board):
    '''This function will give the player hints as to which moves are
       possible in a given square.'''

    # initialize a set to compare existing values with possible values.
    vals = set()
    hints = set()

    # Add numbers 1-9 to the hints set.
    for i in range(1,10):
        hints.add(i)
    
    # Check for move in given 9x9 square.
    c_coord = (column // 3) * 3
    r_coord = (row // 3) * 3

    # Loop through 9x9 square and add existing values to the set vals.
    for square_row in range(0,3):
        for square_column in range(0,3):
            vals.add(((board[r_coord + square_row][c_coord + square_column])))

    # Compare the difference from the hints set and the vals set. The 
    # difference will be all the possible values. 
    return(set(hints).difference(vals))

def check(array):
    zeroCount = 0
    for i in array:
        if(0 in i):
            zeroCount += 1
    if(zeroCount == 0):
        print("You win!")
    else: 
        if(zeroCount == 1):
            print(f"There is one space left.")
        else:
            print(f"There are {zeroCount} spaces left.")

def main():
    '''This function controls the flow of the program.'''

    print('Welcome to Sudoku! Choose from the menu options below to play \
the game! Good luck!')

    # Game loop.
    action= ' '
    while action.upper() != 'Q':

         # Call read_file to get the board.
        board = read_file(filename)

        # Display the board each time through the loop.
        display_board(board)

        # Menu option. Player may choose any of these options until they 
        # Type 'Q'.
        print("1. Play one turn. ")
        print("2. Give me a hint. ")
        print("3. Start over with fresh board. ")
        action = str(input("Choose from the options above. Type 'Q' to quit. "))
        
        # Play one turn.
        if action == '1':

            valid_move = get_valid_move(board)
            (position, move) = valid_move
            row, column = position
            move = move

            column = parse_column(column)

            position = row, column

            possible_solution(row, column, move, board)

            # Update the board if space is available and value is possible.
            if board[row][column] == 0:
                if possible_solution(row, column, move, board) == True:
                    update_board(position, move, board)
            
                else: 
                    print('Invalid move')
            
            else: 
                print('That spot is taken.')

            # Save the board.
            save_file(filename, board)

            print()
        
        # Give a hint.
        if action == '2':

            valid_move = get_hint_location(board)
            position = valid_move
            row, column = position

            # Parse the column from a letter to the correct column number.
            column = parse_column(column)

            # Diplay the possible values in the 9x9 board.
            display_hints = hint(row, column, board)

            print(f"Valid moves in this square are: {display_hints} ")

            print()
        
        # Start over with new fresh board.
        if action == '3':
            verify = input('Are you sure you want to start over? Y/N ')

            if verify.upper() == 'Y':
                save_file(filename, start_board)
            
            else:
                print('Pheww that was a close one. ')
            
 
        
if __name__ == "__main__":
    main()
    