def build_actionable_output(entity_id, rule_output):

    insights = rule_output["insights"]
    ranking = rule_output["ranking"]

    # ============================================================
    # 1. EXECUTIVE SUMMARY
    # ============================================================
    primary_cause = ranking[0][0] if ranking else "No major issue detected"
    confidence = "HIGH" if ranking and ranking[0][1] > 80 else "MEDIUM"

    summary = {
        "entity": entity_id,
        "primary_bottleneck": primary_cause,
        "confidence": confidence,
        "total_issues_detected": len(insights)
    }

    # ============================================================
    # 2. ROOT CAUSE CHAIN (DERIVED FROM INSIGHTS)
    # ============================================================
    chain = []

    # Map patterns of causality
    if any("CPU" in i["cause"] for i in insights):
        chain.append("CPU Usage ↑")

    if any("GC" in i["cause"] for i in insights):
        chain.append("GC Activity ↑")

    if any("Thread" in i["cause"] for i in insights):
        chain.append("Tomcat Threads ↑")

    if any("Database" in i["cause"] for i in insights):
        chain.append("Oracle DB Load ↑")

    if any("Apache" in i["cause"] for i in insights):
        chain.append("Apache Load ↑")

    if any("latency" in i["message"].lower() for i in insights):
        chain.append("Latency ↑ (User Impact)")

    # ============================================================
    # 3. LAYER-WISE BREAKDOWN
    # ============================================================
    layers = {
        "Infrastructure": [],
        "Web (Apache)": [],
        "Application (Tomcat)": [],
        "Database (Oracle)": []
    }

    for i in insights:

        cause = i["cause"]
        msg = i["message"]
        score = i["score"]

        entry = {
            "issue": cause,
            "detail": msg,
            "severity": "HIGH" if score > 80 else "MEDIUM" if score > 60 else "LOW",
            "score": score
        }

        if "CPU" in cause or "Memory" in cause:
            layers["Infrastructure"].append(entry)

        elif "Apache" in cause:
            layers["Web (Apache)"].append(entry)

        elif "Tomcat" in cause or "Thread" in cause or "Heap" in cause:
            layers["Application (Tomcat)"].append(entry)

        elif "Database" in cause or "DB" in cause:
            layers["Database (Oracle)"].append(entry)

    # ============================================================
    # 4. SUPPORTING EVIDENCE (FROM RULES)
    # ============================================================
    evidence = []
    for i in insights:
        evidence.append({
            "cause": i["cause"],
            "justification": i["message"],
            "score": i["score"]
        })

    # ============================================================
    # 5. ACTIONABLE RECOMMENDATIONS
    # ============================================================
    actions = []

    for i in insights:

        cause = i["cause"]

        if "CPU" in cause:
            actions.append("Optimize CPU usage or scale infrastructure")

        if "Memory" in cause:
            actions.append("Check for memory leaks and optimize heap usage")

        if "Heap" in cause:
            actions.append("Increase JVM heap (Xmx) or optimize memory allocation")

        if "GC" in cause:
            actions.append("Tune GC settings or reduce object creation")

        if "Thread" in cause:
            actions.append("Increase Tomcat thread pool or optimize request processing")

        if "Apache" in cause:
            actions.append("Increase Apache worker capacity or tune configs")

        if "Database" in cause or "DB" in cause:
            actions.append("Optimize SQL queries and improve DB performance")

        if "Connection Pool" in cause:
            actions.append("Increase DB connection pool or fix connection leaks")

    # Remove duplicates
    actions = list(set(actions))

    # ============================================================
    # FINAL OUTPUT
    # ============================================================
    return {
        "summary": summary,
        "root_cause_chain": chain,
        "layer_breakdown": layers,
        "evidence": evidence,
        "recommendations": actions
    }