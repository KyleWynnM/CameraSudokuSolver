class EasySudoku:
    def __init__(self, board):
        # Initialize any instance variables here
        self.board = board
        self.empty_squares = {}
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] == ".":
                    self.empty_squares[(r, c)] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def solve_sudoku(self) -> None:
        while self.empty_squares:  # Loop until there are no empty squares left
            # Sort empty squares based on the number of candidates
            sorted_coords = sorted(self.empty_squares.keys(), key=lambda coord: len(self.empty_squares[coord]))

            for coord in sorted_coords:
                self.update_candidates(coord)  # Update candidates for each empty square

                if len(self.empty_squares[coord]) == 1:  # If only one candidate left, fill in the square
                    self.board[coord[0]][coord[1]] = self.empty_squares[coord][0]
                    del self.empty_squares[coord]  # Remove filled square from empty_squares

        print(self.board)

    def update_candidates(self, coordinate):
        row_num, col_num = coordinate
        for candidate in self.empty_squares[coordinate][:]:
            if not (self.check_candidate_in_subsquare(candidate, coordinate)
                    and self.check_candidate_in_row(row_num, candidate)
                    and self.check_candidate_in_col(col_num, candidate)):
                self.empty_squares[coordinate].remove(candidate)

    def check_candidate_in_subsquare(self, candidate, coordinate):
        start_r = (coordinate[0] // 3) * 3
        start_c = (coordinate[1] // 3) * 3

        for i in range(start_r, start_r + 3):
            for j in range(start_c, start_c + 3):
                if self.board[i][j] == candidate:
                    return False

        return True

    def check_candidate_in_row(self, row_num, candidate):
        return candidate not in self.board[row_num]

    def check_candidate_in_col(self, col_num, candidate):
        for r in range(len(self.board)):
            if self.board[r][col_num] == candidate:
                return False

        return True

    def fill_squares(self):
        filled_squares = []  # To store coordinates of filled squares
        for coord, candidates in list(
                self.empty_squares.items()):  # Use list() to create a copy of items to avoid dictionary size change during iteration
            if len(candidates) == 1:
                self.board[coord[0]][coord[1]] = candidates[0]
                filled_squares.append(coord)  # Store filled square coordinates
        # Remove filled squares from empty_squares dictionary
        for coord in filled_squares:
            del self.empty_squares[coord]

