# Open the input file
input_filename = "best_data.txt"
output_filename = "best_best.txt"

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
            # Check if the length of the word is greater than 2
            if len(word) > 8:
                # Write the word to the output file
                output_file.write(word + "\n")

print("Words with length > 2 copied to", output_filename)
