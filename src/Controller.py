"""
System controller for the blackjack game. This module is responsible for
managing the game state and the player's actions.
"""

def get_move(player_hand, dealer_upcard):

    player_sum = sum(player_hand)

    if dealer_upcard == 1:
        dealer_sum = 11
    else:
        dealer_sum = dealer_upcard

    if len(player_hand) == 2 and len(set(player_hand)) == 1:
        # Pairs
        if player_sum == 20:
            return 'stand'

        elif player_sum == 18 and (dealer_sum == 7 or dealer_sum >= 10):
            return 'stand'

        elif player_sum == 10 and dealer_sum <= 9:
            return 'double'

        elif player_sum <=14 and dealer_sum >= 8:
            return 'hit'

        elif player_sum == 12 and dealer_sum == 7:
            return 'hit'

        elif player_sum == 8 and (dealer_sum <= 4 or dealer_sum == 7):
            return 'hit'

        else:
            return 'split'
    

    elif 1 in player_hand and player_sum + 10 <= 21:
        # Soft hand
        player_sum += 10

        if player_sum == 20:
            return 'stand'

        elif player_sum == 19:
            if dealer_sum == 6:
                return 'double' if len(player_hand) == 2 else 'hit'
            else:
                return 'stand'
        
        elif player_sum == 18:
            if dealer_sum <= 6:
                return 'double' if len(player_hand) == 2 else 'hit'
            elif dealer_sum == 7 or dealer_sum == 8:
                return 'stand'
            else:
                return 'hit'

        elif dealer_sum == 5 or dealer_sum == 6:
            return 'double' if len(player_hand) == 2 else 'hit'
        
        elif player_sum == 17 and dealer_sum == 3:
            return 'double' if len(player_hand) == 2 else 'hit'
        
        elif player_sum >= 15 and dealer_sum == 4:
            return 'double' if len(player_hand) == 2 else 'hit'
            
        else:
            return 'hit'
        
    else:
        # Hard hand
        if player_sum >= 17:
            return 'stand'

        elif player_sum >= 13 and dealer_sum <= 6:
            return 'stand'

        elif player_sum == 12 and dealer_sum >= 4 and dealer_sum <= 6:
            return 'stand'

        elif player_sum == 11:
            return 'double' if len(player_hand) == 2 else 'hit'

        elif player_sum == 10 and dealer_sum <= 9:
            return 'double' if len(player_hand) == 2 else 'hit'
        
        elif player_sum == 9 and dealer_sum <= 6 and dealer_sum >= 3:
            return 'double' if len(player_hand) == 2 else 'hit'

        else:
            return 'hit'


if __name__ == '__main__':
    print('Testing')