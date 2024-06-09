import re

# Function to check if a word contains consecutive repeated letters
def has_consecutive_repeated_letters(word):
    return bool(re.search(r'(.)\1', word))

# Open the input file
input_filename = "better_data2.txt"
output_filename = "best_data2.txt"
excluded_words = []

with open(input_filename, "r") as input_file:
    # Read all lines from the input file
    lines = input_file.readlines()

# Open the output file
with open(output_filename, "w") as output_file:
    # Iterate over each line in the input file
    for line in lines:
        # Split the line into words
        words = line.split()
        # Iterate over each word in the line
        for word in words:
            # Check if the word contains consecutive repeated letters
            if not has_consecutive_repeated_letters(word):
                # Write the word to the output file
                output_file.write(word + "\n")
            else:
                # Add excluded word to list
                excluded_words.append(word)

print("Words without consecutive repeated letters copied to", output_filename)

# Output excluded words to console
print("Excluded words:")
for word in excluded_words:
    print(word)
