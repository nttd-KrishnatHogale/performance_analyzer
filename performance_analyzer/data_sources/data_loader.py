# from data_sources.influx_reader import InfluxReader
# from performance_analyzer.data_sources.data_loader import dataLoader
from performance_analyzer.data_sources.influx_reader import InfluxReader
from performance_analyzer.data_sources.jmeter_reader import load_jmeter_files
from performance_analyzer.data_sources.apache_reader import ApacheReader
from performance_analyzer.data_sources.tomcat_reader import TomcatReader
from performance_analyzer.data_sources.oracle_reader import OracleReader
from performance_analyzer.data_sources.os_loader import OSReader

from performance_analyzer.processing.cpu_processor import process_cpu
from performance_analyzer.processing.memory_processor import process_memory
from performance_analyzer.processing.jmeter_processor import process_jmeter
from backend.utils.logger import Logger

logger = Logger.get_logger()
from performance_analyzer.config import settings


def merge_dataframes(df_list):
    """
    Safely merge multiple dataframes on time index
    """

    # Filter valid dfs
    dfs = [df for df in df_list if df is not None and not df.empty]

    if not dfs:
        return None

    combined = dfs[0]

    for df in dfs[1:]:

        # Remove overlapping columns
        overlap = combined.columns.intersection(df.columns)
        df = df.drop(columns=overlap, errors='ignore')

        combined = combined.join(df, how='outer')

    combined.fillna(0, inplace=True)

    return combined

# This function will load data from InfluxDB and JMeter results, process it, and return the processed data for further analysis.
def dataLoader(config):
    # dictionary to hold dataframes for each data source
    
    metrics_collection = {
            "servers": {},
            "jmeter": None   # global data
        }


    # load JMeter results from CSV files, convert timestamps, calculate response time and latency, and filter by time range
    jmeter_files = load_jmeter_files(settings.JMeterResultPath)
    # process JMeter data: convert timestamps, calculate response time and latency, and filter by time range
    jmeter_processed_data = process_jmeter(jmeter_files, settings.START_TIME, settings.END_TIME)
    # append processed JMeter data to the dictionary of dataframes
    metrics_collection["jmeter"] = jmeter_processed_data

    os_loader = OSReader()

    for hostname, server_data in config.servers.items():
            metrics_collection["servers"][hostname] = {
                "cpu": None,
                "memory": None,
                "apache": {},
                "tomcat": {},
                "oracle": {}
            }
            # load CPU & MEMORY data
            cpu_df = os_loader.getCPU(settings.START_TIME,settings.END_TIME, hostname)
            logger.info(
    f"{hostname} CPU Records : "
    f"{0 if cpu_df is None else len(cpu_df)}"
)
            mem_df = os_loader.getMemory(settings.START_TIME,settings.END_TIME, hostname)
            logger.info(
    f"{hostname} Memory Records : "
    f"{0 if mem_df is None else len(mem_df)}"
)
            metrics_collection["servers"][hostname]["cpu"] = cpu_df
            metrics_collection["servers"][hostname]["memory"] = mem_df

            
            # load APACHE instance data
            for instance in server_data["apache"]:
                # Apache data loading and processing
                # Initialize the Apache reader
                apache_reader = ApacheReader()
                # fetch Apache data from InfluxDB and convert to DataFrame
                apache_modstatus_df = apache_reader.get_modstatus(settings.START_TIME, settings.END_TIME, hostname, instance)
                apache_throughput_df = apache_reader.get_throughput(settings.START_TIME, settings.END_TIME, hostname, instance)
                # append processed Apache data to the dictionary of dataframes
                apache_df = merge_dataframes([apache_modstatus_df, apache_throughput_df])
                
                metrics_collection["servers"][hostname]["apache"][instance] = apache_df
            
            
            # load TOMCAT instance data
            for instance in server_data["tomcat"]:
                # Tomcat data loading and processing
                # Initialize the Tomcat loader
                tomcat_reader = TomcatReader()
                # fetch Tomcat data from InfluxDB and convert to DataFrame
                tomcat_jvm_metric_df = tomcat_reader.get_jvm_metrics(settings.START_TIME, settings.END_TIME, hostname, instance)
                tomcat_thread_metric_df = tomcat_reader.get_thread_metrics(settings.START_TIME, settings.END_TIME, hostname, instance)
                tomcat_ds_metrics_df = tomcat_reader.get_ds_metrics(settings.START_TIME, settings.END_TIME, hostname, instance)
                tomcat_session_metrics_df = tomcat_reader.get_session_metrics(settings.START_TIME, settings.END_TIME, hostname, instance)
                tomcat_df = merge_dataframes([tomcat_jvm_metric_df, tomcat_thread_metric_df, tomcat_ds_metrics_df, tomcat_session_metrics_df])
                metrics_collection["servers"][hostname]["tomcat"][instance] = tomcat_df
            
            
            # ✅ ORACLE
            for sid in server_data["oracle"]:
                # Oracle data loading and processing
                # Initialize the Oracle loader
                oracle_reader = OracleReader()
                # fetch Oracle data from InfluxDB and convert to DataFrame
                oracle_data = oracle_reader.load_all(settings.START_TIME,settings.END_TIME, hostname, sid)
                # append processed Oracle data to the dictionary of dataframes
                metrics_collection["servers"][hostname]["oracle"][sid] = oracle_data

    return metrics_collection