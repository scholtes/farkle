'''
Naming conventions and asumptionsin this file:
 * `dice` is a list of ints of throw results in a hand. For example, if you throw 4 dice
   and rolled a 1, 3, 1, and 5, `dice` would be `[1,3,1,5]` (never assumed to be sorted)
 * Valid dice values are only 1 thru 6 (six sided)
 * There are at most 6 dice
 * `dices` is a list of `dice` (list of lists of ints)
 * Rules of farkle only include these ways to score:
   1, 5, 3 of a kind, or 1 thru 6 straight
    * 1s are worth 100
    * 5s are worth 50
    * 3s of a kind of n are worth 100*n, except n=1 is worth 1000
    * 1 thru 6 is worth 1500
'''


##################################################################################################

'''
Returns all numbers that have a 3 of a kind in the hand.
Example inputs and outputs:
    get_all_3_of_kinds([1,2,1,3]) # => []
    get_all_3_of_kinds([2,4,2,2,3]) # => [2]
    get_all_3_of_kinds([1,1,1,2,2,2]) # => [1,2]
    get_all_3_of_kinds([3,3,3,3,3,3]) # => [3]
'''
def get_all_3_of_kinds(dice):
    kinds = []
    for i in [1,2,3,4,5,6]:
        if dice.count(i) >=3:
            kinds.append(i)
    return kinds

'''
For a given set of dice, removes the 3 of the kind for dice value n.
Example inputs and outputs:
    remove_3_of_kind([3,2,3,2,2,1], 2) # => [3,3,1]
    remove_3_of_kind([1,1,1,3,3,3], 3) # => [1,1,1]
    remove_3_of_kind([6,6,6], 6) # => []
    remove_3_of_kind([4,4,4,4,4]) # => [4,4]
Assumes the specified 3 of a kind is present.
'''
def remove_3_of_kind(dice, n):
    pruned = [i for i in dice]
    pruned.remove(n)
    pruned.remove(n)
    pruned.remove(n)
    return pruned

'''
Returns score of 3 of kinds for given dice value n
'''
def score_3_of_kind(n):
    if n == 1:
        return 1000
    else:
        return 100*n



'''
Given a list of dice, returns all possible choices the player
has to score for that throw (not the entire hand). Each choice depends
on which dice the player picks up. 

Returns a list of dictionaries, with these keys:
    * "score" - (int) how many new points they would get from this choice
    * "remaining" - (int) a count of how many dice are remaining after removing the scoring ones

Note that no information about which dice were picked up and which rules were invoked are
returned as that information does not affect future throws.
Only the choices with the highest score for a given number of remaining die are included.

Example inputs and outputs:
    return_all_choices([5,2,2,2,1,4])
    # => [
    #   {"score": 350, "remaining": 1}, # Player picks up 1, 5, 3-of-kind
    #   {"score": 300, "remaining": 2}, # Player picks up 1, 3-of-kind
    #   {"score": 200, "remaining": 3}, # Player picks up 3-of-kind
    #   {"score": 150, "remaining": 4}, # Player picks up 1, 5
    #   {"score": 100, "remaining": 5}, # Player picks up 1
    # ]
Note that in the example, the player may choose to pick scores other than the highest (350)
in order to increase the remaining dice count, but is forbidden from picking up the 5 without
picking up the 1 as the player could simply pick up the 1 instead and still have the same
count of dice in the next throw. I.e., these results are ommited:
    #   {"score": 250, "remaining": 2} # Player picks up 5, 3-of-kind
    #   {"score":  50, "remaining": 5} # Player picks up 5
'''
def return_all_choices(dice):
    return _max_score_only(_rac(dice))

'''
recursion helper function for return_all_choices. Does the same thing it does except
without a check at the end to make sure there is only one choice for any given
"remaining" count.
'''
def _rac(dice):
    if not dice:
        return []
    if has_1_thru_6(dice):
        return [{"score": 1500, "remaining": 0}]
    choices = []
    if 1 in dice:
        choices.append({"score": 100, "remaining": len(dice)-1})
        new_dice = [i for i in dice]
        new_dice.remove(1)
        choices.extend([{
                "score": 100+choice["score"],
                "remaining": choice["remaining"]}
            for choice in _rac(new_dice)])
    if 5 in dice:
        choices.append({"score": 50, "remaining": len(dice)-1})
        new_dice = [i for i in dice]
        new_dice.remove(5)
        choices.extend([{
                "score": 50+choice["score"],
                "remaining": choice["remaining"]}
            for choice in _rac(new_dice)])
    for kind in get_all_3_of_kinds(dice):
        score = score_3_of_kind(kind)
        choices.append({"score": score, "remaining": len(dice)-3})
        new_dice = remove_3_of_kind(dice, kind)
        choices.extend([{
                "score": score+choice["score"],
                "remaining": choice["remaining"]}
            for choice in _rac(new_dice)])
    return choices


