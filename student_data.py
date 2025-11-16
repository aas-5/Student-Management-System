import pyautogui as gui
import pandas as pd

def student_id():
    df = pd.read_csv("students.csv")["Student Id"].tolist()
    last_id = df[-1] if df else 1000
    student_id = last_id + 1
    return student_id

def name():
    while True:
        name = gui.prompt("Enter your name:", title="Student Name")
        if name == "":
            gui.alert("Name cannot be empty. Please enter a valid name.")
            continue

        return name.title()

def age():
    while True:
        age = gui.prompt("Enter your age:", title="Student Age")
        if not age.isdigit() or int(age) <= 0 or "":
            gui.alert("Please enter a valid age.")
            continue

        return age

def grade():
    marks = ""
    while True:
        grade = gui.prompt("Enter your avrage grade in the privious test:", title="Grade")
        if grade.isdigit():
            grade = int(grade)
            if 0 <= grade <= 100:
                if grade >= 75:
                    marks = "A"
                elif grade >= 50:
                    marks = "B"
                elif grade >= 35:
                    marks = "C"
                else:
                    marks = "F"
            else:
                gui.alert("incalide grade. Please enter a grade between 0 and 100.")
                continue
        else:
            gui.alert("Please enter a valid number for the grade.")
            continue
        return marks

def major():
    majors = ["Computer Science", "Mathematics", "Physics", "Chemistry", "Biology", "Engineering", "Business", "Arts"]
    while True:
        major = gui.prompt("Enter the major youd like to continue in (enter list to viwe all the majors available): ")

        if major.lower() == "list":
            gui.alert("\n".join(majors) + "\n", title="Available Majors")
            continue

        if major.title() in majors:
            return major.title()
        
        else:
            gui.alert("Major not found. Please choose from the available majors.")
            continue

