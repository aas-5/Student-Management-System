import pandas as pd

class EXTRACTED_DATA():
    CSV_FILE = "students.csv"

    @classmethod
    def _read_df(cls):
        try:
            return pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            return pd.DataFrame(columns=["Student Id", "Name", "Age", "Grade", "Major"])
    
    @classmethod
    def get_by_age(cls, age):
        df = cls._read_df()
        if ',' in age:
            start_age, end_age = age.split(',', 1)
            start_age = int(start_age.strip())
            end_age = int(end_age.strip())

        else:
            start_age = int(age)
            end_age = None


        masked_df = df[df["Age"] >= start_age]
        if end_age is not None:
            return masked_df[masked_df["Age"] <= end_age]
        return masked_df[masked_df["Age"] == start_age]
    
    @classmethod
    def get_by_major(cls, major):
        df = cls._read_df()
        filtered_students = df[df["Major"] == major]
        return filtered_students
    
