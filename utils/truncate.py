import math


def truncate_float(number, decimals=3):
    if not isinstance(number, float):
        return number  # Return as is if not a float
    if number >= 1:
        factor = 10.0 ** decimals
    else:
        # For numbers less than 1, adjust decimals to keep significant digits
        decimals = abs(int(math.floor(math.log10(abs(number))))) + 3
        factor = 10.0 ** decimals
    return int(number * factor) / factor