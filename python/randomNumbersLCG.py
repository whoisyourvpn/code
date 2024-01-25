import random
import string

# Generate a random 5-digit alphanumeric seed
seed = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

# Convert the alphanumeric seed to a numeric value
numeric_seed = sum(ord(char) for char in seed)

# Create a generator with the random seed
random_generator = lcg(modulus=100, a=113, c=97, seed=numeric_seed)

# Generate 5 random numbers
random_numbers = [next(random_generator) for _ in range(5)]
print(random_numbers)
