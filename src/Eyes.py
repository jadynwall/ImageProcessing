"""
Vision module for blackjack game. This module is responsible for extracting
the game state from the screen and converting it into a format that the
controller can understand.
"""
from PIL import Image
import pytesseract
import numpy as np
import cv2


def get_card_lists(image_name: str):
    # get file path of the image from user input
    img = cv2.imread(f"images/{image_name}.jpg")

    # convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # apply Gaussian blur to the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # apply canny edge detection
    edges = cv2.Canny(blurred, 100, 200)

    # Splitting image down the middle halfway
    h, w = edges.shape[:2]

    # Dealer hand
    dealer_hand = edges[0:h//2, :]

    # Player hand
    player_hand = edges[h//2:h, :]

    




def get_cards(img) -> list:
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
    
    return card_images
        

def isolate_card_value(original_images: list) -> list:
    

def ocr(card_images: list) -> list:
    # Run OCR on each card
    card_texts = []
    for card_image in card_images:
        card_text = pytesseract.image_to_string(card_image, config='--psm 10')
        card_texts.append(card_text)
    
    return card_texts



# # run OCR on the dealer hand
# dealer_text = pytesseract.image_to_boxes(dealer_hand, config='--psm 10')
# print("Dealer Hand Text:", dealer_text)

# # Convert dealer_hand and player_hand to BGR format for colored bounding boxes
# dealer_hand_bgr = cv2.cvtColor(dealer_hand, cv2.COLOR_GRAY2BGR)
# player_hand_bgr = cv2.cvtColor(player_hand, cv2.COLOR_GRAY2BGR)


# # run OCR on the player hand
# player_text = pytesseract.image_to_boxes(player_hand, config='--psm 10')
# print("Player Hand Text:", player_text)


# Display the images with bounding boxes
cv2.imshow("Player Hand", player_hand)
cv2.imshow("Dealer Hand", dealer_hand)
cv2.waitKey(0)
cv2.destroyAllWindows()
