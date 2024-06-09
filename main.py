import time
#--------------------------------------------------------------
# Classes
#--------------------------------------------------------------

#Trie Node class representing a single node in the trie structure.
class TrieNode:
    # Initializes a TrieNode object with an empty children dictionary and is_end_of_word flag set to False.
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

#Trie class representing a trie data structure for efficient word storage and retrieval.
class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    # Class Methods
    def insert(self, word):
        """
        Inserts a word into the trie.
        
        Args:
            word (str): The word to be inserted into the trie.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        """
        Searches for a word in the trie.
        
        Args:
            word (str): The word to be searched in the trie.
        
        Returns:
            bool: True if the word is found in the trie, False otherwise.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        """
        Checks if any word in the trie starts with the given prefix.
        
        Args:
            prefix (str): The prefix to be checked.
        
        Returns:
            bool: True if any word in the trie starts with the prefix, False otherwise.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

#--------------------------------------------------------------
# Methods
#--------------------------------------------------------------

"""
get_user_input(): Prompt the user for relevant game information.

Returns:
letters: A dictionary containing letters associated with each side of the square box.
solution_length: The desired solution length (1 for 1-word, 2 for 2-word, 3 for 3-word).
"""
def get_user_input():
    # Prompt the user to input the letters associated with each side of the square box.
    # Validate the input to ensure it follows the game rules.
    sides = ['top', 'right', 'left', 'bottom']
    letters = {}

    print("")
    print("Game Info Input:")
    print("------------------------")

    for side in sides:
        while True:
            letters_input = input(f"Enter the letters associated with the {side} side (3 letters separated by spaces): ").strip().upper()
            letters_list = letters_input.split()
            if len(letters_list) != 3:
                print("Invalid input. Please enter exactly 3 letters.")
                continue
            if len(set(letters_list)) != 3:
                print("Invalid input. Please ensure all letters are unique.")
                continue
            letters[side] = letters_list
            break
    
    while True:
        solution_length = input("Enter the desired solution length (1 for 1-word, 2 for 2-word, 3 for 3-word): ")
        if solution_length not in ['1', '2', '3']:
            print("Invalid input. Please enter 1, 2, or 3.")
            continue
        else:
            solution_length = int(solution_length)
            break

    print("------------------------")
    print("Letters provided for each side: \n", letters)
    print("------------------------")
    return letters, solution_length


"""
load_dictionary(file_path): Load a dictionary of valid words into a trie.

Params:
file_path (str): The path to the dictionary file.

Returns:
Trie: A trie containing the loaded dictionary.
"""
def load_dictionary(file_path, gameData):
    trie = Trie()
    with open(file_path, 'r') as file:
        for word in file:
            word = word.strip().upper()
            # Flatten the list of letters from gameData
            puzzle_letters = [letter for letters in gameData.values() for letter in letters]
            # Check if the word can be formed using the letters from gameData
            if all(letter in puzzle_letters for letter in word):
                trie.insert(word)
    return trie


"""
find_possible_words(gameData, trie): Find word combinations using backtracking algorithm.

Params:
gameData (dict): A dictionary containing letters associated with each side of the box.
trie (Trie): A trie data structure containing a dictionary of valid words.

Returns:
list: A list of valid word combinations.
"""
def find_possible_words(gameData, trie):
    # Initialize the possible_word list
    possible_words = []
    
    # DEFINE RECURSIVE BACKTRACKING FUNCTION
    def backtrack(current_word, current_side, trie, gameData, possible_words):
        """
        Recursive backtracking function to generate word combinations.

        Args:
            current_word (list): A list of letters forming a partial word.
            current_side (str): The current side of the box being explored.
            trie (Trie): A trie data structure containing a dictionary of valid words.
            gameData (dict): A dictionary containing letters associated with each side of the box.
            possible_words (list): A list to store valid word combinations.
        """
        # Check if the current prefix has no valid continuations
        if not trie.starts_with(current_word):
            return
        # If the current word is a valid word, add it to the list of possible words
        if trie.search(current_word):
            possible_words.append(current_word)

        # Iterate over each side of the box
        for side, side_letters in gameData.items():
            # Exclude the current side being explored
            if side != current_side:
                # Iterate over each letter on the side
                for letter in side_letters:
                    # Recursively explore further with the updated word and side
                    next_word = current_word + [letter]
                    backtrack(next_word, side, trie, gameData, possible_words)
                    
    # Iterate over each side of the box
    for side, side_letters in gameData.items():
        # Iterate over each letter on the side
        for letter in side_letters:
            # Start the backtracking algorithm with the initial letter and the current side
            backtrack([letter], side, trie, gameData, possible_words)

    if (len(possible_words) == 0):
        print("find_possible_words: No words found.")
    return possible_words


"""
find_chains(possible_words, gameData): Find valid word chains using backtracking.

