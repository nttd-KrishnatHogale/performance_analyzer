# from core.config_manager import ConfigManager
from performance_analyzer.core.config_manager import ConfigManager
from performance_analyzer.data_sources.data_loader import dataLoader
# from data_sources.data_loader import dataLoader
from performance_analyzer.aggregation.aggregator import aggregate_all
from performance_analyzer.anomaly_detection.detector import detect_anomalies_and_patterns
from performance_analyzer.rule_engine.rule_engine import run_rule_engine_with_output
from performance_analyzer.utils.output_writer import save_detailed_output, generate_html_report
import json
from backend.utils.logger import Logger

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




 
def run_analysis(config_path):

    config = ConfigManager(config_path)

    metrics_collection = dataLoader(config)

    aggregated_data = aggregate_all(
        metrics_collection,
        config
    )

    analysis_results = detect_anomalies_and_patterns(
        aggregated_data
    )

    final_results = run_rule_engine_with_output(
        analysis_results
    )

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

    
    
