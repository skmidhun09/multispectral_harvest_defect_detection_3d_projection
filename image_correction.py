import cv2
import numpy as np


def compute_major_color(image_name):
    img = cv2.imread(str(image_name)+".jpg")
    find_vertical_factor(img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
    h, s = np.unravel_index(np.argmax(hist), hist.shape)
    dominant_color_hsv = np.array([h, s, 255], dtype=np.uint8)
    # Convert the dominant color back to BGR format
    dominant_color_bgr = cv2.cvtColor(np.array([[dominant_color_hsv]], dtype=np.uint8), cv2.COLOR_HSV2BGR)
    dominant_color_bgr = dominant_color_bgr[0, 0]
    print("Dominant color (BGR):", dominant_color_bgr)
    return dominant_color_bgr

def find_vertical_factor(img):
    # Initialize variables to track the first and last non-blue pixels
    first_nonblue = None
    last_nonblue = None
    # Loop over each row of pixels in the image from top to bottom
    for y in range(img.shape[0]):
        # Get the current row of pixels
        row = img[y, :, :]
        print(y)

        # Loop over each pixel in the row from left to right
        for x in range(row.shape[0]):
            # Get the current pixel
            pixel = row[x, :]

            # Check if the pixel is blue
            if np.array_equal(pixel, [255, 0, 0]):
                continue

            # Found a non-blue pixel
            if first_nonblue is None:
                # This is the first non-blue pixel, mark its position
                first_nonblue = x
            # Always update the position of the last non-blue pixel
            last_nonblue = x

        # Check if we found any non-blue pixels in this row
        if first_nonblue is not None:
            # Found non-blue pixels in this row, print their positions
            print("First non-blue pixel found at x = %d, y = %d" % (first_nonblue, y))
            print("Last non-blue pixel found at x = %d, y = %d" % (last_nonblue, y))
            # Exit the loop after finding the first non-blue pixels in the image
            #break

    # No non-blue pixels found
    if first_nonblue is None:
        print("No non-blue pixels found in the image")

compute_major_color("3D/1")