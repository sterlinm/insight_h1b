#!/usr/bin/env python

from H1BReader import H1BReader

if __name__=="__main__":
    h1b = H1BReader("input/h1b_input.csv")
    h1b.calculate_counts([h1b.occupation_col, h1b.state_col])
    h1b.generate_occupation_report()
    h1b.generate_state_report()