from anomaly_detection.metric_resolver import get_metric_columns
from anomaly_detection.metric_constants import *


# ============================================================
# Helper function
# ============================================================
def _check_corr(df, col1, col2, results, label):

    if col1 not in df or col2 not in df:
        return

    try:
        corr = df[[col1, col2]].corr().iloc[0, 1]
    except:
        return

    if corr is None:
        return

    if abs(corr) > 0.5:
        results["correlations"].append(
            f"{col1} ↔ {col2} | {label} (corr={corr:.2f})"
        )


# ============================================================
# MAIN CORRELATION ENGINE
# ============================================================
def detect_correlations(df, results):

    # ========================================================
    # RESOLVE ALL METRIC GROUPS
    # ========================================================
    latency_cols = get_metric_columns(df, "response_time") + \
                   get_metric_columns(df, "latency")

    cpu_cols = get_metric_columns(df, "cpu_usage")
    heap_cols = get_metric_columns(df, "heap")
    gc_count_cols = get_metric_columns(df, "full_count")
    gc_time_cols = get_metric_columns(df, "full_time")

    thread_cols = get_metric_columns(df, "thread")
    db_exec_cols = get_metric_columns(df, "elapsed_time")
    db_calls_cols = get_metric_columns(df, "executions")
    db_wait_cols = get_metric_columns(df, "time_waited")

    apache_worker_cols = get_metric_columns(df, "busyworkers")

    load_cols = get_metric_columns(df, "threads")  # JMeter
    conn_pool_cols = get_metric_columns(df, "connection_pool")
    session_cols = get_metric_columns(df, "session")
    memory_cols = get_metric_columns(df, "memory_pct")

    xmx_cols = get_metric_columns(df, "opt_mx")

    error_cols = get_metric_columns(df, "error")
    apache_status_cols = get_metric_columns(df, "apache_status")
    db_status_cols = get_metric_columns(df, "oracle_status")

    buffer_hit_cols = get_metric_columns(df, "buffer_hit")

    gc_scavenge_cols = get_metric_columns(df, "scavenge_count")
    old_gen_cols = get_metric_columns(df, "old")

    apache_latency_cols = get_metric_columns(df, "apache_response_time")

    # ========================================================
    # 1. LATENCY-DRIVEN CORRELATIONS
    # ========================================================

    for lat in latency_cols:

        for cpu in cpu_cols:
            _check_corr(df, cpu, lat, results,
                        "CPU bottleneck / Infra constraint")

        for gc in gc_count_cols:
            _check_corr(df, gc, lat, results,
                        "High GC frequency (memory pressure)")

        for gc in gc_time_cols:
            _check_corr(df, gc, lat, results,
                        "GC inefficiency / full GC pauses")

        for heap in heap_cols:
            _check_corr(df, heap, lat, results,
                        "Heap pressure / memory overuse")

        for th in thread_cols:
            _check_corr(df, th, lat, results,
                        "Thread pool bottleneck")

        for db in db_exec_cols:
            _check_corr(df, db, lat, results,
                        "DB performance bottleneck")

        for db in db_calls_cols:
            _check_corr(df, db, lat, results,
                        "DB overload / inefficient queries")

        for db in db_wait_cols:
            _check_corr(df, db, lat, results,
                        "DB contention (locks / IO)")

        for ap in apache_worker_cols:
            _check_corr(df, ap, lat, results,
                        "Apache capacity limit")

    # ✅ Heap / Xmx special case
    for heap in heap_cols:
        for xmx in xmx_cols:
            for lat in latency_cols:

                if heap in df and xmx in df:

                    ratio = df[heap] / df[xmx]

                    if ratio.mean() > 0.8:
                        _check_corr(df, heap, lat, results,
                                    "Heap saturation / insufficient Xmx")

    # ========================================================
    # 2. LOAD PROPAGATION
    # ========================================================

    for load in load_cols:

        for ap in apache_worker_cols:
            _check_corr(df, load, ap, results,
                        "Traffic-driven saturation (Web layer)")

        for lat in latency_cols:
            _check_corr(df, load, lat, results,
                        "Overall system capacity limit")

    for ap in apache_worker_cols:

        for lat in apache_latency_cols:
            _check_corr(df, ap, lat, results,
                        "Apache worker exhaustion")

        for th in thread_cols:
            _check_corr(df, ap, th, results,
                        "App layer capacity stress")

    for th in thread_cols:

        for db in db_calls_cols:
            _check_corr(df, th, db, results,
                        "Application inefficiency / load pressure")

    # ========================================================
    # 3. RESOURCE UTILIZATION
    # ========================================================

    for cpu in cpu_cols:
        for load in load_cols:
            _check_corr(df, cpu, load, results,
                        "CPU scales with traffic")

    for mem in memory_cols:
        for load in load_cols:
            _check_corr(df, mem, load, results,
                        "Memory leak / inefficient caching")

    for conn in conn_pool_cols:
        for lat in latency_cols:
            _check_corr(df, conn, lat, results,
                        "DB connection pool exhaustion")

    for sess in session_cols:
        for mem in memory_cols:
            _check_corr(df, sess, mem, results,
                        "Session leak / retention issue")

    for ap in apache_worker_cols:
        for lat in apache_latency_cols:
            _check_corr(df, ap, lat, results,
                        "Web server bottleneck")

    # ========================================================
    # 4. JVM INTERNAL BEHAVIOR
    # ========================================================

    for heap in heap_cols:
        for gc in gc_count_cols:
            _check_corr(df, heap, gc, results,
                        "Inefficient memory usage")

    for gc in gc_count_cols:
        for cpu in cpu_cols:
            _check_corr(df, gc, cpu, results,
                        "GC overhead causing CPU spikes")

    for gc in gc_time_cols:
        for lat in latency_cols:
            _check_corr(df, gc, lat, results,
                        "GC pauses affecting latency")

    for heap in heap_cols:
        for load in load_cols:
            _check_corr(df, heap, load, results,
                        "Memory pressure / allocation issues")

    for old in old_gen_cols:
        for sc in gc_scavenge_cols:
            _check_corr(df, old, sc, results,
                        "Improper heap tuning")

    # ========================================================
    # 5. DATABASE BEHAVIOR
    # ========================================================

    for db_exec in db_calls_cols:
        for db_time in db_exec_cols:
            _check_corr(df, db_exec, db_time, results,
                        "High query volume")

    for wait in db_wait_cols:
        for lat in latency_cols:
            _check_corr(df, wait, lat, results,
                        "DB contention (locks / IO)")

    for db_exec in db_calls_cols:
        for cpu in cpu_cols:
            _check_corr(df, db_exec, cpu, results,
                        "DB-heavy processing")

    for db_exec in db_calls_cols:
        for lat in latency_cols:
            _check_corr(df, db_exec, lat, results,
                        "Application inefficiency")

    for buf in buffer_hit_cols:
        for lat in latency_cols:
            _check_corr(df, buf, lat, results,
                        "Inefficient caching / poor indexing")

    # ========================================================
    # 6. FAILURE / ERROR CORRELATIONS
    # ========================================================

    for err in error_cols:
        for lat in latency_cols:
            _check_corr(df, err, lat, results,
                        "Application instability")

    for err in error_cols:
        for load in load_cols:
            _check_corr(df, err, load, results,
                        "Capacity breach")

    for ap_err in apache_status_cols:
        for lat in latency_cols:
            _check_corr(df, ap_err, lat, results,
                        "Web misconfiguration / overload")

    for db_err in db_status_cols:
        for lat in latency_cols:
            _check_corr(df, db_err, lat, results,
                        "DB instability")