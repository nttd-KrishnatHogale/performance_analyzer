from rule_engine.rule_definitions import evaluate_rules
from rule_engine.output_formatter import build_actionable_output

def rank_insights(insights):

    # Aggregate by cause
    scores = {}

    for i in insights:
        cause = i["cause"]
        scores[cause] = scores.get(cause, 0) + i["score"]

    # Sort descending
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return ranked


def analyze_entity(entity_analysis):

    insights = evaluate_rules(entity_analysis)

    ranking = rank_insights(insights)

    return {
        "insights": insights,
        "ranking": ranking
    }

""" def run_rule_engine(analysis_results):

    final_results = {
        "flows": {},
        "servers": {}
    }

    # ✅ FLOW LEVEL
    for flow_id, analysis in analysis_results["flows"].items():
        final_results["flows"][flow_id] = analyze_entity(analysis)

    # ✅ SERVER LEVEL
    for server_id, analysis in analysis_results["servers"].items():
        final_results["servers"][server_id] = analyze_entity(analysis)

    return final_results """


def run_rule_engine_with_output(analysis_results):

    final_results = {
        "flows": {},
        "servers": {}
    }

    # FLOWS
    for flow_id, analysis in analysis_results["flows"].items():

        rule_output = analyze_entity(analysis)

        final_results["flows"][flow_id] = build_actionable_output(
            flow_id, rule_output
        )

    # SERVERS
    for server_id, analysis in analysis_results["servers"].items():

        rule_output = analyze_entity(analysis)

        final_results["servers"][server_id] = build_actionable_output(
            server_id, rule_output
        )

    return final_results
