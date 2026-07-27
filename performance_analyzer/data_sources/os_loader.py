from influxdb import InfluxDBClient
from data_sources.influx_reader import InfluxReader
from processing.cpu_processor import process_cpu
from processing.memory_processor import process_memory

class OSReader:
    
    def getCPU (self, start_time, end_time, hostname):
        influx_reader = InfluxReader()
        # CPU data loading and processing
        # fetch CPU data from InfluxDB and convert to DataFrame
        cpu_df = influx_reader.query_cpu(start_time, end_time, hostname)
        # process CPU data: calculate total CPU usage and set time index
        cpu_processed_data = process_cpu(cpu_df)
        return cpu_processed_data

    
    def getMemory (self, start_time, end_time, hostname):
        influx_reader = InfluxReader()
        # Memory data loading and processing
        # fetch Memory data from InfluxDB and convert to DataFrame
        memory_df = influx_reader.query_memory(start_time, end_time, hostname)
        # process Memory data: calculate total, available, and percentage used memory, and set time index
        memory_processed_data = process_memory(memory_df)
        return memory_processed_data