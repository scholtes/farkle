# Farkle simulator

`farkle.py` is a script that lets us statistically compare different play strategies so that we can cream our family.

# Files

 * `farkle.py` - contains a bunch of utility functions for doing farkle math on lists of dice
 * `gameplay.py` - contains a game simulator and some statistics functions
 * `policy_*.py` - contains a policy definition. Try out `python policy_naive.py` for a sample

# How to write a policy

Give your policy a cool name, like "awesome policy" and save it with the naming convention `policy_*.py`, so in your case `policy_awesome.py`. Have it contain a function using the properties defined below, in our example we'll call it `my_awesome_policy`.

Your policy should be a function that takes these arguments:

 - `choices` - a `list` of choices (explanation below)
 - `total_score` - the total score of the game so far, not including points from dice picked up in the current turn
 - `turn_score` - the score of the current turn so far, not including any newly thrown dice which have not yet been picked up
 - `is_open` - `True` if the player needs to choose more dice to open, otherwise `False`

Example signature: `def my_awesome_policy(choices, total_score, turn_score, is_open):`

A `choice` is a `dict` that looks like this (for example):

```python
{
    "score": 300,
    "remaining": 2
}

```

This means that the player will pick up some number of dice, leave `2` dice ready to be re-rolled, and gain `300` points.

For example, if the player rolled `[5, 2, 2, 2, 1, 4]`, the `choices` object would look like this:

```python
[
    {"score": 350, "remaining": 1},
    {"score": 300, "remaining": 2},
    {"score": 200, "remaining": 3},
    {"score": 150, "remaining": 4},
    {"score": 100, "remaining": 5}
]

```

To communicate with the simulator what the player intends to do next, the policy function should return one of these choices and a decision as to whether to continue to roll again.  The return value may look something like the following example:

```python
{
    "choice": {"score": 300, "remaining": 2},
    "roll_again": False
}

```

Using the same `choices` example from above, this would mean the player decided to pick up the 1 and a 3-of-a-kind, scoring `300` points and leaving the 4 and the 5 on the table. This player has elected to not roll the remaining 2 dice (if the player is not yet open the game simulator will override the policy's decision).

# How to test your policy:

Call the `play_single_player_game` function from `gameplay.py`. Set `verbose=True` to see gameplay output:

```python
play_single_player_game(my_awesome_policy_function, verbose=True)
```

Call the `analyze_n_single_player_games` function to run multiple games and generate statistics. For example, to run 10,000 trials:

```python
analyze_n_single_player_games(n=10000, policy=always_roll_once)
```

# Run an example!

Run 

```
python policy_naive.py
```

to see the output from a game using a basic policy, and some statistics about how this policy performs.