import pandas as pd

def python_package():
    print("Your python package is created successfully")

def dataframe():
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Emma'],
        'Age': [25, 30, 35, 40, 45]
        }
    df = pd.DataFrame(data)
    print(df)