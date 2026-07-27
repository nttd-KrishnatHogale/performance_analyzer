import pandas as pd

# This function processes the raw CPU data fetched from InfluxDB and calculates the total CPU usage.
def process_cpu(df):
    # Rename the 'mean' column to 'cpu_idle' for clarity.
    df.rename(columns={'mean': 'cpu_idle'}, inplace=True)
    # Convert the 'time' column to datetime format and calculate total CPU usage by summing up the relevant columns.
    df['time'] = pd.to_datetime(df['time'])
    # Calculate total CPU usage by summing up the relevant columns.
    df['cpu_usage'] = (
        df['dstat__total_cpu_usage__hiq'] +
        df['dstat__total_cpu_usage__siq'] +
        df['dstat__total_cpu_usage__stl'] +
        df['dstat__total_cpu_usage__sys'] +
        df['dstat__total_cpu_usage__usr'] +
        df['dstat__total_cpu_usage__wai']
    )
    # Set 'time' as the index of the DataFrame for easier time-based analysis.
    df.set_index('time', inplace=True)
    
    # return the processed DataFrame with total CPU usage and time index.
    return df