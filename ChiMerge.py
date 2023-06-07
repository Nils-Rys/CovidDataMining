import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import warnings

class Discretization():
    def __init__(cls):
        print("data discretization process started")
    
    def get_new_intervals(cls, intervals, chi, min_chi):
        min_chi_index = np.where(chi == min_chi)[0][0]
        new_intervals = []
        skip = False
        done = False
        for i in range(len(intervals)):
            if skip:
                skip = False
                continue
            if i == min_chi_index and not done:
                t = intervals[i] +intervals[i+1]
                new_intervals.append([min(t), max(t)])
                skip = True
                done = True
            else:
                new_intervals.append(intervals[i])
        return new_intervals
    
    def get_chimerge_intervals(cls, data, colName, label, max_intervals):
        distinct_vals = np.unique(data[colName])
        labels = np.unique(data[label])

        empty_count = {l: 0 for l in labels}
        intervals = [[distinct_vals[i], distinct_vals[i]] for i in range(len(distinct_vals))]
        while len(intervals) > max_intervals:
            chi = []
            print("NEW")
            print(len(intervals))
            for i in range(len(intervals)-1):
                row1 = data[data[colName].between(intervals[i][0], intervals[i][1])]

                row2 = data[data[colName].between(intervals[i+1][0], intervals[i+1][1])]
                total = len(row1 + row2)

                count_0 = np.array([v for i, v in {**empty_count, **Counter(row1[label])}.items()])
                count_1 = np.array([v for i, v in {**empty_count, **Counter(row2[label])}.items()])
                count_total = count_0+count_1
                expected_0 = count_total*sum(count_0)/total
                expected_1 = count_total*sum(count_1)/total
                chi_ = (count_0 - expected_0)**2/expected_0+(count_1-expected_1)**2/expected_1
                chi_ = np.nan_to_num(chi_)
                chi.append(sum(chi_))
            min_chi = min(chi)
            intervals = cls.get_new_intervals(intervals, chi, min_chi)
        print("min chi square value is " + str(min_chi))
        return intervals
                



def start(crosstab):
    max_intervals = 13
    obj = Discretization()

    for colName in crosstab.columns[0:-1]:
        print('\n interval for', colName)
        intervals = obj.get_chimerge_intervals(crosstab, colName, crosstab.columns[-1], max_intervals)
        
        print (intervals)
        with open("intervals.txt", "w") as txt_file:
            for line in intervals:
                txt_file.write(" ".join(line) + "\n") # works with any number of elements in a line

        print(tabulate([[intervals]], tablefmt='fancy_grid'))