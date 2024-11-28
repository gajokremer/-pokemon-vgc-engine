#!/bin/bash

# Check if an input file is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 input_file"
  exit 1
fi

input_file=$1
output_file="copy.txt"

# Initialize variables
team_count=10
match_count=10
overall_wins=0
overall_ties=0
overall_winner="Example Player"

# Function to determine the winner of a team
determine_winner() {
  wins=0
  losses=0
  for match in "${team_results[@]}"; do
    score1=$(echo $match | cut -d',' -f1 | tr -d '[')
    score2=$(echo $match | cut -d',' -f2 | tr -d ']')
    if (( score1 > score2 )); then
      ((wins++))
    elif (( score2 > score1 )); then
      ((losses++))
    fi
  done
  if (( wins > losses )); then
    echo "Player 1"
    ((overall_wins++))
  elif (( losses > wins )); then
    echo "Player 2"
  else
    echo "Tie"
    ((overall_ties++))
  fi
}

# Read the input file
team_index=0
match_index=0
declare -a team_results

# Clear the output file
> "$output_file"

while IFS= read -r line; do
  if [[ $line == "MATCH RESULTS"* ]]; then
    team_results[match_index]=$(echo $line | sed 's/MATCH RESULTS //')
    ((match_index++))
    
    if (( match_index == match_count )); then
      ((team_index++))
      {
        echo "#### Team Build $team_index"
        for ((i=0; i<match_count; i++)); do
          echo "- Match $((i+1)): \$${team_results[i]}\$"
        done
        echo
        winner=$(determine_winner)
        echo "**_Winner:_** $winner"
        echo
      } >> "$output_file"
      match_index=0
      declare -a team_results
    fi
  fi
done < "$input_file"

# Handle the last team if it wasn't processed
if (( match_index > 0 )); then
  ((team_index++))
  {
    echo "#### Team Build $team_index"
    for ((i=0; i<match_count; i++)); do
      echo "- Match $((i+1)): \$${team_results[i]}\$"
    done
    echo
    winner=$(determine_winner)
    echo "**_Winner:_** $winner"
    echo
  } >> "$output_file"
fi

# Print overall winner to the output file
{
  echo "> **_Overall Winner:_** $overall_winner (${overall_wins} victories, ${overall_ties} ties)"
} >> "$output_file"

echo "Output written to $output_file"
