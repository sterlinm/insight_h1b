import csv
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
        self._state_col = self._find_column(["EMPLOYER_STATE", "LCA_CASE_EMPLOYER_STATE", "STATE"])

    

    def __repr__(self):
        return f'H1BReader("{self._file_path}")'

    @property
    def file_path(self):
        return self._file_path
    
    @property
    def header(self):
        return self._header

    def _find_column(self, possible_columns):
        try:
            found_columns = list(filter(lambda x: x in possible_columns, self.header))
            return found_columns[0]
        except:
            print("Could not find column.")
    
    def calculate_counts(self, columns):
        with open(self.file_path, newline='') as h1b_data:
            reader = csv.reader(h1b_data, delimiter=self._sep)
            next(reader) # skip header
            header = self.header

            # exclude columns already in self.counters dictionary
            columns = [column for column in columns if column not in self.counters]

            # iterate through data rows
            column_idxs = [header.index(column) for column in columns]
            status_idx = header.index(self._status_col)

            colCounter = {column:Counter() for column in columns}
            for row in reader:
                case_status = row[status_idx].upper()
                # column_value = row[column_idx].upper()
                if case_status=="CERTIFIED":
                    for column, column_idx in zip(columns, column_idxs):
                        column_value = row[column_idx].upper()
                        colCounter[column].update([column_value])
            
            self.counters.update(colCounter)

    def get_top_counts(self, column, n=10):
        if column not in self.counters:
            self.calculate_counts([column])
        top_n = sorted(self.counters[column].items(), key = lambda count: (-count[1], count[0]))[:n]
        return top_n
    
    def generate_report(self, column, file_name, n=10, column_label="TOP"):
        top_counts = self.get_top_counts(column, n)
        total_certified = sum(self.counters[column].values())
        with open(file_name, 'w') as report:
            report.write(column_label + ";NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE")
            for col_value, num_certified in top_counts:
                percentage = 100*num_certified/total_certified
                report.write(f"\n{col_value};{num_certified};{percentage:.1f}%")
    
    def generate_occupation_report(self,n = 10,
            file_name="./output/top_10_occupations.txt",
            column_label="TOP_OCCUPATIONS"):
        
        self.generate_report(self._occupation_col, file_name, n=n, column_label=column_label)

    def generate_state_report(self,n = 10,
            file_name="./output/top_10_states.txt",
            column_label="TOP_STATES"):
        
        self.generate_report(self._state_col, file_name, n=n, column_label=column_label)