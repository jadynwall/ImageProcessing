"""
Vision module for blackjack game. This module is responsible for extracting
the game state from the screen and converting it into a format that the
controller can understand.
"""
import numpy as np
import cv2
import easyocr


def play(image_name: str):
    # get file path of the image from user input
    img = cv2.imread(f"images/{image_name}.jpg")

    # convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = gray

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

    # Sharpen the images
    dealer_sharpened = sharp(dealer_cards)
    player_sharpened = sharp(player_cards)

    # Crop and get card values
    # dealer_values = get_card_value(dealer_cards)
    # player_values = get_card_value(player_cards)
    dealer_values = get_card_value(dealer_sharpened)
    player_values = get_card_value(player_sharpened)

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
    # for i, contour in enumerate(card_contours):
    #     # Get bounding box for each card
    #     x, y, w, h = cv2.boundingRect(contour)
        
    #     # Extract the card from the original image
    #     card_image = imgs[y:y+h, x:x+w]
    #     card_images.append(card_image)

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
        card_images.append(card_image)
    
    return card_images

def sharp(card_list: list) -> list:
    sharpened_cards = []
    for card in card_list:
        gaussian_blur = cv2.GaussianBlur(card, (7, 7), sigmaX=2)

        sharpened = cv2.addWeighted(card, 3.5, gaussian_blur, -2.5, 0)

        sharpened_cards.append(sharpened)

    return sharpened_cards
        

def get_card_value(card_list: list) -> list:
    card_values = []
    for card in card_list:
        height, width = card.shape[:2]

        # crop image to northwest corner
        x = int(width * 0.05)
        y = int(height * 0.05)
        crop_width = int(width * 0.165)
        crop_height = int(height * 0.19)
        card = card[y:y+crop_height, x:x+crop_width]

        # resize card
        card = cv2.resize(card, (width, height))
        card_values.append(card)
    
    return card_values

def ocr(card_images: list) -> list:
    # Run OCR on each card
    card_texts = []
    reader = easyocr.Reader(['en'])
    for card_image in card_images:
        # Otsu's thresholding
        card_image = cv2.GaussianBlur(card_image, (7, 7), 0)
        _,card_image = cv2.threshold(card_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        card_image = cv2.morphologyEx(card_image, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
        card_image = cv2.erode(card_image, np.ones((3, 3), np.uint8), iterations=1)
        cv2.imshow('Card', card_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        text = reader.readtext(card_image, detail=0)
        if text:
            print(text)
            card_texts.append(text[0])


    return card_texts


def main():
    # Test

    # Complete Image Set
    #test_images = ["0_1", "1_1","1_2", "1_3", "2_1", "2_2", "3_1", "3_2", "3_3", "4_1", "4_2", "5_1", "5_2", "6_1", "6_2", "7_1", "7_2", "8_1", "8_2", "8_3", "8_4", "9_1", "9_2", "9_3", "9_4", "10_1", "10_2"]
    
    # Incorrect Answer Set
    test_images = ["7_1", "7_2"]
    for image in test_images:
        print(f"Image: {image}")
        [dealer, player] = play(image)
        print("Dealer cards:", dealer)
        print("Player cards:", player)
        print("\n")

if __name__ == "__main__":
    main()