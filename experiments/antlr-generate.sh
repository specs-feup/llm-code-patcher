#!/bin/bash

# Install antlr python runtime
# pip install antlr4-python3-runtime

# Set the path to the ANTLR tool
ANTLR_PATH=""

# Set the input grammar file
GRAMMAR_FILE="./antlr/Declaration.g4"

# Set the output directory for generated files
OUTPUT_DIR="declparser"

# Generate the ANTLR files
java -jar $ANTLR_PATH -o $OUTPUT_DIR -Dlanguage=Python3 -Xexact-output-dir $GRAMMAR_FILE