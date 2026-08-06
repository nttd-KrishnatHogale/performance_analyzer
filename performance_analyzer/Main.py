# from core.config_manager import ConfigManager
from performance_analyzer.config import settings
from performance_analyzer.core.config_manager import ConfigManager
from performance_analyzer.data_sources.data_loader import dataLoader
# from data_sources.data_loader import dataLoader
from performance_analyzer.aggregation.aggregator import aggregate_all
from performance_analyzer.anomaly_detection.detector import detect_anomalies_and_patterns
from performance_analyzer.rule_engine.rule_engine import run_rule_engine_with_output
from performance_analyzer.utils.output_writer import save_detailed_output, generate_html_report
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

def print_actionable_output(final_results):

    for flow_id, data in final_results["flows"].items():

        print("\n" + "=" * 80)
        print(f"FLOW: {flow_id}")
        print("=" * 80)

        # ======================================================
        # ✅ SUMMARY
        # ======================================================
        summary = data.get("summary", {})
        print("\n✅ SUMMARY")
        print(f"Primary Bottleneck : {summary.get('primary_bottleneck')}")
        print(f"Confidence          : {summary.get('confidence')}")
        print(f"Total Issues        : {summary.get('total_issues_detected')}")

        # ======================================================
        # ✅ ROOT CAUSE CHAIN
        # ======================================================
        print("\n🔁 ROOT CAUSE CHAIN")

        chain = data.get("root_cause_chain", [])

        if chain:
            print(" → ".join(chain))
        else:
            print("No clear chain identified")

        # ======================================================
        # ✅ LAYER BREAKDOWN
        # ======================================================
        print("\n📊 LAYER-WISE BREAKDOWN")

        layers = data.get("layer_breakdown", {})

        for layer, issues in layers.items():

            print(f"\n--- {layer} ---")

            if not issues:
                print("No major issues")
                continue

            for i in issues:
                print(f"- {i['issue']} | {i['severity']} | Score: {i['score']}")
                print(f"  ➤ {i['detail']}")

        # ======================================================
        # ✅ EVIDENCE
        # ======================================================
        print("\n📌 SUPPORTING EVIDENCE")

        evidence = data.get("evidence", [])

        if not evidence:
            print("No evidence available")
        else:
            for e in evidence:
                print(f"- {e['cause']} (Score: {e['score']})")
                print(f"  ➤ {e['justification']}")

        # ======================================================
        # ✅ RECOMMENDATIONS
        # ======================================================
        print("\n✅ ACTIONABLE RECOMMENDATIONS")

        actions = data.get("recommendations", [])

        if not actions:
            print("No recommendations available")
        else:
            for idx, action in enumerate(actions, 1):
                print(f"{idx}. {action}")

        print("\n" + "=" * 80)

