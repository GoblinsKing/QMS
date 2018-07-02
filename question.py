import csv

def get_answer(answer):
    if answer == "Excellent":
        return 5
    elif answer == "Good":
        return 4
    elif answer == "Fair":
        return 3
    elif answer == "Poor":
        return 2
    elif answer == "Terrible":
        return 1
    else:
        return 0