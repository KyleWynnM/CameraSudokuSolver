import cv2
import numpy as np
import tkinter as tk
from image_processer import process_sudoku_grid
from medium.medium_sudoku_solver import MediumSudoku

# Create Sudoku grid editor GUI
def create_grid_editor(array):
    def save_grid(entries, root):
        updated_grid = []
        for row_entries in entries:
            row_values = []
            for entry in row_entries:
                value = entry.get()
                row_values.append(value if value else ".")
            updated_grid.append(row_values)
        root.destroy()
        solve_sudoku(updated_grid)

    root = tk.Tk()
    root.title("Sudoku Grid Editor")

    entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            if array[i][j] == ".":
                entry = tk.Entry(root, width=2)
            else:
                entry = tk.Entry(root, width=2)
                entry.insert(0, array[i][j])
            entry.grid(row=i, column=j)
            row_entries.append(entry)
        entries.append(row_entries)

    save_button = tk.Button(root, text="Save", command=lambda: save_grid(entries, root))
    save_button.grid(row=9, columnspan=9)

    root.mainloop()

# Function to solve Sudoku puzzle
def solve_sudoku(sudoku_board):
    solver = MediumSudoku(sudoku_board)
    print("Solving Sudoku puzzle...")
    solved_board = solver.solve_sudoku(sudoku_board)

    # Display the solved Sudoku grid
    if solved_board:
        solved_img = create_sudoku_image(solved_board, (450, 450))
        cv2.imshow("Solved Sudoku", solved_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Failed to solve Sudoku puzzle.")

# Function to create Sudoku grid image
def create_sudoku_image(board, img_shape):
    solved_img = np.ones(img_shape, dtype=np.uint8) * 255
    black = (0, 0, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cell_height = img_shape[0] // 9
    cell_width = img_shape[1] // 9
    for i in range(1, 9):
        thickness = 2 if i % 3 == 0 else 1
        cv2.line(solved_img, (0, i * cell_height), (img_shape[1], i * cell_height), black, thickness)
        cv2.line(solved_img, (i * cell_width, 0), (i * cell_width, img_shape[0]), black, thickness)
    for i in range(9):
        for j in range(9):
            if board[i][j] != ".":
                x = j * cell_width + cell_width // 3
                y = i * cell_height + 2 * cell_height // 3
                cv2.putText(solved_img, board[i][j], (x, y), font, 1, black, 2, cv2.LINE_AA)
    return solved_img

# Function to solve Sudoku from image
def solve_sudoku_from_image(image_path):
    img = cv2.imread(image_path)
    sudoku_board = process_sudoku_grid(img)
    create_grid_editor(sudoku_board)

# Main function
def main():
    image_path = "sudoku_image.png"
    solve_sudoku_from_image(image_path)

if __name__ == "__main__":
    main()
