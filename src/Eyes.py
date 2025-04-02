"""
Vision module for blackjack game. This module is responsible for extracting
the game state from the screen and converting it into a format that the
controller can understand.
"""
from PIL import Image
import pytesseract
import numpy as np
import cv2


def play(image_name: str):
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
    dealer_hand_edges = edges[0:h//2, :]
    dealer_hand = img[0:h//2, :]

    # Player hand
    player_hand_edges = edges[h//2:h, :]
    player_hand = img[h//2:h, :]

    dealer_cards = get_cards(dealer_hand_edges, dealer_hand)
    player_cards = get_cards(player_hand_edges, player_hand)

    # Crop and get card values
    dealer_values = get_card_value(dealer_cards)
    player_values = get_card_value(player_cards)

    # Run OCR on the cards
    dealer_texts = ocr(dealer_values)
    player_texts = ocr(player_values)

    return [dealer_texts, player_texts]



def get_cards(edges, imgs) -> list:
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
        card_image = imgs[y:y+h, x:x+w]
        card_images.append(card_image)
    
    return card_images
        

def get_card_value(card_list: list) -> list:
    card_values = []
    for card in card_list:
        height, width = card.shape[:2]

        # crop image to northwest corner
        crop_width = int(width * 0.23)
        crop_height = int(height * 0.23)
        card = card[:crop_height, :crop_width]

        # resize card
        card = cv2.resize(card, (width, height))
        card_values.append(card)
    
    return card_values

def ocr(card_images: list) -> list:
    # Run OCR on each card
    card_texts = []
    for card_image in card_images:
        cv2.imshow('Card', card_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        text = pytesseract.image_to_string(card_image, config='--psm 10 -c tessedit_char_whitelist=123456789JQKA')
        text = text.strip()
        if text:
            card_texts.append(text)
    
    return card_texts


def main():
    # Test

    [dealer, player] = play("6_1")

    print("Dealer cards:", dealer)
    print("Player cards:", player)

if __name__ == "__main__":
    main()