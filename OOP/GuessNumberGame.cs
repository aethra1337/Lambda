using System;

class GuessNumberGame {
    static void Main() {
        // 1. Create a random number generator
        Random random = new Random();
        int targetNumber = random.Next(1, 101); // Between 1 and 100
        int userGuess = 0;

        Console.WriteLine("I have picked a number between 1 and 100. Try to guess it!");

        // 2. Loop until the user finds the correct number
        while (userGuess != targetNumber) {
            Console.Write("Enter your guess: ");
            
            // Convert user input to integer
            userGuess = int.Parse(Console.ReadLine());

            // 3. Check the guess
            if (userGuess < targetNumber) {
                Console.WriteLine("Higher! Try again.");
            }
            else if (userGuess > targetNumber) {
                Console.WriteLine("Lower! Try again.");
            }
            else {
                Console.WriteLine("Congratulations! You found it.");
            }
        }
    }
}