#!/usr/bin/env python

import argparse
from H1BReader import H1BReader

if __name__=="__main__":

    # Create Argument Parser
    parser = argparse.ArgumentParser(description="Process H-1B visa data and generate summaries.")
    parser.add_argument('-i', '--input',
        default="./input/h1b_input.csv",
        help="Input file with H-1B data")
    parser.add_argument('-s', '--state_output',
        default="./output/top_10_states.txt",
        help="Output file for top 10 states")
    parser.add_argument('-o', '--occupation_output',
        default="./output/top_10_occupations.txt",
        help="Output file for top 10 occupations")

    # Parse Input Arguments
    opts = parser.parse_args()
    input_file = opts.input
    occupation_file = opts.occupation_output
    state_file = opts.state_output

    # Instantiate H1BReader and generate output files
    h1b = H1BReader(input_file)
    h1b.calculate_counts([h1b.occupation_col, h1b.state_col])
    h1b.generate_occupation_report(file_name=occupation_file)
    h1b.generate_state_report(file_name=state_file)