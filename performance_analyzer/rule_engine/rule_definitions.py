def evaluate_rules(analysis):

    insights = []

    correlations = analysis.get("correlations", [])
    patterns = analysis.get("patterns", [])
    anomalies = analysis.get("anomalies", [])

    def match(keyword):
        return any(keyword.lower() in c.lower() for c in correlations)

    # ============================================================
    # RULE 1–4: CPU / MEMORY
    # ============================================================

    # RULE 1: CPU + Latency
    if match("CPU") and match("latency"):
        insights.append({
            "cause": "CPU Bottleneck",
            "message": "CPU usage is high and impacting latency (CPU limiting performance)",
            "category": "bottlenecks",
            "score": 80
        })

    # RULE 2: CPU sustained
    if any("cpu" in p.lower() for p in patterns):
        insights.append({
            "cause": "CPU Resource Pressure",
            "message": "CPU utilization is continuously high (CPU resource pressure)",
            "category": "resource_issues",
            "score": 60
        })

    # RULE 3: Memory + Latency
    if match("memory") and match("latency"):
        insights.append({
            "cause": "Memory Bottleneck",
            "message": "Memory usage is high and impacting latency",
            "category": "resource_issues",
            "score": 75
        })

    # RULE 4: Memory trend
    if any("memory" in p.lower() for p in patterns):
        insights.append({
            "cause": "Memory Leak",
            "message": "Memory usage is continuously increasing (possible leak)",
            "category": "resource_issues",
            "score": 70
        })

    # ============================================================
    # RULE 5–8: APACHE
    # ============================================================

    # RULE 5
    if match("Apache capacity") or match("busyworkers"):
        insights.append({
            "cause": "Apache Bottleneck",
            "message": "Apache Server latency high with worker saturation (web saturation)",
            "category": "bottlenecks",
            "score": 80
        })

    # RULE 6
    if match("Apache pressure"):
        insights.append({
            "cause": "Apache Resource Pressure",
            "message": "Apache worker utilization sustained high",
            "category": "resource_issues",
            "score": 60
        })

    # RULE 7
    if match("error"):
        insights.append({
            "cause": "Apache Stability Issue",
            "message": "Apache HTTP errors observed impacting stability",
            "category": "stability_issues",
            "score": 75
        })

    # RULE 8
    if match("Apache") and match("latency"):
        insights.append({
            "cause": "Apache Performance Limit",
            "message": "Apache throughput increase causing latency (web scaling issue)",
            "category": "performance_limits",
            "score": 70
        })

    # ============================================================
    # RULE 9–19: TOMCAT (JVM)
    # ============================================================

    # RULE 9
    if match("heap") and match("latency"):
        insights.append({
            "cause": "Tomcat Heap Bottleneck",
            "message": "Tomcat JVM heap usage impacting latency",
            "category": "bottlenecks",
            "score": 80
        })

    # RULE 10
    if match("Heap saturation"):
        insights.append({
            "cause": "Tomcat Heap Near Max",
            "message": "Heap nearing maximum (Xmx)",
            "category": "resource_issues",
            "score": 70
        })

    # RULE 11
    if match("heap"):
        insights.append({
            "cause": "Heap Growth Trend",
            "message": "Heap usage increasing continuously",
            "category": "resource_issues",
            "score": 65
        })

    # RULE 12
    if match("GC") and match("time"):
        insights.append({
            "cause": "High GC Time",
            "message": "Garbage collection time is high",
            "category": "resource_issues",
            "score": 65
        })

    # RULE 13
    if match("GC") and match("count"):
        insights.append({
            "cause": "High GC Frequency",
            "message": "Garbage collection count is high",
            "category": "resource_issues",
            "score": 65
        })

    # RULE 14
    if match("GC") and match("latency"):
        insights.append({
            "cause": "GC Impact",
            "message": "Garbage collection affecting latency",
            "category": "performance_limits",
            "score": 75
        })

    # RULE 15
    if match("thread") and match("latency"):
        insights.append({
            "cause": "Tomcat Thread Bottleneck",
            "message": "Thread utilization high causing latency",
            "category": "bottlenecks",
            "score": 85
        })

    # RULE 16
    if match("thread"):
        insights.append({
            "cause": "Thread Saturation",
            "message": "Thread utilization sustained high",
            "category": "resource_issues",
            "score": 65
        })

    # RULE 17
    if match("connection pool"):
        insights.append({
            "cause": "DB Connection Pool Bottleneck",
            "message": "Database connection pool utilization high",
            "category": "bottlenecks",
            "score": 80
        })

    # RULE 18
    if match("connection"):
        insights.append({
            "cause": "Connection Pool Pressure",
            "message": "DB connection pool sustained high utilization",
            "category": "resource_issues",
            "score": 65
        })

    # RULE 19
    if match("session"):
        insights.append({
            "cause": "Session Growth",
            "message": "Active session count increasing",
            "category": "observations",
            "score": 40
        })

    # ============================================================
    # RULE 20–30: CROSS LAYER
    # ============================================================

    # RULE 20
    if match("apache") and match("latency"):
        insights.append({
            "cause": "End-to-End Latency",
            "message": "Apache + Application latency impacting performance",
            "category": "performance_limits",
            "score": 70
        })

    # RULE 21
    if match("GC") and match("CPU"):
        insights.append({
            "cause": "GC CPU Impact",
            "message": "GC activity increasing CPU usage",
            "category": "resource_issues",
            "score": 70
        })

    # RULE 22
    if match("heap") and match("load"):
        insights.append({
            "cause": "Heap Load Scaling",
            "message": "Heap usage increasing with load",
            "category": "observations",
            "score": 40
        })

    # RULE 23
    if match("heap") and match("latency"):
        insights.append({
            "cause": "Heap Performance Impact",
            "message": "Heap usage contributing to latency",
            "category": "performance_limits",
            "score": 70
        })

    # RULE 24
    if match("load") and match("latency"):
        insights.append({
            "cause": "Load Driven Latency",
            "message": "System latency increases with load",
            "category": "performance_limits",
            "score": 75
        })

    # RULE 25
    if match("Apache") and match("load"):
        insights.append({
            "cause": "Apache Load Limit",
            "message": "Apache reaching performance limit under load",
            "category": "performance_limits",
            "score": 70
        })

    # RULE 26
    if match("GC") and match("latency"):
        insights.append({
            "cause": "GC Bottleneck",
            "message": "High GC causing latency bottleneck",
            "category": "bottlenecks",
            "score": 80
        })

    # RULE 27
    if match("CPU") and match("GC") and match("latency"):
        insights.append({
            "cause": "CPU-GC Combined Bottleneck",
            "message": "CPU + GC jointly causing latency",
            "category": "bottlenecks",
            "score": 85
        })

    # RULE 28
    if match("worker") and match("latency"):
        insights.append({
            "cause": "Apache Worker Bottleneck",
            "message": "Apache workers saturated impacting latency",
            "category": "bottlenecks",
            "score": 80
        })

    # RULE 29
    if match("thread") and match("apache"):
        insights.append({
            "cause": "Thread Impact on Apache",
            "message": "Tomcat Threads impacting Apache latency",
            "category": "bottlenecks",
            "score": 75
        })

    # RULE 30
    if match("connection") and match("latency"):
        insights.append({
            "cause": "Connection Pool Latency",
            "message": "DB connection pool impacting latency",
            "category": "bottlenecks",
            "score": 80
        })

    # ============================================================
    # RULE 31–47: ORACLE DATABASE
    # ============================================================

    # RULE 31
    if match("DB execution"):
        insights.append({
            "cause": "Database Execution High",
            "message": "Oracle DB execution time is high",
            "category": "resource_issues",
            "score": 70
        })

    # RULE 32
    if match("DB contention"):
        insights.append({
            "cause": "Database Wait Contention",
            "message": "Oracle DB wait time is high",
            "category": "resource_issues",
            "score": 75
        })

    # RULE 33
    if match("SQL execution"):
        insights.append({
            "cause": "Database Load High",
            "message": "High SQL execution volume",
            "category": "performance_limits",
            "score": 70
        })

    # RULE 34
    if match("DB execution") and "sustained":
        insights.append({
            "cause": "Sustained DB Load",
            "message": "Oracle DB execution time sustained high",
            "category": "resource_issues",
            "score": 75
        })

    # RULE 35
    if match("DB") and match("latency"):
        insights.append({
            "cause": "DB Latency Impact",
            "message": "Oracle DB affecting application latency",
            "category": "performance_limits",
            "score": 80
        })

    # RULE 36
    if match("DB") and match("load"):
        insights.append({
            "cause": "DB Load Scaling",
            "message": "Database load increases with traffic",
            "category": "observations",
            "score": 40
        })

    # RULE 37
    if match("wait") and match("latency"):
        insights.append({
            "cause": "DB Wait Impact",
            "message": "DB wait causing latency",
            "category": "performance_limits",
            "score": 80
        })

    # RULE 38
    if match("DB") and match("Apache"):
        insights.append({
            "cause": "DB → Apache Impact",
            "message": "Database latency impacting Apache",
            "category": "performance_limits",
            "score": 80
        })

    # RULE 39
    if match("PGA"):
        insights.append({
            "cause": "Oracle PGA Memory Pressure",
            "message": "Oracle PGA memory usage high",
            "category": "resource_issues",
            "score": 65
        })

    # RULE 40
    if match("SGA"):
        insights.append({
            "cause": "Oracle SGA Memory Pressure",
            "message": "Oracle SGA memory usage high",
            "category": "resource_issues",
            "score": 65
        })

    # RULE 41
    if match("DB execution") and match("latency"):
        insights.append({
            "cause": "Database Execution Bottleneck",
            "message": "DB execution directly causing latency",
            "category": "bottlenecks",
            "score": 85
        })

    # RULE 42
    if match("DB wait") and match("latency"):
        insights.append({
            "cause": "Database Wait Bottleneck",
            "message": "DB wait contention causing latency",
            "category": "bottlenecks",
            "score": 85
        })

    # RULE 43
    if match("DB calls") and match("latency"):
        insights.append({
            "cause": "Database Calls Bottleneck",
            "message": "High DB calls causing latency",
            "category": "bottlenecks",
            "score": 80
        })

    # RULE 44
    if match("DB") and match("apache") and match("thread"):
        insights.append({
            "cause": "End-to-End DB → App → Web Chain",
            "message": "Oracle → Tomcat → Apache chain bottleneck detected",
            "category": "bottlenecks",
            "score": 95
        })

    # RULE 45
    if match("CPU") and match("DB"):
        insights.append({
            "cause": "CPU + Database Bottleneck",
            "message": "CPU and Oracle DB jointly causing latency",
            "category": "bottlenecks",
            "score": 90
        })

    # RULE 46
    if match("Apache") and match("DB"):
        insights.append({
            "cause": "Apache + Database Performance Issue",
            "message": "Apache and Oracle DB combined performance degradation",
            "category": "performance_limits",
            "score": 80
        })

    # RULE 47
    if match("thread") and match("DB"):
        insights.append({
            "cause": "Thread + Database Bottleneck",
            "message": "Tomcat threads waiting on DB causing bottleneck",
            "category": "bottlenecks",
            "score": 85
        })

    return insights
