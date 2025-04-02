"""
Vision module for blackjack game. This module is responsible for extracting
the game state from the screen and converting it into a format that the
controller can understand.
"""

import numpy as np
import cv2

# get file path of the image from user input
file_path = input("Enter the path to the image: ")
img = cv2.imread(file_path)

# split image in half

# apply Gaussian blur to the image
blurred = cv2.GaussianBlur(img, (5, 5), 0)

# apply canny edge detection
edges = cv2.Canny(blurred, 100, 200)

# display the edges
cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()


# convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# apply Gaussian blur to the image
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# apply adaptive thresholding to the image
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)

# find contours in the image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# draw contours on the original image
for contour in contours:
    # filter contours based on area
    if cv2.contourArea(contour) > 100:
        # draw the contour on the image
        cv2.drawContours(img, [contour], -1, (0, 255, 0), 3)


# display the image
cv2.imshow("Image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()