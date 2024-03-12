import cv2
from PIL import Image
import pytesseract


# Function to find the largest square contour within the Sudoku grid
def find_largest_square_contour(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 3)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        return largest_contour
    else:
        return None


# Function to extract the largest square from a contour
def extract_square_from_contour(img, contour):
    x, y, w, h = cv2.boundingRect(contour)
    square_img = img[y:y + h, x:x + w]
    return square_img


def predict_digit(square):
    # Convert numpy array to PIL Image
    square = Image.fromarray(square)

    # Convert image to grayscale
    square_gray = square.convert('L')

    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(square_gray, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

    # Check if any text is detected
    if text.strip() == '':
        return "."
    else:
        return text.strip()


def process_sudoku_grid(img):
    contour = find_largest_square_contour(img)
    if contour is None:
        print("No Sudoku grid found in the image.")
        return

    square_img = extract_square_from_contour(img, contour)
    square_size = square_img.shape[0] // 9
    crop_pixels = 10
    puzzle = []
    #fig, axes = plt.subplots(9, 9, figsize=(9, 9))
    for row in range(9):
        puzzle_row = []

        for col in range(9):
            small_square_img = square_img[
                               row * square_size + crop_pixels: (row + 1) * square_size - crop_pixels,
                               col * square_size + crop_pixels: (col + 1) * square_size - crop_pixels
                               ]
            #axes[row, col].imshow(cv2.cvtColor(small_square_img, cv2.COLOR_BGR2RGB))
            #axes[row, col].axis('off')
            digit = predict_digit(small_square_img)
            puzzle_row.append(digit)
            # axes[row, col].set_title(digit)
        puzzle.append(puzzle_row)
    # plt.tight_layout()
    # plt.show()
    return puzzle




def main(image_path):
    img = cv2.imread(image_path)
    process_sudoku_grid(img)


if __name__ == "__main__":
    main("sudoku_image.png")
