from performance_analyzer.core.config_manager import ConfigManager
from performance_analyzer.data_sources.data_loader import dataLoader
import json
from backend.utils.logger import Logger
from performance_analyzer.llm.rca_engine import LLMRCAEngine
from performance_analyzer.report.report_generator import ReportGenerator

logger = Logger.get_logger()
def print_sample_data(metrics_collection, rows=5):
    print("\n===== JMETER SAMPLE =====")
    jmeter_df = metrics_collection["jmeter"]
    if jmeter_df is not None:
        print(jmeter_df.head(5))
    else:
        print("No JMeter data")
    
    for hostname, server_data in metrics_collection["servers"].items():

        print(f"\n===== SERVER: {hostname} =====")

        # CPU
        if server_data.get("cpu") is not None:
            print("\n--- CPU SAMPLE ---")
            print(server_data["cpu"].head(rows))

        # Memory
        if server_data.get("memory") is not None:
            print("\n--- MEMORY SAMPLE ---")
            print(server_data["memory"].head(rows))

        # Apache
        for inst, df in server_data.get("apache", {}).items():
            print(f"\n--- APACHE ({inst}) SAMPLE ---")
            print(df.head(rows))

        # Tomcat
        for inst, df in server_data.get("tomcat", {}).items():
            print(f"\n--- TOMCAT ({inst}) SAMPLE ---")
            print(df.head(rows))

        # Oracle
        for sid, db_data in server_data.get("oracle", {}).items():
            print(f"\n--- ORACLE ({sid}) SAMPLE ---")

            for table, df in db_data.items():
                print(f"\n   [{table.upper()}]")
                print(df.head(rows))


def run_analysis(config_path,run_id):

    config = ConfigManager(config_path)

    metrics_collection = dataLoader(config)


    # ==========================================================
    # DEBUG - Print all available metrics and DataFrame columns
    # ==========================================================

    print("\n" + "=" * 100)
    print("METRICS COLLECTION")
    print("=" * 100)

    # JMeter
    if metrics_collection.get("jmeter") is not None:
        print("\nJMETER COLUMNS")
        print(metrics_collection["jmeter"].columns.tolist())

    # Servers
    for hostname, server in metrics_collection["servers"].items():

        print("\n")
        print("=" * 80)
        print(f"HOST : {hostname}")
        print("=" * 80)

        # CPU
        cpu = server.get("cpu")
        if cpu is not None:
            print("\nCPU Columns")
            print(cpu.columns.tolist())

        # Memory
        memory = server.get("memory")
        if memory is not None:
            print("\nMemory Columns")
            print(memory.columns.tolist())

        for inst, df in server.get("apache", {}).items():

            print(f"\nApache Instance : {inst}")

            if df is not None:
                print(df.columns.tolist())
            else:
                print("No Apache Data")


        for inst, df in server.get("tomcat", {}).items():

            print(f"\tomcat Instance : {inst}")

            if df is not None:
                print(df.columns.tolist())
                print("Rows :", len(df))
                print(df.head())
            else:
                print("No tomcat Data")

        # Oracle
        for sid, tables in server.get("oracle", {}).items():

            print(f"\nOracle SID : {sid}")

            for table_name, df in tables.items():

                print(f"Table : {table_name}")

                if df is not None:
                    print(df.columns.tolist())
                    print("Rows :", len(df))
                    print(df.head())

    print("=" * 100)


    # ==========================================================
    from performance_analyzer.timeline.timeline_builder import TimelineBuilder
    from performance_analyzer.config import settings


    timeline_data = TimelineBuilder().build(
    metrics_collection,
    settings
    )

    timeline = timeline_data["timeline"]

    apache_analysis = timeline_data["apache"]

    tomcat_analysis = timeline_data["tomcat"]

    oracle_analysis = timeline_data["oracle"]

    for event in timeline:
        print(event)



    print("\nOracle")
    print(timeline_data["oracle"])


    from performance_analyzer.jmeter.jmeter_analyzer import JMeterAnalyzer

    jmeter_analysis = JMeterAnalyzer().analyze(
        metrics_collection["jmeter"]
    )
    from performance_analyzer.correlation.correlation_engine import CorrelationEngine

    correlations = CorrelationEngine().analyze(
    metrics_collection,
    apache_analysis,
    tomcat_analysis,
    oracle_analysis
)

    logger.info("=" * 80)
    logger.info("CORRELATION ENGINE")
    logger.info("=" * 80)

    for c in correlations:

        logger.info(
            "%s --> %s | %.2f",
            c["source"],
            c["target"],
            c["confidence"]
        )


    from backend.configuration.server_configuration_collector import (
    ServerConfigurationCollector)
    from backend.ssh.ssh_client import SSHClient
    from backend.configuration.jmeter_config import JMeterConfig
    ssh = SSHClient()

    configuration = ServerConfigurationCollector(
        ssh
    ).collect()

    configuration["jmeter"] = JMeterConfig().collect()
    from performance_analyzer.jmeter.dashboard_locator import DashboardLocator
    from performance_analyzer.jmeter.dashboard_parser import DashboardParser

    dashboard = DashboardLocator.latest_dashboard(
        r"C:/KrishnatHOgale/PerformancePlatform/reports/jmeter"
    )

    dashboard_summary = DashboardParser().parse(dashboard)


    llm_report = LLMRCAEngine().generate(

        timeline,
        apache_analysis,
        tomcat_analysis,
        oracle_analysis,
        correlations,
        jmeter_analysis,
        configuration,
        dashboard_summary,
    

    )
    final_results = {
    "llm_report": llm_report
}


# ==========================================================
# Report Generation
# ==========================================================


    reports = ReportGenerator().generate(

        run_id,          # <-- see note below

        llm_report,

        timeline,

        correlations

    )

    final_results["reports"] = reports

    print("this is final result line 481", final_results)

    return final_results

if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("INSIDE PERFORMANCE ANALYZER")
    logger.info("=" * 80) 
    results = run_analysis(
        "config/monitoring_config.yaml"
    )
    print("this is result on 492", results)
    logger.info("Performance Analyzer Completed Successfully")
    