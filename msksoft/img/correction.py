import cv2
import numpy as np
from PIL import Image


def compute_major_color(image_name):
    img = cv2.imread(str(image_name) + ".jpg")
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
    xlist = []
    ylist = []
    row = None
    for y in range(img.shape[0]):
        # Get the current row of pixels
        row = img[y, :, :]
        # Loop over each pixel in the row from left to right
        for x in range(row.shape[0]):
            pixel = row[x, :]
            if pixel[0] < 200:
                xlist.append(x)
                ylist.append(y)
    y_max = img.shape[0]
    x_max = row.shape[0]
    y_top = min(ylist)
    y_bottom = y_max - max(ylist)
    y_correct = y_bottom - y_top
    x_left = min(xlist)
    x_right = x_max - max(xlist)
    x_correct = x_right - x_left
    xtl = 0
    ytl = 0
    xbr = x_max
    ybr = y_max
    #print("x_left "+str(x_left)+" x right"+str(x_right))
    if y_correct < 0:
        ytl = ytl - y_correct
    else:
        ybr = ybr - y_correct
    if x_correct < 0:
        xtl = xtl - x_correct
    else:
        xbr = xbr - x_correct
    cropped_img = img[ytl:ybr, xtl:xbr]
    return cropped_img

def correctedPIl(image):
    cv_image = find_vertical_factor(image)
    # Convert the color from BGR to RGB
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    # Convert the OpenCV image to a PIL image
    pil_image = Image.fromarray(cv_image)
    #pil_image.show()
    return pil_image

#compute_major_color("../../input/1")
