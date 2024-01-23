#include <iostream>
#include <random>
#include <set>

int main() {
    std::random_device rd;  // Random device engine, usually based on /dev/random on UNIX-like systems
    std::mt19937 rng(rd()); // Initialize Mersenne Twister pseudo-random number generator

    std::uniform_int_distribution<int> uni(1, 115); // Uniformly distributed in range (1, 115)

    std::set<int> random_numbers; // Set to store unique numbers

    // Generate 5 unique random numbers
    while(random_numbers.size() < 5) {
        int random_number = uni(rng);
        random_numbers.insert(random_number);
    }

    // Print the random numbers
    for (int num : random_numbers) {
        std::cout << num << ' ';
    }
    std::cout << std::endl;

    return 0;
}
