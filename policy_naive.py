from gameplay import *

'''
In a given turn, this policy just rolls once and picks up every die it can
'''
def always_roll_once(choices,total_score,turn_score,is_open):
    return {
        "choice": max(choices, key=lambda choice: choice["score"]),
        "roll_again": False
    }

if __name__ == "__main__":
    play_single_player_game(always_roll_once, verbose=True)