def print_short_output(final_results):

    for flow_id, data in final_results["flows"].items():

        print("=" * 60)
        print(f"FLOW: {flow_id}")
        print("=" * 60)

        layers = data.get("layer_breakdown", {})
        insights = data.get("evidence", [])
        recommendations = data.get("recommendations", [])
        summary = data.get("summary", {})

        # --------------------------------------------------
        # ✅ BOTTLENECKS
        # --------------------------------------------------
        print("\n🚨 BOTTLENECKS")

        found = False
        for layer, issues in layers.items():

            for i in issues:
                if i["severity"] == "HIGH":
                    print(f"- {i['issue']} ({layer})")
                    found = True

        if not found:
            print("- No major bottlenecks detected")

        # --------------------------------------------------
        # ✅ RISKS
        # --------------------------------------------------
        print("\n⚠️ RISKS")

        risks = []

        for layer, issues in layers.items():

            for i in issues:
                if i["severity"] == "MEDIUM":
                    risks.append(i["issue"])

        if risks:
            for r in set(risks):
                print(f"- {r}")
        else:
            print("- No significant risks")

        # --------------------------------------------------
        # ✅ ACTION ITEMS
        # --------------------------------------------------
        print("\n✅ ACTION ITEMS")

        if recommendations:
            for idx, r in enumerate(recommendations[:5], 1):
                print(f"{idx}. {r}")
        else:
            print("No actions required")

        # --------------------------------------------------
        # ✅ CONFIDENCE
        # --------------------------------------------------
        print(f"\n🎯 CONFIDENCE: {summary.get('confidence')}")
        print("Confidence High = Strong evidence. Act Immediately")
        print("Confidence Medium = Partial evidence. Observe")
        print("Confidence Weak = Weak evidence. Ignore")

        print("\n" + "=" * 60 + "\n")




 
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

        # Apache
        # for inst, df in server.get("apache", {}).items():

        #     print(f"\nApache Instance : {inst}")
        #     print(df.columns.tolist())
        for inst, df in server.get("apache", {}).items():

            print(f"\nApache Instance : {inst}")

            if df is not None:
                print(df.columns.tolist())
            else:
                print("No Apache Data")

        # Tomcat
        # for inst, df in server.get("tomcat", {}).items():

        #     print(f"\nTomcat Instance : {inst}")
        #     print(df.columns.tolist())

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

    # timeline = TimelineBuilder().build(
    #     metrics_collection,
    #     settings
    # )

    # for event in timeline:

    #     print(event)

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

    print("\nTimeline Data Keys")
    print(timeline_data.keys())

    print("\nApache")
    print(timeline_data["apache"])

    print("\nTomcat")
    print(timeline_data["tomcat"])

    print("\nOracle")
    print(timeline_data["oracle"])

    from performance_analyzer.apache.apache_analyzer import ApacheAnalyzer
    from performance_analyzer.tomcat.tomcat_analyzer import TomcatAnalyzer
    from performance_analyzer.oracle.oracle_analyzer import OracleAnalyzer

    # apache_analysis = ApacheAnalyzer().analyze(metrics_collection)

    # tomcat_analysis = TomcatAnalyzer().analyze(metrics_collection)

    # oracle_analysis = OracleAnalyzer().analyze(metrics_collection)
    from performance_analyzer.jmeter.jmeter_analyzer import JMeterAnalyzer

    jmeter_analysis = JMeterAnalyzer().analyze(
        metrics_collection["jmeter"]
    )
    from performance_analyzer.correlation.correlation_engine import CorrelationEngine

    # correlations = CorrelationEngine().analyze(metrics_collection)
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

  

    aggregated_data = aggregate_all(
        metrics_collection,
        config
    )

    analysis_results = detect_anomalies_and_patterns(
        aggregated_data
    )
    # from performance_analyzer.timeline.timeline_builder import TimelineBuilder

    # timeline = TimelineBuilder().build(
    #     metrics_collection,
    #     settings
    # )

    final_results = run_rule_engine_with_output(
                analysis_results
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



    # print("\n" + "="*80)
    # print("DATA SENT TO LLM")
    # print("="*80)

    # print("\nApache Analysis")
    # print(apache_analysis)

    # print("\nTomcat Analysis")
    # print(tomcat_analysis)

    # print("\nOracle Analysis")
    # print(oracle_analysis)

    # print("\nJMeter Analysis")
    # print(jmeter_analysis)

    # print("\nCorrelations")
    # print(correlations)

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

    final_results["llm_report"] = llm_report


    # ==========================================================
# Report Generation
# ==========================================================

    from performance_analyzer.report.report_generator import ReportGenerator

    reports = ReportGenerator().generate(

        run_id,          # <-- see note below

        llm_report,

        timeline,

        correlations

    )

    final_results["reports"] = reports

    save_detailed_output(final_results)

    generate_html_report(final_results)

    return final_results

if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("INSIDE PERFORMANCE ANALYZER")
    logger.info("=" * 80) 
    results = run_analysis(
        "config/monitoring_config.yaml"
    )
    logger.info("Performance Analyzer Completed Successfully")
    print_short_output(results)



    # # read configuration file
    # config = ConfigManager("config/monitoring_config.yaml")
    # #config.print_summary()
    # # load metric data
    # metrics_collection = dataLoader(config)
    # # print_sample_data(metrics_collection)
    
    # aggregated_data = aggregate_all(metrics_collection, config)

    # """ print("\n===== FLOW DATA =====")
    # for flow_id, df in aggregated_data["flows"].items():
    #     print(flow_id, df.shape if df is not None else "No data")

    # print("\n===== SERVER DATA =====")
    # for server, df in aggregated_data["servers"].items():
    #     print(server, df.shape if df is not None else "No data") """
    

    # analysis_results = detect_anomalies_and_patterns(aggregated_data)

    # # -----------------------------------
    # # DEBUG OUTPUT
    # # -----------------------------------
    # """ print("\n===== FLOW ANALYSIS =====")
    # print(json.dumps(analysis_results["flows"], indent=2)) """
    # """ for k, v in analysis_results["flows"].items():
    #     print(k, v) """

    # """ print("\n===== SERVER ANALYSIS =====")
    # print(json.dumps(analysis_results["servers"], indent=2)) """
    # """ for k, v in analysis_results["servers"].items():
    #     print(k, v) """
    

    
    # # STEP 5
    # final_results = run_rule_engine_with_output(analysis_results)

    # # -------------------------
    # # PRINT OUTPUT
    # # -------------------------
    # #print_actionable_output(final_results)
    # print_short_output(final_results)
    # save_detailed_output(final_results)
    # generate_html_report(final_results)

    # """ print("\n===== FINAL RCA =====")

    # for flow, result in final_results["flows"].items():

    #     print(f"\nFlow: {flow}")

    #     print("\nTop Causes:")
    #     for cause, score in result["ranking"]:
    #         print(f" - {cause}: {score}")

    #     print("\nInsights:")
    #     for i in result["insights"]:
    #         print(f" - {i['message']} (Score: {i['score']})") """

    
    
