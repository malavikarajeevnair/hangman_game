import random
import sys
import os

# ----------------- Configuration & Data -----------------

# List of words for the game. Feel free to expand this!
WORD_LIST = [
    "PYTHON", "GEMINI", "PROGRAMMING", "COMPUTER", "ALGORITHM",
    "KEYBOARD", "FUNCTION", "VARIABLE", "MODULAR", "DEVELOPER"
]

# ASCII art for the hangman figure (7 stages, from 0 to 6 misses)
HANGMAN_STAGES = [
    """
       -----
       |   |
           |
           |
           |
           -
    """,  # 0 misses (Start)
    """
       -----
       |   |
       O   |
           |
           |
           -
    """,  # 1 miss (Head)
    """
       -----
       |   |
       O   |
       |   |
           |
           -
    """,  # 2 misses (Body)
    """
       -----
       |   |
       O   |
      /|   |
           |
           -
    """,  # 3 misses (Left Arm)
    """
       -----
       |   |
       O   |
      /|\\  |
           |
           -
    """,  # 4 misses (Both Arms)
    """
       -----
       |   |
       O   |
      /|\\  |
      /    |
           -
    """,  # 5 misses (Left Leg)
    """
       -----
       |   |
       O   |
      /|\\  |
      / \\  |
           -
    """   # 6 misses (Full Hangman - Game Over)
]

# The maximum number of incorrect guesses allowed
MAX_MISSES = len(HANGMAN_STAGES) - 1

# ----------------- Game Logic Functions -----------------

def get_word():
    """Selects a random word from the list."""
    return random.choice(WORD_LIST)

def display_game_state(word, guessed_letters, misses_left):
    """
    Prints the current state of the game: hangman art, hidden word, and guessed letters.
    """
    # 1. Print Hangman Art
    misses_count = MAX_MISSES - misses_left
    print("\n" * 2)
    print("---------------------------------")
    print(HANGMAN_STAGES[misses_count])
    print(f"Misses Left: {misses_left}/{MAX_MISSES}")
    print("---------------------------------")

    # 2. Print the word with gaps
    display_word = ""
    for letter in word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    print(f"\nWord: {display_word}")
    
    # 3. Print letters already guessed
    sorted_guesses = sorted(list(guessed_letters))
    print(f"Guessed Letters: {' '.join(sorted_guesses)}\n")

    return display_word

def get_guess(guessed_letters):
    """
    Prompts the user for a valid single-letter guess.
    """
    while True:
        try:
            guess = input("Enter your guess (a single letter): ").strip().upper()

            if len(guess) != 1 or not 'A' <= guess <= 'Z':
                print("Invalid input. Please enter exactly one alphabetical letter.")
            elif guess in guessed_letters:
                print(f"You already guessed '{guess}'. Try a different letter.")
            else:
                return guess
        except EOFError:
            # Handle Ctrl+D or end-of-file input gracefully
            print("\nExiting game.")
            sys.exit(0)
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nGame interrupted. Exiting.")
            sys.exit(0)


# ----------------- Main Game Loop -----------------

def play_hangman():
    """Runs the main Hangman game."""
    print("=" * 40)
    print("       Welcome to Console Hangman!")
    print("=" * 40)
    
    # Game initialization
    word_to_guess = get_word()
    guessed_letters = set()
    misses_left = MAX_MISSES
    game_over = False

    while not game_over:
        # Step 1: Display current game state
        current_display = display_game_state(word_to_guess, guessed_letters, misses_left)

        # Win condition check
        if "_" not in current_display:
            print("🎉 CONGRATULATIONS! You guessed the word!")
            game_over = True
            break
        
        # Loss condition check
        if misses_left <= 0:
            display_game_state(word_to_guess, guessed_letters, misses_left) # Show final state
            print("💀 GAME OVER! The man is hanged.")
            print(f"The word was: {word_to_guess}")
            game_over = True
            break

        # Step 2: Get user input
        guess = get_guess(guessed_letters)
        guessed_letters.add(guess)

        # Step 3: Process guess
        if guess in word_to_guess:
            print(f"\n--- Good guess! '{guess}' is in the word. ---")
        else:
            misses_left -= 1
            print(f"\n--- Incorrect guess. '{guess}' is NOT in the word. ---")

    # Ask to play again
    print("\n" + "=" * 40)
    if input("Play again? (Y/N): ").strip().upper() == 'Y':
        # Clear the screen for a new game (basic cross-platform attempt)
        os.system('cls' if os.name == 'nt' else 'clear')
        play_hangman()
    else:
        print("Thanks for playing! Goodbye.")

if __name__ == "__main__":
    play_hangman()
