import pandas as pd
import pyautogui as gui
import csv

#system imports
import student_data
import functions

class CSV():
    CSV_FILE = "students.csv"
    COLUMNS = ["Student Id", "Name", "Age", "Grade", "Major"]

    @classmethod
    def csv_file(cls):
        try:
            pf = pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            pf = pd.DataFrame(cls.COLUMNS)
            pf.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def data_entry(cls, student_id, Name, Age, Grade, Major):
        new_entry = {
            "Student Id" : student_id,
            "Name" : Name,
            "Age" : Age,
            "Grade" : Grade,
            "Major" : Major
        }

        with open("students.csv", "a", newline="") as std_file:
            writer = csv.DictWriter(std_file, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)

    @classmethod
    def find_student(cls, student_id):
        while True:
            df = pd.read_csv(cls.CSV_FILE)
            
            if student_id in df["Student Id"].values:
                student = df[df["Student Id"] == student_id]
                found_stdent = gui.alert(student.to_string(), title=f"Student Id: {student_id}")

            else:
                found_stdent = gui.alert(f"No student found with Id: {student_id}", title="Not Found")

            return found_stdent
            

def main():
    while True:
        action = gui.confirm("studen data base funciones:", buttons=["Add Student", "view existing student", "find by ID", "sort by age", "soft by major", "Exit"], title="Student Database")

        #exit program
        if action == "Exit":
            gui.alert("Exiting the program.")
            quit()

        #sort by age
        elif action == "sort by age":
            while True:
                age = gui.prompt("Enter the age to filter by (enter a range of age by using ',' to filer an age group):", title="Filter by Age", default="e.g. 18")

                if not age:
                    gui.alert("Please enter a valid age.", title="Input Error")
                    continue
                    
                elif ", " in age or age.istudent_dataigit():
                    filtered_students = functions.EXTRACTED_DATA.get_by_age(str(age))
                    if filtered_students.empty:
                        gui.alert(f"No students found for the age: {age}", title="No Results")
                    else:
                        gui.alert(filtered_students.to_string(), title=f"Students aged: {age}")
                        main()

                else:
                    gui.alert("pleace chack your formet, formet: 'age, age', and make sure to enter a velid age", title="Input Error")
                    continue

        #sort by major
        elif action == "soft by major":
            while True:
                major = gui.prompt("Enter the major to filter by:", title="Filter by Major", default="e.g., Arts").title()

                if not major:
                    gui.alert("Please enter a valid major.", title="Input Error")
                    continue
                else:
                    filtered_students = functions.EXTRACTED_DATA.get_by_mejor(major)
                    if filtered_students.empty:
                        gui.alert(f"No students found for the major: {major}", title="No Results")
                    else:
                        gui.alert(filtered_students.to_string(), title=f"Students in Major: {major}")
                        main()


        #addting students
        elif action == "Add Student":
            student_id = student_data.student_id()
            name = student_data.name()
            age = student_data.age()
            grade = student_data.grade()
            major = student_data.major()

            CSV.csv_file()
            CSV.data_entry(student_id, name, age, grade, major)

            gui.alert("Student added successfully!", title="Success")

        # viewing existing students
        elif action == "view existing student":
                try:
                    df = pd.read_csv("students.csv")

                    if df.empty:
                        gui.alert("No student data found. Please add students first.", title="No Data")
                    else:
                        gui.alert(df.to_string(), title="Existing Students")
                except FileNotFoundError:
                    gui.alert("No student data found. Please add students first.", title="File Not Found")

        # finding a student by id
        elif action == "find by ID":
            student_id = gui.prompt("Enter the Student Id to search for:", title="Find Student", default="e.g., 1001")
            if not student_id.isdigit():
                gui.alert("Please enter a valid Student Id.", title="Id Error")
                continue
            else:
                student_id = int(student_id)
                student = CSV.find_student(student_id)
                return student, main()

main()