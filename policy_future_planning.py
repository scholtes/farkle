from gameplay import *

'''
In a given turn, this policy :
    * Rolls if there are at least n dice remaining to roll (try using n=3, earlier determined to be best)
    * Picks up every die it can on each throw
    * Stops when it gets to 5000
    * If picking up all valid dice yield k or more dice remaining, only pick up 1 die if score
      less than 250 (no 3 of kinds except for 2s) (for k=5,4,3 only)
    * _115 -> if you roll 6 dice and only have 1, 1, 5 to choose, pick up both 1s but leave the 5
    * _155 -> if you roll 6 dice and only have 1, 5, 5 to choose, pick up a 1 and a 5, but leave the other 5
'''
def leave_out_some_dice(n,k,_115=False,_155=False):
    # The play_single_player_game function won't pass in n to our policy so we just
    # have this outer function return a function that play_single_player_game can use.
    def inner_policy(choices,total_score,turn_score,is_open):
        greediest_choice = max(choices, key=lambda choice: choice["score"])
        choice = None
        if greediest_choice["score"] > 250 or greediest_choice["remaining"] < k:
            choice = greediest_choice
        elif greediest_choice["remaining"] >= k:
            if any(choice["score"] == 50 for choice in choices):
                choice = list(filter(lambda choice: choice["score"] == 50, choices))[0]
            elif any(choice["score"] == 100 for choice in choices):
                choice = list(filter(lambda choice: choice["score"] == 100, choices))[0]
            else:
                choice = greediest_choice
        else:
            choice = greediest_choice
        ##### options where you pick 2 things
        if _155:
            is_115 = any(choice["score"] == 100 and choice["remaining"]==5 for choice in choices) and\
                any(choice["score"] == 200 and choice["remaining"]==4 for choice in choices) and\
                any(choice["score"] == 250 and choice["remaining"]==3 for choice in choices)
            is_155 = any(choice["score"] == 100 and choice["remaining"]==5 for choice in choices) and\
                any(choice["score"] == 150 and choice["remaining"]==4 for choice in choices) and\
                any(choice["score"] == 200 and choice["remaining"]==3 for choice in choices)
            if is_155 or is_115:
                choice = list(filter(lambda choice: choice["remaining"]==4, choices))[0]
        elif _115:
            is_115 = any(choice["score"] == 100 and choice["remaining"]==5 for choice in choices) and\
                any(choice["score"] == 200 and choice["remaining"]==4 for choice in choices) and\
                any(choice["score"] == 250 and choice["remaining"]==3 for choice in choices)
            if is_115:
                choice = list(filter(lambda choice: choice["remaining"]==4, choices))[0]
        #####
        roll_again = choice["remaining"] >= n and (choice["score"]+total_score+turn_score < 5000)
        return {
            "choice": choice,
            "roll_again": roll_again
        }
    return inner_policy


if __name__ == "__main__":
    
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Playing a single game n=3 k=5...")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    play_single_player_game(leave_out_some_dice(n=3,k=5), verbose=True)

    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    for k in [5,4,3]:
        print(f"Playing 50,000 games n=3 k={k}...")
        analyze_n_single_player_games(n=50000, policy=leave_out_some_dice(n=3,k=k),
                printStats=True,
                verboseStats=False,
                verboseProgress=True,
                verboseGames=False)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    print("================================")
    print(f"Playing 50,000 games n=3 k=3... but also grab 1,1 from 1,1,5")
    analyze_n_single_player_games(n=50000, policy=leave_out_some_dice(n=3,k=3,_115=True,_155=False),
            printStats=True,
            verboseStats=False,
            verboseProgress=True,
            verboseGames=False)
    print(f"Playing 50,000 games n=3 k=3... but also grab 1,5 from 1,5,5")
    analyze_n_single_player_games(n=50000, policy=leave_out_some_dice(n=3,k=3,_115=False,_155=True),
            printStats=True,
            verboseStats=False,
            verboseProgress=True,
            verboseGames=False)
    print("================================")