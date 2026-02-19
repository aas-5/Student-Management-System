import csv
import pandas as pd
import pyautogui as gui

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
            pf = pd.DataFrame(columns=cls.COLUMNS)
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
            if std_file.tell() == 0:
                writer.writeheader()
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
        action = gui.confirm(
            "Student database options:",
            buttons=[
                "Add Student",
                "View Existing Students",
                "Find by ID",
                "Sort by Age",
                "Sort by Major",
                "Exit",
            ],
            title="Student Database",
        )

        #exit program
        if action == "Exit":
            confirmation = gui.confirm("Are you sure you want to exit the program?", title="Exit Confirmation", buttons=["Yes", "No"])
            if confirmation == "Yes":
                quit()

        #sort by age
        elif action == "Sort by Age":
            while True:
                age = gui.prompt(
                    "Enter the age to filter by (use ',' to filter a range):",
                    title="Filter by Age",
                    default="e.g. 18 or 18, 21",
                )

                if not age:
                    gui.alert("Please enter a valid age.", title="Input Error")
                    continue

                if "," in age or age.strip().isdigit():
                    try:
                        filtered_students = functions.EXTRACTED_DATA.get_by_age(age)
                    except ValueError:
                        gui.alert(
                            "Please check your format: 'age' or 'age, age'.",
                            title="Input Error",
                        )
                        continue

                    if filtered_students.empty:
                        gui.alert(
                            f"No students found for the age: {age}",
                            title="No Results",
                        )
                    else:
                        gui.alert(
                            filtered_students.to_string(),
                            title=f"Students aged: {age}",
                        )
                    break

                gui.alert(
                    "Please check your format: 'age' or 'age, age', and make sure to enter a valid age.",
                    title="Input Error",
                )
                continue

        #sort by major
        elif action == "Sort by Major":
            while True:
                major = gui.prompt("Enter the major to filter by:", title="Filter by Major", default="e.g., Arts").title()

                if not major:
                    gui.alert("Please enter a valid major.", title="Input Error")
                    continue
                else:
                    filtered_students = functions.EXTRACTED_DATA.get_by_major(major)
                    if filtered_students.empty:
                        gui.alert(f"No students found for the major: {major}", title="No Results")
                    else:
                        gui.alert(filtered_students.to_string(), title=f"Students in Major: {major}")
                    break


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
        elif action == "View Existing Students":
                try:
                    df = pd.read_csv("students.csv")

                    if df.empty:
                        gui.alert("No student data found. Please add students first.", title="No Data")
                    else:
                        start = 0
                        page_size = 10
                        while True:
                            chunk = df[start:start + page_size]
                            text = chunk.to_string(index=False)
                            action = gui.confirm(text=text, title="Students", buttons=["Next", "Previous", "Exit"])

                            if action == "Exit":
                                break
                            elif action == "Next":
                                start += page_size
                                if start >= len(df):
                                    start = 0  # Loop back to the beginning
                            elif action == "Previous":
                                start -= page_size
                                if start < 0:
                                    start = max(0, len(df) - page_size)  # Loop back to the end
                        

                except FileNotFoundError:
                    gui.alert("No student data found. Please add students first.", title="File Not Found")

        # finding a student by id
        elif action == "Find by ID":
            student_id = gui.prompt("Enter the Student Id to search for:", title="Find Student", default="e.g., 1001")
            if not student_id.isdigit():
                gui.alert("Please enter a valid Student Id.", title="Id Error")
                continue
            else:
                student_id = int(student_id)
                CSV.find_student(student_id)
                continue

main()
