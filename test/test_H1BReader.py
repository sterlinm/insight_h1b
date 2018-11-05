import csv
import os
import unittest
from collections import Counter

from src.H1BReader import H1BReader


class TestConstruction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_path = "input/h1b_input.csv"
        cls.h1b = H1BReader(cls.file_path)
    
    def test_h1b_file_exists(self):
        
        self.assertEqual(self.file_path,
            self.h1b.file_path)
    
    def test_h1b_file_does_not_exist(self):
        bad_file = "input/not_a_file.csv"
        self.assertRaises(FileNotFoundError,
            H1BReader,
            bad_file)
    
    def test_header_is_first_row(self):

        with open(self.file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            first_row = next(reader)
            header = [col.upper() for col in first_row]
        
        self.assertEqual(header, self.h1b.header)

    def test_separator(self):
        # Separator is semicolon
        self.assertEqual(self.h1b._sep,";")
    
    def test_special_columns(self):
        self.assertEqual(self.h1b.status_col,"CASE_STATUS")
        self.assertEqual(self.h1b.state_col,"WORKSITE_STATE")
        self.assertEqual(self.h1b.occupation_col,"SOC_NAME")

    def test_counters_empty_dict(self):
        self.assertEqual(self.h1b.counters,{})
    

class TestAssignment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_path = "input/h1b_input.csv"
        cls.h1b = H1BReader(cls.file_path)

    def test_assign_file_path(self):
        with self.assertRaises(AttributeError):
            self.h1b.file_path = 'file.txt'
    
    def test_assign_sep(self):
        with self.assertRaises(AttributeError):
            self.h1b.sep = ','
    
    def test_assign_counters(self):
        c = Counter(['a','b','c'])
        with self.assertRaises(AttributeError):
            self.h1b.counters = c

    def test_assign_header(self):
        with self.assertRaises(AttributeError):
            self.h1b.header = ['a','b','c']
    
    def test_assign_occupation_col(self):
        with self.assertRaises(AttributeError):
            self.h1b.occupation_col = 'JOB_TITLE'
    
    def test_assign_state_col(self):
        with self.assertRaises(AttributeError):
            self.h1b.state_col = 'EMPLOYER_STATE'
    
    def test_assign_status_col(self):
        with self.assertRaises(AttributeError):
            self.h1b.status_col = 'VISA_STATUS'

class TestCountCalculations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_path = "input/h1b_input.csv"

    def test_count_calculation(self):
        h1b = H1BReader(self.file_path)
        h1b.calculate_counts('WORKSITE_STATE')

        # Check counts
        expectedCounts = {'FL':2,
                          'AL':1,
                          'CA':1,
                          'DE':1,
                          'GA':1,
                          'MD':1,
                          'NJ':1,
                          'TX':1,
                          'WA':1}
        self.assertEqual(h1b.counters['WORKSITE_STATE'], expectedCounts)

    def test_count_one_column_list(self):
        h1b = H1BReader(self.file_path)
        cols = ['WORKSITE_STATE']
        h1b.calculate_counts(cols)

        # Check keys of counters
        self.assertEqual(list(h1b.counters.keys()),cols)
    
    def test_count_one_column_str(self):
        h1b = H1BReader(self.file_path)
        cols = ['WORKSITE_STATE']
        h1b.calculate_counts(cols[0]) # pass in string instead of list

        # Check keys of counters
        self.assertEqual(list(h1b.counters.keys()),cols)


    def test_count_two_columns(self):
        h1b = H1BReader(self.file_path)
        cols = ['WORKSITE_STATE','SOC_NAME']
        h1b.calculate_counts(cols) # pass in string instead of list
        
        # test that keys of counter match cols
        counters_keys = sorted(h1b.counters.keys())
        cols = sorted(cols)
        self.assertEqual(cols, counters_keys)

        
    
    def test_count_column_does_not_exist(self):
        h1b = H1BReader(self.file_path)
        bad_col = 'ABC'
        exp_message = f"'{bad_col}' is not in file header."
        try:
            h1b.calculate_counts(bad_col)
        except ValueError as e:
            err_message = str(e)

        self.assertEqual(exp_message,err_message)
    
    def test_count_bad_column_value(self):
        h1b = H1BReader(self.file_path)
        bad_col = 1
        exp_message = 'Columns must be string or list of strings'
        try:
            h1b.calculate_counts(bad_col)
        except ValueError as e:
            err_message = str(e)

        self.assertEqual(exp_message,err_message)
    
    def test_count_bad_column_list(self):
        h1b = H1BReader(self.file_path)
        bad_col = ['WORKSITE_STATE',1]
        exp_message = 'Columns must be string or list of strings'
        try:
            h1b.calculate_counts(bad_col)
        except ValueError as e:
            err_message = str(e)

        self.assertEqual(exp_message,err_message)

        # Make sure it didn't modify counters for WORKSITE_STATE
        self.assertEqual(h1b.counters, {})
 
if __name__ == '__main__':
    unittest.main()
