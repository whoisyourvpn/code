#include <iostream>
#include <random>
#include <set>

using namespace std;

int main() {
    // Using C++ Standard Library for Random Number Generation
    // Advantage: C++ provides a powerful random number generation framework via <random> library,
    // with various distributions and engines for different needs.
    // Drawback: Requires a more complex setup compared to Python's 'random' module.

    random_device rd;      // Random device engine, usually based on /dev/random on UNIX-like systems
    mt19937 rng(rd());     // Initialize Mersenne Twister pseudo-random number generator

    uniform_int_distribution<int> uni(1, 115); // Uniformly distributed in range (1, 115)

    set<int> random_numbers; // Set to store unique numbers

    // Generate 5 unique random numbers
    while (random_numbers.size() < 5) {
        int random_number = uni(rng);
        random_numbers.insert(random_number);
    }

    // Print the random numbers
    for (int num : random_numbers) {
        cout << num << ' ';
    }
    cout << endl;

    return 0;
}
