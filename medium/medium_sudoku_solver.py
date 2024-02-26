class MediumSudoku:
    def __init__(self, board):
        # Initialize any instance variables here
        self.board = board
        self.empty_squares = {}
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] == ".":
                    self.empty_squares[(r, c)] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def print_board(self, board):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 21)  # Print horizontal line every 3 rows
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")  # Print vertical line every 3 columns
                print(f"{board[i][j]:^2}", end="")
            print()  # Move to the next line after printing each row

    def solve_sudoku(self, board) -> None:
        board_copy = [row[:] for row in board]  # Create a copy of the original board
        empty_squares_copy = {}
        for coord, candidates in self.empty_squares.items():
            empty_squares_copy[coord] = candidates.copy()  # Manual deep copy

        result = self.recursive_solve(board_copy, empty_squares_copy)
        if not result:
            print("No solution")
            return

        self.board = [row[:] for row in result]
        self.print_board(self.board)

    def recursive_solve(self, board, empty_squares):
        board_copy = [row[:] for row in board]  # Create a copy of the original board
        empty_squares_copy = {}
        for coord, candidates in empty_squares.items():
            empty_squares_copy[coord] = candidates.copy()  # Manual deep copy

        while empty_squares_copy:  # Loop until there are no empty squares left
            #self.print_board(board_copy)
            print(empty_squares_copy)
            prev_num_empties = len(empty_squares_copy.keys())
            # Sort empty squares based on the number of candidates
            sorted_coords = sorted(empty_squares_copy.keys(), key=lambda coord: len(empty_squares_copy[coord]))

            for coord in sorted_coords:
                board_copy, empty_squares_copy = self.update_candidates(coord, board_copy,
                                                                        empty_squares_copy)  # Update candidates for each empty square

                if len(empty_squares_copy[coord]) == 1:  # If only one candidate left, fill in the square
                    board_copy[coord[0]][coord[1]] = empty_squares_copy[coord][0]
                    del empty_squares_copy[coord]  # Remove filled square from empty_squares

            current_num_empties = len(empty_squares_copy.keys())

            if not empty_squares_copy:
                return board_copy
            # if naked singles are tapped out
            if current_num_empties == prev_num_empties:
                print("breaking")
                break

        if self.has_empty_arrays(empty_squares_copy):
            print("impossible solution; backtracking")
            return False

        # only need to check one square, if it's valid, then you can let the recursion handle the other possible empties
        empty_square = sorted(empty_squares_copy.keys(), key=lambda coord: len(empty_squares_copy[coord]))[0]

        guess_empty_squares = {}
        for coord, candidates in empty_squares_copy.items():
            if coord != empty_square:
                guess_empty_squares[coord] = candidates.copy()  # Manual deep copy

        print("attempting to fill", empty_square)
        for candidate in empty_squares_copy[empty_square]:
            guess_board = [row[:] for row in board_copy]
            guess_board[empty_square[0]][empty_square[1]] = candidate
            print("GUESSING", candidate, empty_square)
            print("empty squares", empty_squares_copy)
            # self.print_board(guess_board)
            attempt = self.recursive_solve(guess_board, guess_empty_squares)

            if attempt:
                return attempt

        return False

    def has_empty_arrays(self, dictionary):
        for value in dictionary.values():
            if isinstance(value, list) and not value:
                return True
        return False

    def update_candidates(self, coordinate, board, empty_squares):
        row_num, col_num = coordinate
        updated_empty_squares = {}
        for coord, candidates in empty_squares.items():
            updated_empty_squares[coord] = candidates.copy()  # Manual deep copy
        updated_board = [row[:] for row in board]  # Create a copy of the board to update

        for candidate in updated_empty_squares[coordinate][:]:
            if not (self.check_candidate_in_subsquare(candidate, coordinate, updated_board)
                    and self.check_candidate_in_row(row_num, candidate, updated_board)
                    and self.check_candidate_in_col(col_num, candidate, updated_board)):
                updated_empty_squares[coordinate].remove(candidate)

        return updated_board, updated_empty_squares

    def check_candidate_in_subsquare(self, candidate, coordinate, board):
        start_r = (coordinate[0] // 3) * 3
        start_c = (coordinate[1] // 3) * 3

        for i in range(start_r, start_r + 3):
            for j in range(start_c, start_c + 3):
                if board[i][j] == candidate:
                    return False

        return True

    def check_candidate_in_row(self, row_num, candidate, board):
        return candidate not in board[row_num]

    def check_candidate_in_col(self, col_num, candidate, board):
        for r in range(len(board)):
            if board[r][col_num] == candidate:
                return False

        return True
