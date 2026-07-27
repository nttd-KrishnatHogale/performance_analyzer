import pandas as pd

# Function to process JMeter results: convert timestamps, calculate response time and latency, and filter by time range
def process_jmeter(df, start, end):
    # Convert 'timeStamp' from milliseconds to datetime and set as index
    df['time'] = pd.to_datetime(df['timeStamp'], unit='ms', utc=True)
    df.set_index('time', inplace=True)
    # Calculate response time and latency, and convert success to binary
    df['response_time'] = df['elapsed']
    df['latency'] = df['Latency']
    df['success'] = df['success'].astype(int)
    df['error'] = 1 - df['success']
    # keep only required columns for analysis
    df = df[[
        'response_time',
        'latency',
        'success',
        'error',
        'grpThreads',
        'allThreads',
        'label'
    ]]
    # Filter data to include only records within the specified time range
    df = df[
        (df.index >= start) &
        (df.index <= end)
    ]

    # return the processed DataFrame with relevant columns
    return df