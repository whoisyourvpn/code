# Using Python's 'random' Module
# Advantage: The 'random' module provides a convenient way to generate random numbers and sample from a range.
# Drawback: While suitable for many cases, it's pseudo-random, meaning that the sequence can be predicted if the initial seed is known.
# It's not suitable for cryptographic applications requiring true randomness.

import random

# Generate 5 random numbers within the range 1 to 115
random_numbers = random.sample(range(1, 116), 5)

# Print the random numbers
print(random_numbers)
