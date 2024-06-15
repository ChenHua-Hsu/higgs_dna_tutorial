#!/bin/bash

# Define the file path
file="../../HiggsDNA/higgs_dna/workflows/__init__.py"

# Define the lines to be added and the line numbers
line11="from higgs_dna.workflows.own_processor import OwnProcessor"
line24='workflows["ownprocessor"] = OwnProcessor'

echo "Modifying file: $file"

# Check if the line to be added at line 11 already exists
if ! grep -qF "$line11" "$file"; then
  sed -i "11i $line11" "$file"
  echo "Line added at position 11: $line11"
else
  echo "Line already exists at position 11: $line11"
fi

# Check if the line to be added at new_line_number already exists
if ! grep -qF "$line24" "$file"; then
  sed -i "24i $line24" "$file"
  echo "Line added at position 24: $line24"
else
  echo "Line already exists at position 24: $line24"
fi
