from gameplay import *

'''
In a given turn, this policy :
    * Rolls if there are less than n points scored in turn
    * Picks up every die it can on each throw
    * Stops when it gets to 5000
'''
def roll_until_n_points(n):
    def inner_policy(choices,total_score,turn_score,is_open):
        choice = max(choices, key=lambda choice: choice["score"])
        roll_again = choice["score"] < n and (choice["score"]+total_score+turn_score < 5000)
        return {
            "choice": choice,
            "roll_again": roll_again
        }
    return inner_policy


if __name__ == "__main__":

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Playing a single game with n=400...")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    play_single_player_game(roll_until_n_points(400), verbose=True)

    print("")
    print("")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("Playing 100,000 games for each n 50 thru 1000...")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("")

    for score_limit in [50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000]:
        print(f"")
        print(f"----------------------------------------------------------")
        print(f"Policy: roll again until {score_limit} points are reached:")
        the_policy = roll_until_n_points(score_limit)
        analyze_n_single_player_games(n=100000, policy=the_policy,
            printStats=True,
            verboseStats=False,
            verboseProgress=True,
            verboseGames=False)