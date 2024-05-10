# Copyright (c) 2024 구FS, all rights reserved. Subject to the MIT licence in `licence.md`.
import math


def round_sig(x: float, significants: int) -> float:    
    """
    Round x to significant number. If significants is smaller 1, always returns 0.

    Arguments:
    - x: number to round
    - significants: number of significant digits to round to

    Returns:
    - x: rounded number
    """

    x=float(x)


    if x==0:    # if x is 0: magnitude determination fails, but rounded number always 0
        return x

    magnitude=math.floor(math.log10(abs(x)))    # determine magnitude floored
    x=round(x, -1*magnitude+significants-1)     # round #type:ignore
   
    return x