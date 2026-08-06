import pandas as pd


class MetricsSummary:

    # ==========================================================
    # Apache
    # ==========================================================

    @staticmethod
    def summarize_apache(apache):

        summary = {}

        for host, instances in apache.items():

            summary[host] = {}

            for instance, data in instances.items():

                result = {}

                # ----------------------------
                # Findings
                # ----------------------------

                result["findings"] = (
                    data.get("analysis", {}).get("findings", [])
                )

                # ----------------------------
                # Timeline
                # ----------------------------

                result["timeline"] = (
                    data.get("analysis", {}).get("timeline", [])
                )

                # ----------------------------
                # Throughput
                # ----------------------------

                throughput = data.get("throughput")

                if isinstance(throughput, pd.DataFrame) and not throughput.empty:

                    if "response_time" in throughput.columns:

                        result["response_time"] = {

                            "average": round(
                                float(throughput["response_time"].mean()), 2
                            ),

                            "max": round(
                                float(throughput["response_time"].max()), 2
                            ),

                            "min": round(
                                float(throughput["response_time"].min()), 2
                            ),

                            "p95": round(
                                float(
                                    throughput["response_time"].quantile(0.95)
                                ),
                                2,
                            ),

                        }

                # ----------------------------
                # Busy Workers
                # ----------------------------

                mod = data.get("modstatus")

                if isinstance(mod, pd.DataFrame) and not mod.empty:

                    if "busyworkers" in mod.columns:

                        peak = mod["busyworkers"].max()

                        avg = mod["busyworkers"].mean()

                        result["busy_workers"] = {

                            "average": round(float(avg), 2),

                            "peak": round(float(peak), 2),

                        }

                summary[host][instance] = result

        return summary

    # ==========================================================
    # Tomcat
    # ==========================================================

    @staticmethod
    def summarize_tomcat(tomcat):

        summary = {}

        for host, instances in tomcat.items():

            summary[host] = {}

            for instance, data in instances.items():

                result = {}

                result["findings"] = (
                    data.get("analysis", {}).get("findings", [])
                )

                result["timeline"] = (
                    data.get("analysis", {}).get("timeline", [])
                )

                # ----------------------------
                # Thread Pool
                # ----------------------------

                thread = data.get("thread")

                if isinstance(thread, pd.DataFrame) and not thread.empty:

                    if (
                        "used_thread_count" in thread.columns
                        and "max_thread_count" in thread.columns
                    ):

                        max_threads = thread["max_thread_count"].max()

                        peak_threads = thread["used_thread_count"].max()

                        util = 0

                        if max_threads > 0:

                            util = (peak_threads / max_threads) * 100

                        result["thread_pool"] = {

                            "max_threads": int(max_threads),

                            "peak_threads": int(peak_threads),

                            "average_threads": round(
                                float(thread["used_thread_count"].mean()), 2
                            ),

                            "utilization_percent": round(util, 2),

                        }

                # ----------------------------
                # JVM
                # ----------------------------

                jvm = data.get("jvm")

                if isinstance(jvm, pd.DataFrame) and not jvm.empty:

                    gc = {}

                    if "scavenge_count" in jvm.columns:

                        gc["gc_events"] = int(
                            jvm["scavenge_count"].max()
                        )

                    if "scavenge_time" in jvm.columns:

                        gc["gc_time"] = round(
                            float(jvm["scavenge_time"].max()), 2
                        )

                    if "gc_throughput" in jvm.columns:

                        gc["gc_throughput"] = round(
                            float(jvm["gc_throughput"].mean()), 2
                        )

                    if "heap_total" in jvm.columns:

                        gc["heap_peak"] = round(
                            float(jvm["heap_total"].max()), 2
                        )

                    result["jvm"] = gc

                # ----------------------------
                # JDBC Pool
                # ----------------------------

                ds = data.get("datasource")

                if isinstance(ds, pd.DataFrame) and not ds.empty:

                    jdbc = {}

                    if "max_connection_pool" in ds.columns:

                        jdbc["max_pool"] = int(
                            ds["max_connection_pool"].max()
                        )

                    if "used_connection_pool" in ds.columns:

                        jdbc["peak_used"] = int(
                            ds["used_connection_pool"].max()
                        )

                    result["jdbc"] = jdbc

                # ----------------------------
                # Sessions
                # ----------------------------

                session = data.get("session")

                if isinstance(session, pd.DataFrame) and not session.empty:

                    if "active_session_count" in session.columns:

                        result["sessions"] = {

                            "peak": int(
                                session["active_session_count"].max()
                            ),

                            "average": round(
                                float(
                                    session[
                                        "active_session_count"
                                    ].mean()
                                ),
                                2,
                            ),

                        }

                summary[host][instance] = result

        return summary

    # ==========================================================
    # Oracle
    # ==========================================================

    @staticmethod
    def summarize_oracle(oracle):

        summary = {}

        for host, instances in oracle.items():

            summary[host] = {}

            for instance, data in instances.items():

                result = {}

                result["findings"] = (
                    data.get("analysis", {}).get("findings", [])
                )

                result["timeline"] = (
                    data.get("analysis", {}).get("timeline", [])
                )

                result["top_sql"] = (
                    data.get("analysis", {}).get("top_sql", [])
                )

                result["plans"] = (
                    data.get("analysis", {}).get("plans", [])
                )

                raw = data.get("raw", {})

                db_summary = {}

                for table_name, df in raw.items():

                    if isinstance(df, pd.DataFrame):

                        db_summary[table_name] = {

                            "rows": len(df),

                            "columns": list(df.columns),

                        }

                result["database_summary"] = db_summary

                summary[host][instance] = result

        return summary

    # ==========================================================
    # JMeter
    # ==========================================================

    @staticmethod
    def summarize_jmeter(jmeter):

        if not isinstance(jmeter, dict):

            return {}

        summary = {

            "users": jmeter.get("total_users"),

            "ramp_up": jmeter.get("ramp_up"),

            "duration": jmeter.get("duration"),

            "loops": jmeter.get("loops"),

            "thread_groups": len(
                jmeter.get("thread_groups", [])
            ),

        }

        return summary