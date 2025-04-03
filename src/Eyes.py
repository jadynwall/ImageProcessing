"""
Vision module for blackjack game. This module is responsible for extracting
the game state from the screen and converting it into a format that the
controller can understand.
"""

import numpy as np
import cv2
import easyocr

log = False


def play(image_name: str):
    # Read input image.
    img = cv2.imread(f"images/{image_name}.jpg")

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if log:
        cv2.imshow('Gray Scale', gray)
        cv2.waitKey(0)

    # Apply Gaussian blur to the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    if log:
        cv2.imshow('Gaussian Blurred', blurred)
        cv2.waitKey(0)

    # Apply canny edge detection. Needed to detect contours
    edges = cv2.Canny(blurred, 100, 200)

    if log:
        cv2.imshow('Canny Edge Detector', edges)
        cv2.waitKey(0)

    # Splitting image down the middle halfway
    h, w = edges.shape[:2]

    # Dealer hand
    dealer_hand_edges = edges[0:h//2, :]
    dealer_hand = gray[0:h//2, :]

    # Player hand
    player_hand_edges = edges[h//2:h, :]
    player_hand = gray[h//2:h, :]

    dealer_cards = get_cards(dealer_hand_edges, dealer_hand)
    player_cards = get_cards(player_hand_edges, player_hand)

    # Sharpen the images
    dealer_sharpened = sharp(dealer_cards)
    player_sharpened = sharp(player_cards)

    # Crop and get card values
    dealer_values = get_card_value(dealer_sharpened)
    player_values = get_card_value(player_sharpened)

    # Run OCR on the cards
    dealer_texts, d_adj = ocr(dealer_values)
    player_texts, p_adj = ocr(player_values)

    # Number of adjustments from OCR results made
    # print(f"Dealer adjustments: {d_adj}")
    # print(f"Player adjustments: {p_adj}")

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
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int32(box)

        # Order the points in a consistent order: top-left, top-right, bottom-right, bottom-left
        box = sorted(box, key=lambda x: (x[1], x[0]))  # Sort by y, then x
        top_left, top_right = sorted(box[:2], key=lambda x: x[0])  # Top two points
        bottom_left, bottom_right = sorted(box[2:], key=lambda x: x[0])  # Bottom two points

        # Define the width and height of the new image
        width = int(max(np.linalg.norm(top_right - top_left), np.linalg.norm(bottom_right - bottom_left)))
        height = int(max(np.linalg.norm(top_left - bottom_left), np.linalg.norm(top_right - bottom_right)))

        # Define the destination points for the perspective transform
        dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")

        # Compute the perspective transform matrix
        src = np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")
        M = cv2.getPerspectiveTransform(src, dst)

        # Apply the perspective transformation to get an upright card image
        card_image = cv2.warpPerspective(imgs, M, (width, height))
        
        if log:
            cv2.imshow('Isolate card via contours', card_image)
            cv2.namedWindow('Isolate card via contours', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Isolate card via contours', 700, 700)
            cv2.waitKey(0)

        card_images.append(card_image)
    
    return card_images

def sharp(card_list: list) -> list:
    sharpened_cards = []
    for card in card_list:
        # First blur the image
        gaussian_blur = cv2.GaussianBlur(card, (7, 7), sigmaX=2)

        # Sharpen the image by subtracting a blurred version of the image (weighted empirically)
        sharpened = cv2.addWeighted(card, 3.5, gaussian_blur, -2.5, 0)

        if log:
            cv2.imshow('Sharpen', sharpened)
            cv2.namedWindow('Sharpen', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Sharpen', 700, 700)
            cv2.waitKey(0)


        sharpened_cards.append(sharpened)

    return sharpened_cards
        

def get_card_value(card_list: list) -> list:
    card_values = []
    for card in card_list:
        height, width = card.shape[:2]

        # Crop image to northwest corner
        x = int(width * 0.05)
        y = int(height * 0.05)
        crop_width = int(width * 0.165)
        crop_height = int(height * 0.19)
        card = card[y:y+crop_height, x:x+crop_width]

        # Resize card so value is larger in frame
        card = cv2.resize(card, (width, height))

        if log:
            cv2.imshow('Crop to Corner', card)
            cv2.namedWindow('Crop to Corner', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Crop to Corner', 700, 700)
            cv2.waitKey(0)

        card_values.append(card)
    
    return card_values

def ocr(card_images: list) -> list:
    adjustments = 0

    # Run OCR on each card
    card_texts = []
    reader = easyocr.Reader(['en'])
    for card_image in card_images:
        
        # Otsu's thresholding to convert image to binary
        card_image = cv2.GaussianBlur(card_image, (7, 7), 0)
        _,card_image = cv2.threshold(card_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Morphological operations to "sharpen" the card values and remove noise
        card_image = cv2.morphologyEx(card_image, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
        card_image = cv2.erode(card_image, np.ones((3, 3), np.uint8), iterations=1)

        if log:
            cv2.imshow('OCR Input', card_image)
            cv2.namedWindow('OCR Input', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('OCR Input', 700, 700)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        text = reader.readtext(card_image, detail=0)
        if text:
            if text == "0":
                text = "Q"
                adjustments += 1
            if text == "1":
                text = "7"
                adjustments += 1
            card_texts.append(text[0])

        
    return card_texts, adjustments


if __name__ == "__main__":
    [dealer, player] = play("1_1")
    print(f"Dealer: {dealer}")
    print(f"Player: {player}")