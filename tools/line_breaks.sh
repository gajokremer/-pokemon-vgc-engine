#!/bin/bash

# Check if a file was provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 filename"
    exit 1
fi

# Input file
input_file="$1"

# Check if the file exists
if [ ! -f "$input_file" ]; then
    echo "File not found!"
    exit 1
fi

# Output file
# same as input file with "_formatted" appended
output_file="${input_file%.*}_formatted.${input_file##*.}"

# Clear output file before starting
> "$output_file"

# Initialize line counter
line_counter=0

# Read the input file line by line
while IFS= read -r line
do
    echo "$line" >> "$output_file"
    line_counter=$((line_counter + 1))
    
    # Check if the line counter is a multiple of 10
    if [ $((line_counter % 10)) -eq 0 ]; then
        echo "" >> "$output_file"  # Add an empty line
    fi
done < "$input_file"

echo "Processed file saved as $output_file"
