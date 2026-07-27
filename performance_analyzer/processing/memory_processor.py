import pandas as pd

# This function processes the raw Memory data fetched from InfluxDB and calculates total, available, and percentage used memory.
def process_memory(df):
    # Convert memory data time column and set index (unchanged)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    # Calculate total memory by summing up used, free, buff, and cach columns.
    df['total'] = df[['dstat__memory_usage__used',
                      'dstat__memory_usage__free',
                      'dstat__memory_usage__buff',
                      'dstat__memory_usage__cach']].sum(axis=1)
    # Calculate available memory by summing up free, buff, and cach columns.
    df['available'] = df[['dstat__memory_usage__free',
                          'dstat__memory_usage__buff',
                          'dstat__memory_usage__cach']].sum(axis=1)
    # Calculate percentage of used memory.
    df['pct_used'] = ((df['total'] - df['available']) / df['total']) * 100
    
    # return the processed DataFrame with total, available, and percentage used memory columns.
    return df