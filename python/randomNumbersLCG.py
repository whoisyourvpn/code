def lcg(modulus, a, c, seed):
    while True:
        seed = (a * seed + c) % modulus
        yield seed

# Create a generator with a different seed value
random_generator = lcg(modulus=100, a=113, c=97, seed=42)

# Generate 5 random numbers
random_numbers = [next(random_generator) for _ in range(5)]
print(random_numbers)
