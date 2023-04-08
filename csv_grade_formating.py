# Jye Floreani, Task 3.1p/3.2c, 23/03/2023, 9:30, 08/04/2023, 16:45
import numpy as np
import pandas as pd
from enum import Enum
# x_csv == function, csv_x == object/data

# filter a csv for errors and return float numpy array
def read_csv(csv_file_str):
    # split the file by newlines, then csv
    i = -1
    csv_arr = []
    # record of the elements filtered out
    erased_arr = []
    try:
        with open(csv_file_str, "r") as csv_file:
            line_split = csv_file.read().split('\n')
    except:
        print("File doesn't exist! Now exiting...")
        return
    for each in line_split:
        i = i + 1
        # test each element: if it's not a float, rm that line.
        # if it's a null element, rm that line
        csv_split = each.split(",")
        if(not all(x.replace(".", "", 1).isdigit() for x in csv_split)):
            erased_arr.append("{}th row has been erased".format(i))
            continue
        if(each == ""):
            erased_arr.append("{}th row has been erased".format(i))
            continue
        csv_arr.append(list(map(float, csv_split) ))
    # tell the user what rows were removed
    if(erased_arr is not None):
        print("\n".join(erased_arr))
    # convert native python list type into numpy array type
    csv_arr = np.array(csv_arr)
    return csv_arr

# save out csv with appropriate column names. Useful before save_csv
# col 6 == "total", col 7 == "final", col 8 == "grade"
def header_csv(csv_data):
    i = 0
    csv_grade_arr = []
    for each in csv_data:
        if(each[-1] >= 79.45):
            csv_grade_arr.append("HD")
        elif(each[-1] >= 69.45):
            csv_grade_arr.append("D")
        elif(each[-1] >= 59.45):
            csv_grade_arr.append("C")
        elif(each[-1] >= 49.45):
            csv_grade_arr.append("P")
        else:
            csv_grade_arr.append("N")
        i = i + 1
    # convert, then convert again. This is so it doesn't try to stack..
    # .. as a float type array
    stack1 = (np.round(csv_data[:,0], 0).astype(int)).astype(str)
    stack2 = np.round(csv_data[:,1:-1], 2)
    stack3 = (np.round(csv_data[:,-1], 0).astype(int)).astype(str)
    csv_data = np.column_stack((stack1, stack2, stack3))
    
    # adjust header size to match either 3.2C or 3.1P array size
    if(len(csv_data[0]) == 8):
        csv_header = np.array(["ID","Ass1","Ass2","Ass3","Ass4",
                               "Exam","Total","Final","Grade"])
        # restack and round the exam column specifically
        csv_data = np.column_stack((csv_data[:,:5],
                                    csv_data[:,5].astype(float).astype(int),
                                    csv_data[:,6:],
                                    csv_grade_arr))
    elif(len(csv_data[0]) == 6):
        csv_header = np.array(["ID","Ass1","Ass2","Ass3","Ass4","Exam"])
    # and then insert the header at the front
    csv_data = np.vstack((csv_header, csv_data))
    return csv_data

# save out a csv array as some file. Format it so it's human-readable
def save_csv(csv_data, csv_file_str):
    try:
        np.savetxt(csv_file_str, csv_data, fmt='%.1f', delimiter=',')
    except:
        np.savetxt(csv_file_str, csv_data, fmt='%s', delimiter=',')

# filter a csv to see if the value check in the column value..
# .. is between x and y, for every row. return float numpy array
def filter_csv(csv_arr, col, valchk1, valchk2):
    csv_fil_arr1 = [row for row in csv_arr if float(row[col]) >= valchk1]
    csv_fil_arr2 = [row for row in csv_fil_arr1 if float(row[col]) <= valchk2]
    return np.array(csv_fil_arr2)

# takes an array, writes and returns array with new column values.
# should be modular, but hard coded values should suffice for now
def write_csv(csv_arr):
    # MATHS: the formula for a WEIGHTED average is..
    # sum of all(w*x)/sum of all(w), and exam pct (x/120)*100
    # is logically equivalent to x*(100/120) = x*0.83333333
    i = 0
    csv_new_arr = np.copy(csv_arr)
    csv_new_arr[:,5] = np.multiply(csv_new_arr[:,5], 0.83333333)
    csv_new_arr[:,5] = np.round(csv_new_arr[:,5], 2)
    pct = np.array([0, 5, 15, 5, 15, 60])
    try:
        csv_total_arr = np.average(csv_new_arr, weights=pct, axis=1)
    except:
        pct = np.array([0, 5, 15, 5, 15, 60, 0, 0])
        csv_total_arr = np.average(csv_new_arr, weights=pct, axis=1)
    csv_total_arr = np.round(csv_total_arr, 2)
    csv_final_arr = np.copy(csv_total_arr)
    csv_new_arr[:,5] = 0
    for each in csv_arr:
        if(each[5] < 40):
            csv_final_arr[i] = np.average(csv_new_arr[i], weights=pct)
        i = i + 1
    csv_final_arr = np.round(csv_final_arr, 0)
    csv_new_arr = np.column_stack((csv_arr, csv_total_arr, csv_final_arr))
    return csv_new_arr

