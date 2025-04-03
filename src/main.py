"""
Main function running the overall game. 
"""

import time
from Controller import get_move 
from Convert import convert_hand
from Eyes import play

def main():

    again = 'y'

    while again == 'y' or again == 'Y': 

        print("\nWelcome to Backjack Strategist! We will give you the BEST odds to maximize your hard-earned dollars!\n")

        next_move = 'start'
        split = 0

        while True:

            if split == 0:
                # get file path of the image from user input
                print("Take a picture of your updated hand and the dealer's card (from your perspective)")
                file_path = input("Enter the name of this image (without extension): ")
            elif split == 1:
                print("Take a picture of your first hand you are playing (post-split)")
                file_path = input("Enter the name of this image (without extension): ")
            else:
                print("Take a picture of your second hand you are playing (post-split)")
                file_path = input("Enter the name of this image (without extension): ")

            try:
                # pass image into processing function 
                [dealer_card, player_cards] = play(file_path)

            except:
                print("invalid image name - try again")

            else:
                print("player cards: ", player_cards) # TESTING 
                print("dealer card: ", dealer_card) # TESTING
                player_cards = convert_hand(player_cards) # convert player hand to lists of integer values
                dealer_card = convert_hand(dealer_card) # convert dealer hand to lists of integer values
                print("player sum: ", sum(player_cards)) # TESTING 
                print("dealer sum: ", dealer_card[0]) # TESTING

                next_move = get_move(player_cards, dealer_card[0])
                print("Next move:", next_move)
                time.sleep(2)

                # if the next move is to stand, then no more moves to make
                # if next move is to double, this is the last move player allowed to make  
                if (next_move == 'stand' or next_move == 'double') and split == 1:
                    split = 2
                    split_save_player = player_cards
                    split_save_next_move = next_move
                elif (next_move == 'stand' or next_move == 'double') and split == 2:
                    split_save_player2 = player_cards
                    split_save_next_move2 = next_move
                    break
                elif next_move == 'stand' or next_move == 'double':
                    break
                elif next_move == 'split':
                    split = 1
        
        if split == 0:
            if sum(player_cards) > 21 and next_move == 'double':
                print("You busted - You lost (double)!")
            elif sum(player_cards) > 21:
                print("You busted - You lost!")
            else:
                # get file path of the image from user input
                print("Take a picture of the final results (from your perspective)")
                file_path = input("Enter the name of this image (without extension): ")

                # pass image into processing function 
                [dealer_cards, player_cards] = play(file_path)
                player_cards = convert_hand(player_cards) # convert player hand to lists of integer values
                dealer_cards = convert_hand(dealer_cards) # convert dealer hand to lists of integer values
                print("player cards: ", player_cards) # TESTING 
                print("dealer card: ", dealer_cards) # TESTING

                if sum(dealer_cards) > 21 and next_move == 'double':
                    print("Dealer busted - You won (DOUBLE)!")
                elif sum(dealer_cards) > 21:
                    print("Dealer busted - You won!")
                else:
                    if sum(player_cards) > sum(dealer_cards) and next_move == 'double':
                        print("You won (DOUBLE)!")
                    elif sum(player_cards) > sum(dealer_cards):
                        print("You won!")
                    elif sum(player_cards) == sum(dealer_cards):
                        print("You pushed (money back)!")
                    elif sum(player_cards) < sum(dealer_cards) and next_move == 'double':
                        print("You lost (double)!")
                    else:
                        print("You lost!")
        else: # split hand 
            for i in range(2):
                if i == 0:
                    if sum(split_save_player) > 21 and split_save_next_move == 'double':
                        print("Your first hand busted - You lost (double)!")
                    elif sum(split_save_player) > 21:
                        print("Your first hand busted - You lost!")
                    else:
                        # get file path of the image from user input
                        print("Take a picture of the final results (from your perspective) of the first hand")
                        file_path = input("Enter the name of this image (without extension): ")

                        # pass image into processing function 
                        [dealer_cards, player_cards] = play(file_path)
                        player_cards = convert_hand(player_cards) # convert player hand to lists of integer values
                        dealer_cards = convert_hand(dealer_cards) # convert dealer hand to lists of integer values
                        print("player cards: ", player_cards) # TESTING 
                        print("dealer card: ", dealer_cards) # TESTING

                        if sum(dealer_cards) > 21 and next_move == 'double':
                            print("Dealer busted on your first hand - You won (DOUBLE)!")
                        elif sum(dealer_cards) > 21:
                            print("Dealer busted on your first hand - You won!")
                        else:
                            if sum(player_cards) > sum(dealer_cards) and next_move == 'double':
                                print("You won on your first hand (DOUBLE)!")
                            elif sum(player_cards) > sum(dealer_cards):
                                print("You won on your first hand!")
                            elif sum(player_cards) == sum(dealer_cards):
                                print("You pushed on your first hand (money back)!")
                            elif sum(player_cards) < sum(dealer_cards) and next_move == 'double':
                                print("You lost on your first hand (double)!")
                            else:
                                print("You lost on your first hand!")
                else: # second hand 
                    if sum(split_save_player2) > 21 and split_save_next_move2 == 'double':
                        print("Your second hand busted - You lost (double)!")
                    elif sum(split_save_player2) > 21:
                        print("Your second hand busted - You lost!")
                    else:
                        # get file path of the image from user input
                        print("Take a picture of the final results (from your perspective) of the second hand")
                        file_path = input("Enter the name of this image (without extension): ")

                        # pass image into processing function 
                        [dealer_cards, player_cards] = play(file_path)
                        player_cards = convert_hand(player_cards) # convert player hand to lists of integer values
                        dealer_cards = convert_hand(dealer_cards) # convert dealer hand to lists of integer values
                        print("player cards: ", player_cards) # TESTING 
                        print("dealer card: ", dealer_cards) # TESTING

                        if sum(dealer_cards) > 21 and next_move == 'double':
                            print("Dealer busted on your second hand - You won (DOUBLE)!")
                        elif sum(dealer_cards) > 21:
                            print("Dealer busted on your second hand - You won!")
                        else:
                            if sum(player_cards) > sum(dealer_cards) and next_move == 'double':
                                print("You won on your second hand (DOUBLE)!")
                            elif sum(player_cards) > sum(dealer_cards):
                                print("You won on your second hand!")
                            elif sum(player_cards) == sum(dealer_cards):
                                print("You pushed on your second hand (money back)!")
                            elif sum(player_cards) < sum(dealer_cards) and next_move == 'double':
                                print("You lost on your second hand (double)!")
                            else:
                                print("You lost on your second hand!")

            time.sleep(2)


        print("\nThanks for playing!\n")
        
        again = input("Play another hand? Press y to play again, or any other key to exit ")


if __name__ == '__main__':
    main()