from random import randint
from farkle import *


'''
Plays thru a game of farkle using some policy.
`policy` is any function that takes these arguments:
    `choices` - a list of choices (which are dicts that looks like {"score": <int>, "remaining": <int>})
    `total_score` - the total score of the game so far NOT including the current turn
    `turn_score` - the score of the current turn so far, not including the newly thrown dice
    `is_open` - True if the player has opened with dice selected so far (not including thrown dice not yet picked up)
and returns a dict like this:
    {
        "choice": <the choice dict they choose>,
        "roll_again": <whether the player chooses to roll again>
    }
policy can make roll_again false even if player is not open as the game will force them to roll again anyways


This function returns a thing like this:
{
    "total_score": <int> # the total score after the game ends
    "scores": <list<int>> # a list of scores from each turn (including 0 for farkles)
    "turns": <int> # the number of turns
}
'''
def play_single_player_game(policy, verbose=False):
    scores = [] # scores of each turn
    total_score = 0 # == sum(scores)
    turn_count = 0
    is_open = False
    while total_score < 5000:
        turn_count += 1
        turn_score = 0
        # Lets play a turn
        # FIRST THROW in turn
        dice = [randint(1,6) for i in range(6)]
        if verbose: print("----------------------------------------")
        if verbose: print(f"Turn {turn_count}, Score {total_score}")
        if verbose: print(f"Player rolled {dice}")
        choices = return_all_choices(dice)
        farkled = len(choices) == 0
        is_open = is_open or turn_score >= 500
        if not farkled:
            player_decision = policy(
                    choices=choices,
                    total_score=total_score,
                    turn_score=turn_score,
                    is_open=is_open
                )
            player_choice = player_decision["choice"]
            roll_again = player_decision["roll_again"]
            turn_score += player_choice["score"]
            is_open = is_open or turn_score >= 500
            if verbose:
                player_choice_score = player_choice["score"]
                player_choice_remaining = player_choice["remaining"]
                print(f"Player claims {player_choice_score} points with {player_choice_remaining} dice remaining")
            while (not farkled) and ((not is_open) or roll_again):
                # SUBSEQUENT THROWS in turn
                new_count = player_choice["remaining"]
                new_count = new_count if new_count > 0 else 6 # Re-roll all dice if run out
                dice = [randint(1,6) for i in range(new_count)]
                if verbose: print(f"Player rolled {dice}")
                choices = return_all_choices(dice)
                farkled = len(choices) == 0
                if not farkled:
                    player_decision = policy(
                            choices=choices,
                            total_score=total_score,
                            turn_score=turn_score,
                            is_open=is_open
                        )
                    player_choice = player_decision["choice"]
                    roll_again = player_decision["roll_again"]
                    turn_score += player_choice["score"]
                    is_open = is_open or turn_score >= 500
                    if verbose:
                        player_choice_score = player_choice["score"]
                        player_choice_remaining = player_choice["remaining"]
                        print(f"Player claims {player_choice_score} points with {player_choice_remaining} dice remaining")
        if farkled:
            turn_score = 0
        if verbose: print(f"Turn has ended. {turn_score} points earned in turn.")
        scores.append(turn_score)
        total_score += turn_score
    if verbose: print("----------------------------------------")
    if verbose: print(f"GAME OVER. Score: {total_score}")
    result = {
        "total_score": total_score,
        "scores": scores,
        "turns": turn_count
    }
    if verbose: print(result)



if __name__ == "__main__":
    print(is_farkle([2,3]))