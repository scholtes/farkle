from policy_future_planning import *
from policy_always_roll_with_n_remaining_dice import *


if __name__ == "__main__":
    #compare_policies(50000, always_roll_with_n_remaining_dice(3), leave_out_some_dice(n=3,k=3))
    compare_policies(50000, leave_out_some_dice(n=3,k=3), leave_out_some_dice(n=3,k=3,_115=True,_155=False))
    compare_policies(50000, leave_out_some_dice(n=3,k=3), leave_out_some_dice(n=3,k=3,_155=True,_115=False))