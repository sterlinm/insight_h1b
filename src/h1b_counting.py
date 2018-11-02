import csv
from collections import defaultdict
from operator import itemgetter

# fn = '/Users/msterling/Development/insight_h1b/insight_testsuite/tests/test_1/input/h1b_input.csv'
fn = '/Users/msterling/Development/insight_h1b/insight_testsuite/tests/test_2/input/H1B_FY_2014.csv'

occupation_counts = defaultdict(int)
status_list = defaultdict(int)
total_certified = 0

with open(fn, newline='') as csvfile:
    freader = csv.reader(csvfile, delimiter=';')
    header = next(freader)

    # find relevant column indices
    # case_status_col = header.index("CASE_STATUS")
    # soc_code_col = header.index("SOC_CODE")
    # soc_name_col = header.index("SOC_NAME")
    case_status_col = header.index("STATUS")
    soc_code_col = header.index("LCA_CASE_SOC_CODE")
    soc_name_col = header.index("LCA_CASE_SOC_NAME")

    for row in freader:
        soc_code = row[soc_code_col]
        soc_name = row[soc_name_col]
        case_status = row[case_status_col]
        if case_status=="CERTIFIED":
            occupation_counts[soc_name] += 1
            total_certified += 1

num_items = 0
for occupation, num_certified in sorted(occupation_counts.items(), key=itemgetter(1, 0), reverse=True):
    print(f"{occupation};{num_certified};{100*num_certified/total_certified:.1f}%")
    num_items +=1
    if num_items>10:
        break
