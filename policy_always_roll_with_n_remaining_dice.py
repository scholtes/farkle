from gameplay import *

'''
In a given turn, this policy :
    * Rolls if there are at least n dice remaining to roll
    * Picks up every die it can on each throw
    * Stops when it gets to 5000
'''
def always_roll_with_n_remaining_dice(n):
    # The play_single_player_game function won't pass in n to our policy so we just
    # have this outer function return a function that play_single_player_game can use.
    def inner_policy(choices,total_score,turn_score,is_open):
        choice = max(choices, key=lambda choice: choice["score"])
        roll_again = choice["remaining"] >= n and (choice["score"]+total_score+turn_score < 5000)
        return {
            "choice": choice,
            "roll_again": roll_again
        }
    return inner_policy


if __name__ == "__main__":

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Playing a single game with n=4...")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    play_single_player_game(always_roll_with_n_remaining_dice(4), verbose=True)

    print("")
    print("")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("Playing 50,000 games for each n 2 thru 6...")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("")

    for dice_limit in [2,3,4,5,6]:
        print(f"")
        print(f"Policy: roll again when {dice_limit} or more dice available:")
        the_policy = always_roll_with_n_remaining_dice(dice_limit)
        analyze_n_single_player_games(n=50000, policy=the_policy,
            printStats=True,
            verboseStats=False,
            verboseProgress=True,
            verboseGames=False)

    print("")
    print("")
    print("=========================================")
    print("n=3 and n=4 are very close, let's compare")
    print("  Policy 1 (roll with 3 or more)")
    print("  Policy 2 (roll with 4 or more)")
    print("Playing 1,000,000 games each...")
    print("=========================================")
    print("")

    # 3 wins by 1%
    compare_policies(1000000, always_roll_with_n_remaining_dice(3), always_roll_with_n_remaining_dice(4))
