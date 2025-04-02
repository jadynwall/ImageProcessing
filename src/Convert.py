"""
Convert output from get_move() from card values to corresponding integer values. 
"""

def convert_hand(hand_list):

    int_hand = []

    # convert all elements in list to corresponding integer value 
    for i in range(len(hand_list)):
        if hand_list[i] == 'J' or hand_list[i] == 'Q' or hand_list[i] == 'K':
            int_hand.append(10)
        elif hand_list[i] == 'A':
            int_hand.append(1)
        else:
            int_hand.append(int(hand_list[i]))
    
    # loop through hand to find any cases where card was an ace (to determine if treating as 1 or 11)
    for j in range(len(int_hand)):
        if int_hand[j] == 1:
            if sum(int_hand) > 11:
                int_hand[j] = 1
            else:
                int_hand[j] = 11

    return int_hand