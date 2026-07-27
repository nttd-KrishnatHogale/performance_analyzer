import pandas as pd
from pathlib import Path

# Function to load JMeter CSV files from a specified directory and concatenate them into a single DataFrame
def load_jmeter_files(path):
    # List to hold individual DataFrames for each CSV file
    df_list = []
    # Iterate through all files in the specified directory
    for file_path in Path(path).iterdir():
        if file_path.is_file():
            # Read the CSV file into a DataFrame, treating the 4th column as string to handle potential non-numeric values
            df = pd.read_csv(file_path, sep=',', dtype={3: str})
            # Convert the 4th column to numeric, coercing errors to NaN, and append the DataFrame to the list
            col_name_3 = df.columns[3]
            # Coerce non-numeric values to NaN and convert the column to numeric type
            df[col_name_3] = pd.to_numeric(df[col_name_3], errors='coerce')
            # Append the processed DataFrame to the list
            df_list.append(df)
    # Concatenate all DataFrames in the list into a single DataFrame, ignoring the original index
    return pd.concat(df_list, ignore_index=True)