#! /usr/bin/python

import pandas as pd
import numpy as np
from random import shuffle

class bidirectional_iterator(object):
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    def next(self):
        try:
            result = self.collection[self.index]
            self.index += 1
        except IndexError:
            raise StopIteration
        return result

    def prev(self):
        self.index -= 1
        if self.index < 0:
            raise StopIteration
        return self.collection[self.index]

    def __iter__(self):
        return self

def schedule(shift_iter, employee_status, shift_assignments):
	shift = next(shift_iter, None)
	if shift == None:
		return shift_assignments
	for index, employee in employee_status.sample(frac=1).iterrows():
		if employee.loc["shifts"] > 0 and employee.iloc[1 + shift_iter.index]:
			employee_status.loc[str(index), "shifts"] -= 1
			shift_assignments[shift_iter.index] = index
			print shift_assignments
			ret = schedule(shift_iter, employee_status, shift_assignments)
			if ret == 1:
				return 1
			else:
				employee["shifts"] += 1
	return 0

if __name__ == "__main__":
	truck_hours = pd.read_csv("truck_hours.csv")
	employee_hours = pd.read_csv("employee_hours.csv", index_col="Name")
	shift_times = [("12:00 PM", "4:00 PM"), ("4:00 PM", "8:00 PM"), ("8:00 PM", "12:00 AM")]

	shift_array = np.ndarray(shape=(14,len(shift_times))) 
	for index, row in truck_hours.iterrows():
		started = False
		ended = False
		for i in range(len(shift_times)):
			if((row["Start"] == shift_times[i][0] or started == True) and ended == False):
				shift_array[index][i] = True
				started = True
			else:
				shift_array[index][i] = False
			if(row["End"] == shift_times[i][1]):
				ended = True
	print shift_array

	schedule_array = np.ndarray(shape=(14,len(shift_times))).flatten()
	shift_assignments = np.ndarray(shape=(14,len(shift_times)), dtype=str).flatten()
	shifts = schedule(bidirectional_iterator(schedule_array), employee_hours, shift_assignments)
	print shifts