Params:
possible_words (list): A list of possible words.
gameData (dict): A dictionary containing letters associated with each side of the box.

Returns:
list: A list of valid word chains.
"""
def find_chains(possible_words, gameData, solution_length):

    def generate_chain(start_chain, remaining_letters):
        """
        generate_chain(start_chain, remaining_letters): RECURSIVELY generate valid word chains.

        Params:
        start_chain (list): The current chain of words being explored.
        remaining_letters (list): The list of remaining letters in the game data.

        Base Case:
        If the length of the start_chain exceeds 2 (2 words per solution)or there are no remaining letters in the game data, the function returns without further exploration.

        Logic:
        - Check if the current start_chain is too long or if all letters have been used. If so, terminate.
        - Find the last word and its last letter in the start_chain.
        - Iterate over possible_words to find potential continuations starting with the last letter of the last word.
        - For each valid continuation, recursively call generate_chain with the updated start_chain and remaining_letters.

        Returns:
        None. (Adds valid word chains to the valid_chain_solutions list.)
        """
        # Base case: If all letters have been used, stop exploration, and add chain to valid_chain_solutions
        if len(remaining_letters) <= 0:
            if len(start_chain) == 1:
                one_word_solutions.append(start_chain)
                return
            elif len(start_chain) == 2:
                two_word_solutions.append(start_chain)
                return
            elif len(start_chain) == 3:
                three_word_solutions.append(start_chain)
                return
            return
        if len(start_chain) >= solution_length:
            return
        
        # Find the last word and its last letter in the start_chain
        last_word = start_chain[-1]
        last_letter = last_word[-1]

        # Select every word as a potential continuation of the chain
        for word in possible_words:
            if word[0] == last_letter:
                new_start_chain = start_chain + [word]
                new_remaining_letters = remaining_letters.copy()
                for letter in word:
                    if letter in new_remaining_letters:
                        new_remaining_letters.remove(letter)
                    
                # Recursively call generate_chain with the updated start_chain and remaining_letters
                generate_chain(new_start_chain, new_remaining_letters)

    # Initialize remaining letters from gameData
    remaining_letters = [letter for letters in gameData.values() for letter in letters]

    # Initialize valid_chain_solutions
    one_word_solutions = []
    two_word_solutions = []
    three_word_solutions = []

    # Iterate over each word in the possible_words list
    for word in possible_words:
        new_remaining_letters = remaining_letters.copy()
        for letter in word:
            if letter in new_remaining_letters:
                new_remaining_letters.remove(letter)

        # First-Case-Call to generate_chain with the current word and remaining_letters
        generate_chain([word], new_remaining_letters)

    return one_word_solutions, two_word_solutions, three_word_solutions
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Main Function: Allows user to input puzzle data and find all 2-word solutions
def main():
    while True:
        # Get user input for the game data
        gameData, solution_length = get_user_input()
        
        
        # Execution time of load_dictionary
        loadDict_start_time = time.time()
        # Load the dictionary
        trie = load_dictionary('largest_data_accurate.txt', gameData)
        loadDict_end_time = time.time()
        
        # Execution time of find_possible_words
        findPossibleWords_start_time = time.time()
        # Find possible words
        possible_words = find_possible_words(gameData, trie)
        findPossibleWords_end_time = time.time()

        # Execution time of find_chains
        findChains_start_time = 0
        if possible_words:
            findChains_start_time = time.time()
            one_word_solutions, two_word_solutions, three_word_solutions = find_chains(possible_words, gameData, solution_length)
            findChains_end_time = time.time()
            if solution_length == 1:
                print("\nWinning One-Word Solutions: (", len(one_word_solutions), " solutions)")
                for chain in one_word_solutions:
                    print(chain)
            elif solution_length == 2:
                print("\nWinning Two-Word Solutions: (", len(two_word_solutions), " solutions)")
                for chain in two_word_solutions:
                    print(chain)
            elif solution_length == 3:
                print("\nWinning Three-Word Solutions: (", len(three_word_solutions), " solutions)")
                for chain in three_word_solutions:
                    print(chain)
            else:
                print("No winning chains found with desired solution length.")
        print()
        print("find_chains: {} seconds".format(findChains_end_time - findChains_start_time))
        print("load_dictionary: {} seconds".format(loadDict_end_time - loadDict_start_time))
        print("find_possible_words: {} seconds".format(findPossibleWords_end_time - findPossibleWords_start_time))

        break
        # Ask the user if they want to continue or quit
        user_input = input("Do you want to continue (y/n)? ").lower()
        if user_input != 'y':
            break
#------------------------------------------------------------------------------

# If Run as Main and not as Module
if __name__ == "__main__":
    main_start_time = time.time()
    main()
    main_end_time = time.time()
    print("Total time elapsed:", main_end_time - main_start_time)