'''
Given a list of dicts of scores and remaining, returns only those dicts for which
`score` is max for a given `remaining` value.
'''
def _max_score_only(rac_result):
    pruned_result = []
    for i in [0,1,2,3,4,5]:
        choices = [choice for choice in rac_result if choice["remaining"] == i]
        if choices:
            pruned_result.append(max(choices, key=lambda x: x["score"]))
    return pruned_result

##################################################################################################

'''
Example inputs and outputs:
    is_farkle([1,2,4,1,6]) # => False
    is_farkle([2,2,3,6,2]) # => False
    is_farkle([2,6,6,3,4,4]) # => True
    is_farkle([4]) # => True
'''
def is_farkle(dice):
    return not (
            1 in dice
            or 5 in dice
            or has_3_of_kind(dice)
            or has_1_thru_6(dice)
        )



'''
Example inputs and outputs:
    has_3_of_kind([1,2,4,1,6]) # => False
    has_3_of_kind([2,2,3,6,2]) # => True
    has_3_of_kind([2,6,6,3,4,4]) # => False
    has_3_of_kind([4]) # => False
'''
def has_3_of_kind(dice):
    for i in [1,2,3,4,5,6]:
        if dice.count(i) >=3:
            return True
    return False



'''
Returns True only if all ints 1 thru 6 are in the dice set
exactly once (assumes max of 6 dice):

Example inputs and outputs:
    has_1_thru_6([2,5,4,1,6,3]) # => True
    has_1_thru_6([1,2,3,4,5,6]) # => True
    has_1_thru_6([1,1,3,4,5,6]) # => False
    has_1_thru_6([2,3,2]) # => False
'''
def has_1_thru_6(dice):
    return len(list(set(dice))) == 6



'''
Lists all possible roles of dice for n dice. Returns list of lists of ints
Order of dice matters, e.g., get_all_dice_len_n(3) includes [1,2,1] and [1,1,2] distinctly
Example inputs and outputs:
    get_all_dices_len_n(3)
        # => 
        # [[1,1,1],
        #  [1,1,2],
        #  [1,1,3],
        # ... 211 more ...
        #  [6,6,5], 
        #  [6,6,6]]
Returns 6**n lists each of length n
'''
def get_all_dices_len_n(n):
    if n == 1:
        return [[1], [2], [3], [4], [5], [6]]
    less_dices = get_all_dices_len_n(n-1)
    dices = []
    for i in [1,2,3,4,5,6]:
        for less_dice in less_dices:
            dices.append([i] + less_dice)
    return dices



'''
Given a list of roles, counts how many are farkles.
Example inputs and outputs:
    get_farkle_count([[1,2,4,1,6]
        [2,2,3,6,2]
        [2,6,6,3,4,4]
        [4]])
    # => 2
'''
def get_farkle_count(dices):
    count = 0
    for dice in dices:
        if is_farkle(dice):
            count += 1
    return count

##################################################################################################
######################################### main functions #########################################
##################################################################################################
'''
Prints out the probability of a farkle for each number of dice. Output (with extra formatting):
------------------------------------------------------------
For 1 dice probability of farkle is 4/6             66.666 %
For 2 dice probability of farkle is 16/36           44.444 %
For 3 dice probability of farkle is 60/216          27.777 %
For 4 dice probability of farkle is 204/1296        15.740 %
For 5 dice probability of farkle is 600/7776         7.716 %
For 6 dice probability of farkle is 1440/46656       3.086 %
------------------------------------------------------------
'''
def do_all_farkle_counts():
    for i in [1,2,3,4,5,6]:
        dices = get_all_dices_len_n(i) #always has len 6**i
        farkles = get_farkle_count(dices)
        prob = farkles / 6**i
        print(f"For {i} dice probability of farkle is {farkles}/{6**i} --- ({100*prob}%)")

'''
Manually check that return_all_choices behaves like it should
'''
def test_cases_for_return_all_choices():
    test_cases = [
        [5,2,2,2,1,4]
    ]
    for dice in test_cases:
        print("="*32)
        print(dice)
        print("-"*24)
        for choice in return_all_choices(dice):
            print(choice)
    print("="*32)

##################################################################################################
##################################################################################################
##################################################################################################

# Uncomment any of the lines below to play with a thing
if __name__ == '__main__':
    # do_all_farkle_counts()
    test_cases_for_return_all_choices()