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

    print(">>>>>>>>>>>>>>>>>>>>>>>>")
    print("Playing a single game...")
    print(">>>>>>>>>>>>>>>>>>>>>>>>")

    play_single_player_game(always_roll_once, verbose=True)

    print("<<<<<<<<<<<<<<<<<<<<<<<<")
    print("Playing 10,000 games...")
    print("<<<<<<<<<<<<<<<<<<<<<<<<")

    analyze_n_single_player_games(n=10000, policy=always_roll_once)