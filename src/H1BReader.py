import csv
import warnings
from collections import Counter


class H1BReader:

    # Specify filter column and value (e.g. STATUS==CERTIFIED)
    # group count arbitrary number of columns

    def __init__(self, file_path):

        self._file_path = file_path
        self._sep = ";"
        self.counters = {}

        # Get Header from file
        with open(self.file_path, 'r') as h1b_data:
            reader = csv.reader(h1b_data, delimiter=self._sep)
            self._header = [col.upper() for col in next(reader)]

        # Special Columns
        self._occupation_col = self._find_column(["SOC_NAME","LCA_CASE_SOC_NAME","OCCUPATIONAL_TITLE"])
        self._status_col = self._find_column(["CASE_STATUS", "STATUS", "APPROVAL_STATUS"])
        self._state_col = self._find_column(["WORKSITE_STATE", "LCA_CASE_WORKLOC1_STATE", "WORK_LOCATION_STATE1", "STATE_1"])

    def __repr__(self):
        return f'H1BReader("{self._file_path}")'

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

    def _find_column(self, possible_columns):

        found_columns = list(filter(lambda col: col in possible_columns, self.header))
        if len(found_columns)==0:
            raise KeyError(f"Header did not contain any of the columns: {possible_columns}")
        elif len(found_columns)>1:
            warnings.warn("Header contained more than one of {possible_columns}. Using {found_columns[0]}",RuntimeWarning)
        
        return found_columns[0]
    
    def calculate_counts(self, columns):
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
                        column_value = row[column_idx].upper()
                        colCounter[column].update([column_value])
            
            # Update self.counters with calculated counts
            self.counters.update(colCounter)

    def get_top_counts(self, column, n=10):
        if column not in self.counters:
            self.calculate_counts([column])
        top_n = sorted(self.counters[column].items(), key = lambda count: (-count[1], count[0]))[:n]
        return top_n
    
    def generate_report(self, column, file_name, n=10, column_label="TOP", sep = ";"):
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
        
        self.generate_report(self.occupation_col, file_name, n=n, column_label=column_label, sep=sep)

    def generate_state_report(self,n = 10,
            file_name="./output/top_10_states.txt",
            column_label="TOP_STATES",
            sep = ";"):
        
        self.generate_report(self.state_col, file_name, n=n, column_label=column_label, sep=sep)
