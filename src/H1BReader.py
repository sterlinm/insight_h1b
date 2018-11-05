import csv
import warnings
from collections import Counter


class H1BReader:
    """H1BReader accepts the path to an H-1B data file and provides methods for
    calculating group counts and writing out reports which count the number of
    certified visa applications grouped by the specified column.
    """

    def __init__(self, file_path):

        self._file_path = file_path
        self._sep = ";"
        self._counters = {}

        # Get Header from file
        try:
            with open(self.file_path, 'r') as h1b_data:
                reader = csv.reader(h1b_data, delimiter=self._sep)
                self._header = [col.upper() for col in next(reader)]
        except FileNotFoundError:
            raise FileNotFoundError(f"{self.file_path} does not exist")

        # Valid occupation, status, and state column names
        # These are ordered such that if there are duplicates the first found is used
        self._possible_occupation_cols = ["SOC_NAME","LCA_CASE_SOC_NAME","OCCUPATIONAL_TITLE"]
        self._possible_status_cols = ["CASE_STATUS", "STATUS", "APPROVAL_STATUS"]
        self._possible_state_cols = ["WORKSITE_STATE", "LCA_CASE_WORKLOC1_STATE", "WORK_LOCATION_STATE1", "STATE_1"]

        # Identify occupation, state, and status columns
        self._occupation_col = self._find_column(self._possible_occupation_cols)
        self._status_col = self._find_column(self._possible_status_cols)
        self._state_col = self._find_column(self._possible_state_cols)

    def __repr__(self):
        return f'H1BReader("{self._file_path}")'

    # In order to avoid accidental overwriting of important properties,
    # access to many properties is hidden (but still possible to overwrite if motivated)
    @property
    def file_path(self):
        return self._file_path
    
    @property
    def header(self):
        return self._header

    @property
    def occupation_col(self):
        return self._occupation_col
    
    @property
    def status_col(self):
        return self._status_col
    
    @property
    def state_col(self):
        return self._state_col
    
    @property
    def sep(self):
        return self._sep

    @property
    def counters(self):
        return self._counters

    def _find_column(self, possible_columns):
        """Utility function for finding which columns in the provided list of possible
        columns can be found in the header.
        """
        found_columns = list(filter(lambda col: col in possible_columns, self.header))
        if len(found_columns)==0:
            raise KeyError(f"Header did not contain any of the columns: {possible_columns}")
        elif len(found_columns)>1:
            warnings.warn("Header contained more than one of {possible_columns}. Using {found_columns[0]}",RuntimeWarning)
        
        return found_columns[0]
    
    def calculate_counts(self, columns):
        """Update self.counters with a counter object for each of the listed columns.
        This function ignores columns which have already been counted, and returns
        an error if the list contains columns that are not found in the file header.
        It iterates through the data file a single time for each call, regardless of the
        number of columns provided.
        """

        # Validate type of columns - must be str or list of str
        if type(columns) is not list:
            columns = [columns]
        if any([type(c) is not str for c in columns]):
            raise ValueError('Columns must be string or list of strings')

        with open(self.file_path, newline='') as h1b_data:
            reader = csv.reader(h1b_data, delimiter=self._sep)
            next(reader) # skip header
            header = self.header

            # exclude columns already in self.counters dictionary
            # convert columns to uppercase
            columns = [column.upper() for column in columns if column not in self.counters]

            # Find index of columns
            column_idxs = []
            try:
                for column in columns:
                    column_idxs.append(header.index(column))
            except ValueError:
                raise ValueError(f"'{column}' is not in file header.")
            
            # Find index of status column
            status_idx = header.index(self._status_col)

            # Initialize counters for each column to be scanned
            colCounter = {column:Counter() for column in columns}

            # Iterate through data records in file
            for row in reader:
                case_status = row[status_idx].upper()
                if case_status=="CERTIFIED":
                    for column, column_idx in zip(columns, column_idxs):
                        try:
                            column_value = row[column_idx].upper()
                        except IndexError:
                            raise IndexError('Input file is malformed.')
                        colCounter[column].update([column_value])
            
            # Update self.counters with calculated counts
            self._counters.update(colCounter)

    def get_top_counts(self, column, n=10):
        """Provide a sorted list of the top n items in the counter specified
        by column. The specified count is calculated if it is not already in
        self.counters. The list is sorted by count (descending), and then by
        the value of the counter keys in the case of ties.
        """
        # Validate n
        if type(n) is not int:
            raise TypeError('n must be an integer')
        elif n<0:
            raise ValueError('n must be greater than or equal to zero')

        # Validate column
        if type(column) is not str:
            raise TypeError('column must be a string')
        
        # Calculate counts for column (only done if not already calculated)
        self.calculate_counts(column)
        
        # Return top n from appropriate counter
        # Sort by count, then key value
        top_n = sorted(self.counters[column].items(),
                       key = lambda count: (-count[1], count[0]))[:n] # return up to n items
        return top_n
    
    def generate_report(self, column, file_name, n=10, column_label="TOP", sep = ";"):
        """Generate a semicomma delimited report of the top n items for the specified counter.
        Calculate an additional column for the percentage of total.
        """
        top_counts = self.get_top_counts(column, n)
        total_certified = sum(self.counters[column].values())
        with open(file_name, 'w') as report:
            report.write(sep.join([column_label, "NUMBER_CERTIFIED_APPLICATIONS", "PERCENTAGE"]))
            for col_value, num_certified in top_counts:
                percentage = 100*num_certified/total_certified
                report.write(f"\n{col_value}{sep}{num_certified}{sep}{percentage:.1f}%")
    
    def generate_occupation_report(self,n = 10,
            file_name="./output/top_10_occupations.txt",
            column_label="TOP_OCCUPATIONS",
            sep = ";"):
        """Generate a report for the top occupations, as identified by the column self.occupation_col.
        """
        
        self.generate_report(self.occupation_col, file_name, n=n, column_label=column_label, sep=sep)

    def generate_state_report(self,n = 10,
            file_name="./output/top_10_states.txt",
            column_label="TOP_STATES",
            sep = ";"):
        """Generate a report for the top states, as identified by the column self.occupation_col.
        """
        
        self.generate_report(self.state_col, file_name, n=n, column_label=column_label, sep=sep)
