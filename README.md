# Table of Contents

1. [Introduction](README.md#introduction)
2. [Problem](README.md#problem)
3. [Approach](README.md#approach)
4. [Run Instructions](README.md#run-instructions)
5. [Testing](README.md#testing)

# Introduction
This is my submission for the Insight Data Engineering coding challenge, as described [here](https://github.com/InsightDataScience/h1b_statistics). I decided to tackle the challenge using Python and will describe my approach below. Thank you for your consideration.

# Problem
A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visa application processing over the past years, trying to identify the occupations and states with the most number of approved H1B visas. She has found statistics available from the US Department of Labor and its [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). But while there are ready-made reports for [2018](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2018/H-1B_Selected_Statistics_FY2018_Q4.pdf) and [2017](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_Selected_Statistics_FY2017.pdf), the site doesn’t have them for past years. 

As a data engineer, you are asked to create a mechanism to analyze past years data, specificially calculate two metrics: **Top 10 Occupations** and **Top 10 States** for **certified** visa applications.

Your code should be modular and reusable for future. If the newspaper gets data for the year 2019 (with the assumption that the necessary data to calculate the metrics are available) and puts it in the `input` directory, running the `run.sh` script should produce the results in the `output` folder without needing to change the code.

# Approach

I chose to create an `H1BReader` class to handle the loading and processing of the data files. The `H1BReader` class made it straightforward to handle a number of issues we encounter in this project:

* Potentially large data files
* Inconsistent file structures
* Flexible report generation

The current design automatically will handle any files that match the structure found in any of the data files from 2008 through 2017. Furthermore, it provides a generic report generator method (`H1BReader.generate_report()`) that can generate summary files for whichever column the user would like. This should make it easy to handle future changes to the data format, should they occur.

The grouped counts can be calculated for any of the columns found in the provided file, and are stored in a dictionary of Counter objects. For the sake of efficiency, one can calculate multiple group counts simultaneously so as to avoid iterating through the entire data file multiple times. The following would iterate through the data file twice.

    from H1BReader import H1BReader

    h1b = H1BReader('input/h1b_input.csv')
    h1b.generate_occupation_report() # implicit call to h1b.calculate_counts(h1b.occupation_col)
    h1b.generate_state_report() # implicit call to h1b.calculate_counts(h1b.state_col)

On the other hand, this would involve only a single run through the data file:

    h1b = H1BReader('input/h1b_input.csv')
    h1b.calculate_counts([h1b.occupation_col, h1b.state_col])
    h1b.generate_occupation_report()
    h1b.generate_state_report()

# Run Instructions

The program can be run by either directly running the python script:

    python ./src/h1b_counting.py

Alternatively, use the provided shell script:

    sh ./run.sh

Either method will create the following output files:

* `output/top_10_occupations.txt`
* `output/top_10_states.txt`

# Testing

You can run unit tests from the root folder with the following command:

    python -m unittest discover test "test_*.py"

You can also run the test shell script in the insight_testsuite from that directory:

    cd insight_testsuite
    sh ./run_tests.sh