# returns and prints all of highest scorers for each assessment/exam
def highscore_csv(csv_arr):
    # declare all of our variables we're using before we start
    csv_print = []
    csv_new_arr = np.array([[]])
    itr = [0,0,0,0,0]
    highscores = np.max(csv_arr[:, 1:], axis=0)
    ass_enum = Enum('assessment',["Ass1","Ass2","Ass3","Ass4","exam"])
    
    for i, score in enumerate(highscores):
        # csv_arr[:,i+1] skips the ID, takes all elements for each..
        # .. 'assessment', AKA the entire column in the main dataset
        col = csv_arr[:,i+1]
        # maps to see 'where' the 'csv_data' matches the high'score's
        csv_indices = np.where(col == score)[0]
        for index in csv_indices:
            # itr == iterations for each assessment, in a list
            itr[i] = itr[i] + 1
            # np.append is rigid and will not dynamically add rows
            # so we need to prepare the csv_new_array by .reshaping() it
            csv_new_arr = np.array(csv_new_arr).reshape(-1,len(csv_arr[index,:]))
            csv_new_arr = np.append(csv_new_arr, [csv_arr[index,:]], axis=0)
            assessment = ass_enum(i+1).name
            csv_print.append("ID: {} with {} score on {}".format(
                int(csv_arr[index][0]), score, assessment))
    # for each in csv_print:
    #     print("".join(each))
    # print("\n")
    # y += x, keep track of continual row positions, to make sure you don't
    # print a row you've done before.
    y = 0
    for i, x in enumerate(itr):
        panda = panda_create(header_csv(csv_new_arr[y:y+x]))
        assessment = ass_enum(i+1).name
        print("student(s) with highest {}".format(assessment))
        display(panda)
        print("\n")
        y = y + x
    return csv_new_arr

# prints the average, minimum, maximum, for each student ID
def print_student_csv(csv_arr):
    i = 0
    csv_mean_arr = np.mean(csv_arr[:,1:], axis=1)
    csv_min_arr = np.min(csv_arr[:,1:], axis=1)
    csv_max_arr = np.max(csv_arr[:,1:], axis=1)
    csv_print = []
    # use list comprehension
    # actually, nevermind that, my brain can't figure it out rn
    for each in csv_arr:
        csv_print.append(["ID {} avg: {:.1f}".format(i+1, csv_mean_arr[i]),
                          "ID {} min: {:.1f}".format(i+1, csv_min_arr[i]),
                          "ID {} max: {:.1f}".format(i+1, csv_max_arr[i])])
        i = i + 1
    for each in csv_print:
        # /n doesn't work? huh? why?
        print("\n".join(each))
    print("\n")
    
# prints the average, minimum, maximum, for the entire csv
def print_total_csv(csv_arr):
    i = 0
    csv_mean_arr = np.mean(csv_arr[:,1:], axis=0)
    csv_min_arr = np.min(csv_arr[:,1:], axis=0) 
    csv_max_arr = np.max(csv_arr[:,1:], axis=0)
    csv_print = []
    for i in range(0, 4):
        csv_print.append(["ass{} avg: {:.1f}".format(i+1, csv_mean_arr[i]),
                          "ass{} min: {:.1f}".format(i+1, csv_min_arr[i]),
                          "ass{} max: {:.1f}".format(i+1, csv_max_arr[i])])
    csv_print.append(["exam avg: {:.1f}".format(csv_mean_arr[4]),
                      "exam min: {:.1f}".format(csv_min_arr[4]),
                      "exam max: {:.1f}".format(csv_max_arr[4])])
    for each in csv_print:
        print("\n".join(each))
        print("\n")

# input csv style np.array, output a panda DataFrame
def panda_create(csv_data):
    panda = pd.DataFrame(csv_data[1:,1:],
                         index=csv_data[1:,0],
                         columns=csv_data[0,1:])
    panda.columns.name = csv_data[0,0]
    return panda

# -- task 3.1P --
csv_file_str = "result_withoutTotal.csv"
csv_arr = read_csv(csv_file_str)
# print_student_csv(csv_arr)
print_total_csv(csv_arr)
highscore_csv(csv_arr)
# -- task 3.2C --
csv_new_arr = write_csv(csv_arr)
csv_fail_arr = header_csv(filter_csv(csv_new_arr, 5, 0, 49.45))
csv_new_arr = header_csv(csv_new_arr)
save_csv(csv_new_arr, "result_updated.csv")
save_csv(csv_fail_arr, "failedhurdle.csv")
# -- task 3.2C, pandas display --
panda = write_csv(csv_arr)

csv_everyone = header_csv(panda)
csv_lowest = header_csv(filter_csv(panda, 5, 0, 48))
csv_highest = header_csv(filter_csv(panda, 5, 100, 120))

panda_everyone = panda_create(csv_everyone)
panda_lowest = panda_create(csv_lowest)
panda_highest = panda_create(csv_highest)

display(panda_everyone)
print("\n")
display(panda_lowest)
print("\n")
display(panda_highest)
