from collections import defaultdict
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
    return result


'''
Runs multiple games and gives statistics.
    `n` - number of games to play
    `policy` - the policy function (see `play_single_player_game` for explanation and `policy_naive.py` for an example)
    `printStats` - print statistic results (mean and standard deviations for turns per game and score per turn for the policy)
    `verboseStats` - print more verbose statistics (contains histograms)
    `verboseProgress` - prints a period (".") every time 1,000 games have completed being simulated.
    `verboseGames` - prints the verbose output of every game simulated (warning: VERY verbose for large n)
On my machine, n=10,000 games takes about 5 seconds to complete for the demo naive policy.

The return value of this function is what `verboseStats` prints out, which looks something like this example:

```
{
    "games": [
        {"turns": 15, "games": 1040}, # I.e. 1,040 of the total simulated games took 15 turns to complete
        ...
    ],
    "turns": [
        {"score": 750, "turns": 1605}, # I.e. 1,605 of the total simulated turns ended with a score of 750
        ...
    ],
    "totalTurns": 159373,
    "totalGames": 10000,
    "meanTurnsPerGame":  15.9373,
    "stdvTurnsPerGame":   3.7843,
    "meanScorePerTurn": 331.3830,
    "stdvScorePerTurn": 322.6619
}
```
'''
def analyze_n_single_player_games(n, policy, printStats=True, verboseStats=True, verboseProgress=True, verboseGames=False):
    turns_hist = defaultdict(int)
    games_hist = defaultdict(int)
    progress = 0
    for i in range(n):
        if progress % 1000 == 0:
            if verboseProgress: print(".",end="",flush=True) # Print status marker every 1000 games
        trial = play_single_player_game(policy, verboseGames)
        games_hist[trial["turns"]] += 1
        for score in trial["scores"]:
            turns_hist[score] += 1
        progress += 1
    if verboseProgress: print()
    turns_per_game = sorted([{"turns": k, "games": v} for k,v in games_hist.items()], key=lambda bucket: bucket["turns"])
    score_per_turn = sorted([{"score": k, "turns": v} for k,v in turns_hist.items()], key=lambda bucket: bucket["score"])
    turns_count = sum(bucket["turns"]*bucket["games"] for bucket in turns_per_game)
    games_count = n
    mean_turns_per_game = sum(bucket["games"]*bucket["turns"] for bucket in turns_per_game)/games_count
    mean_score_per_turn = sum(bucket["turns"]*bucket["score"] for bucket in score_per_turn)/turns_count
    stdv_turns_per_game = (sum(bucket["games"]*(bucket["turns"]-mean_turns_per_game)**2 for bucket in turns_per_game)/games_count)**0.5
    stdv_score_per_turn = (sum(bucket["turns"]*(bucket["score"]-mean_score_per_turn)**2 for bucket in score_per_turn)/turns_count)**0.5
    result = {
        "games": turns_per_game,
        "turns": score_per_turn,
        "totalTurns": turns_count,
        "totalGames": games_count,
        "meanTurnsPerGame": mean_turns_per_game,
        "stdvTurnsPerGame": stdv_turns_per_game,
        "meanScorePerTurn": mean_score_per_turn,
        "stdvScorePerTurn": stdv_score_per_turn
    }
    if verboseStats: print(result)
    if printStats: print(f"Turns per game: {mean_turns_per_game:.4f} (\u00b1{stdv_turns_per_game:.4f})")
    if printStats: print(f"Score per turn: {mean_score_per_turn:.4f} (\u00b1{stdv_score_per_turn:.4f})")
    return result



if __name__ == "__main__":
    print(is_farkle([2,3]))