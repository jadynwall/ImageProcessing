"""
Vision module for blackjack game. This module is responsible for extracting
the game state from the screen and converting it into a format that the
controller can understand.
"""
from PIL import Image
import pytesseract
import numpy as np
import cv2

# get file path of the image from user input
file_path = input("Enter the name of the image (without extension): ")
img = cv2.imread(f"images/{file_path}.jpg")

# convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ocr
text = pytesseract.image_to_string(gray, config='--psm 10')
print("OCR Text:", text)

# apply Gaussian blur to the image
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# apply canny edge detection
edges = cv2.Canny(blurred, 100, 200)

# Detect contours to find individual cards
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours based on area to remove noise
card_contours = [contour for contour in contours if cv2.contourArea(contour) > 1000]

print(f"Number of cards detected: {len(card_contours)}")

# Create a new image for each card
card_images = []
for i, contour in enumerate(card_contours):
    # Get bounding box for each card
    x, y, w, h = cv2.boundingRect(contour)
    
    # Extract the card from the original image
    card_image = img[y:y+h, x:x+w]
    card_images.append(card_image)
    
    # Save the card image
    card_filename = f"card_{i+1}.jpg"
    cv2.imwrite(card_filename, card_image)
    print(f"Saved card image: {card_filename}")

# Optional: Draw bounding boxes around detected cards on the original image
for contour in card_contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Green bounding box

# Display the original image with bounding boxes
cv2.imshow("Detected Cards", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Splitting image down the middle halfway
h, w = edges.shape[:2]

# Dealer hand
dealer_hand = edges[0:h//2, :]

# Player hand
player_hand = edges[h//2:h, :]

# run OCR on the dealer hand
dealer_text = pytesseract.image_to_boxes(dealer_hand, config='--psm 10')
print("Dealer Hand Text:", dealer_text)

# Convert dealer_hand and player_hand to BGR format for colored bounding boxes
dealer_hand_bgr = cv2.cvtColor(dealer_hand, cv2.COLOR_GRAY2BGR)
player_hand_bgr = cv2.cvtColor(player_hand, cv2.COLOR_GRAY2BGR)

# Draw bounding boxes for dealer hand
for box in dealer_text.splitlines():
    b = box.split()
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    h_dealer = dealer_hand_bgr.shape[0]
    cv2.rectangle(dealer_hand_bgr, (x, h_dealer - y), (w, h_dealer - h), (0, 0, 255), 2)  # Red bounding box

# run OCR on the player hand
player_text = pytesseract.image_to_boxes(player_hand, config='--psm 10')
print("Player Hand Text:", player_text)

# Draw bounding boxes for player hand
for box in player_text.splitlines():
    b = box.split()
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    h_player = player_hand_bgr.shape[0]
    cv2.rectangle(player_hand_bgr, (x, h_player - y), (w, h_player - h), (0, 0, 255), 2)  # Red bounding box

# Display the images with bounding boxes
cv2.imshow("Player Hand", player_hand_bgr)
cv2.imshow("Dealer Hand", dealer_hand_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()
