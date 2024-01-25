def lcg(modulus, a, c, seed):
    """
    Implements a linear congruential generator (LCG) for generating pseudo-random numbers.
    
    The LCG is a simple and classic method for generating a sequence of pseudo-randomized numbers 
    based on a linear equation. This function yields a new number every time it's called.

    Parameters:
    modulus (int): The modulus of the LCG, which determines the range of the output numbers.
    a (int): The multiplier factor in the LCG formula.
    c (int): The increment factor in the LCG formula.
    seed (int): The initial value or 'seed' that starts off the sequence.
    
    Yields:
    int: The next pseudo-random number in the sequence.
    """
    while True:
        seed = (a * seed + c) % modulus  # LCG formula to calculate the next number
        yield seed  # Using 'yield' to create a generator that produces the next number in sequence

# Create a generator using the LCG function
# The generator will produce a sequence of pseudo-random numbers based on the given parameters.
random_generator = lcg(modulus=45, a=113, c=97, seed=1)

# Generate 5 random numbers in the range of 1 to 45
# The '+1' adjusts the range from [0, 44] to [1, 45]
random_numbers = [next(random_generator) + 1 for _ in range(5)]
print(random_numbers)
