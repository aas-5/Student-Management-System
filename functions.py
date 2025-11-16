import pandas as pd

class EXTRACTED_DATA():
    CSV_FILE = "students.csv"
    df = pd.read_csv(CSV_FILE)
    
    @classmethod
    def get_by_age(cls, age):
        if ',' in age:
            start_age, end_age = age.split(', ')
            start_age = int(start_age.strip())
            end_age = int(end_age.strip())

        else:
            start_age = int(age)
            end_age = None


        masked_df = cls.df[cls.df["Age"] >= start_age]
        if end_age is not None:
            masked_df = masked_df[masked_df["Age"] <= end_age]
            return masked_df
        else:
            masked_df = masked_df[masked_df["Age"] == start_age]
            return masked_df
    
    @classmethod
    def get_by_mejor(cls, mejor):
        filtered_students = cls.df[cls.df["Major"] == mejor]
        return filtered_students
    
