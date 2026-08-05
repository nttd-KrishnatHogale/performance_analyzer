from performance_analyzer.timeline.event_detector import EventDetector
from performance_analyzer.timeline.event_merger import EventMerger
from performance_analyzer.timeline.timeline_printer import TimelinePrinter
from performance_analyzer.apache.apache_analyzer import ApacheAnalyzer
from performance_analyzer.tomcat.tomcat_analyzer import TomcatAnalyzer
from performance_analyzer.oracle.oracle_analyzer import OracleAnalyzer
class TimelineBuilder:

    def __init__(self):

        self.detector = EventDetector()

        self.printer = TimelinePrinter()
        self.apache_analyzer = ApacheAnalyzer()
        self.tomcat_analyzer = TomcatAnalyzer()
        self.oracle_analyzer = OracleAnalyzer()

    def build(self, metrics_collection, settings):

        timeline = []
        apache_results = {}

        tomcat_results = {}

        oracle_results = {}

        for hostname, server in metrics_collection["servers"].items():

            # ---------------- CPU ----------------

            cpu = server.get("cpu")

            cpu_events = self.detector.detect(

                df=cpu,

                column="cpu_usage",

                threshold=settings.CPU_HIGH_THRESHOLD,

                component="Infrastructure",

                metric=f"CPU ({hostname})"
            )

            timeline.extend(cpu_events)

            # ---------------- Memory ----------------

            memory = server.get("memory")

            memory_events = self.detector.detect(

                df=memory,

                column="pct_used",

                threshold=settings.MEMORY_HIGH_THRESHOLD,

                component="Infrastructure",

                metric=f"Memory ({hostname})"
            )

            timeline.extend(memory_events)

        # ------------------------------------
        # Apache Analysis
        # ------------------------------------

            for instance, apache_df in server.get("apache", {}).items():

                if apache_df is None or apache_df.empty:
                    continue

                # Split merged dataframe
                modstatus_cols = [
                    "busyworkers",
                    "workerssum",
                    "scoreboard_count_cleanup",
                    "scoreboard_count_closing",
                    "scoreboard_count_dns",
                    "scoreboard_count_graceful",
                    "scoreboard_count_keepalive",
                    "scoreboard_count_log",
                    "scoreboard_count_openslot",
                    "scoreboard_count_read",
                    "scoreboard_count_reply",
                    "scoreboard_count_start",
                    "scoreboard_count_wait",
                ]

                throughput_cols = [
                    "path",
                    "response_time",
                    "status",
                    "size",
                ]

                modstatus_df = apache_df[
                    [c for c in modstatus_cols if c in apache_df.columns]
                ]

                throughput_df = apache_df[
                    [c for c in throughput_cols if c in apache_df.columns]
                ]

                # apache_analysis = self.apache_analyzer.analyze(
                #     modstatus_df,
                #     throughput_df,
                #     settings
                # )

                # timeline.extend(apache_analysis["timeline"])
                apache_analysis = self.apache_analyzer.analyze(
                modstatus_df,
                throughput_df,
                settings
            )

                # apache_results[(hostname, instance)] = apache_analysis
                apache_results.setdefault(hostname, {})
                apache_results[hostname][instance] = {
                    "analysis": apache_analysis,
                    "modstatus": modstatus_df,
                    "throughput": throughput_df,
                }
                timeline.extend(apache_analysis["timeline"])

        # for instance, tomcat in server["tomcat"].items():

        #     analysis = self.tomcat_analyzer.analyze(

        #         tomcat["jvm"],

        #         tomcat["thread"],

        #         tomcat["datasource"],

        #         tomcat["session"],

        #         settings

        #     )

        #     timeline.extend(analysis["timeline"])

        # ------------------------------------
        # Tomcat Analysis
        # ------------------------------------
            print("\n" + "=" * 80)
            print("RAW TOMCAT DATA")
            print("=" * 80)

            for instance, tomcat_df in server.get("tomcat", {}).items():

                if tomcat_df is None or tomcat_df.empty:
                    continue

                # JVM columns
                jvm_cols = [
                       "heap_total",
                        "gc_throughput",
                        "full_count",
                        "full_time",
                        "eden",
                        "old",
                        "survivor",
                        "scavenge_count",
                        "scavenge_time",
                        "opt_ms",
                        "opt_mx",
                    ]

                # Thread Pool columns
                thread_cols = [
                        "used_thread_count",
                        "max_thread_count",
                        "thread_name",
                    ]

                # JDBC Pool columns
                datasource_cols = [
                        "used_connection_pool",
                        "max_connection_pool",
                        "ds_name",
                    ]

                # Session columns
                session_cols = [
                        "active_session_count",
                        "max_session_count",
                    ]

                jvm_df = tomcat_df[
                        [c for c in jvm_cols if c in tomcat_df.columns]
                    ]

                thread_df = tomcat_df[
                        [c for c in thread_cols if c in tomcat_df.columns]
                    ]   

                datasource_df = tomcat_df[
                        [c for c in datasource_cols if c in tomcat_df.columns]
                    ]

                session_df = tomcat_df[
                        [c for c in session_cols if c in tomcat_df.columns]
                    ]

                # analysis = self.tomcat_analyzer.analyze(

                #         jvm_df,
                #         # tomcat_df,
                #         thread_df,

                #         datasource_df,

                #         session_df,

                #         settings

                #     )
                print("\nInstance:", instance)

                if tomcat_df is None:
                    print("DataFrame is None")
                    continue

                print("Rows:", len(tomcat_df))
                print("Columns:", tomcat_df.columns.tolist())
                print(tomcat_df.head())

                analysis = self.tomcat_analyzer.analyze(
                    jvm_df,
                    thread_df,
                    datasource_df,
                    session_df,
                    settings
                )
                print("\nTomcat Analyzer Output")
                print(analysis)
                # tomcat_results[(hostname, instance)] = analysis
                tomcat_results.setdefault(hostname, {})
                # tomcat_results[hostname][instance] = analysis
                tomcat_results[hostname][instance] = {
                    "analysis": analysis,
                    "jvm": jvm_df,
                    "thread": thread_df,
                    "datasource": datasource_df,
                    "session": session_df,
                }

                timeline.extend(analysis["timeline"])

                print("\n" + "=" * 80)
                print("RAW ORACLE DATA")
                print("=" * 80)

            for sid, oracle_data in server["oracle"].items():

                # oracle_analysis = self.oracle_analyzer.analyze(

                #             oracle_data,

                #             settings

                #         )

                print("\nSID:", sid)

                for table, df in oracle_data.items():

                    print("\nTable:", table)

                    if df is None:
                        print("None")
                        continue

                    print("Rows:", len(df))
                    print(df.head())
                
                oracle_analysis = self.oracle_analyzer.analyze(
                    oracle_data,
                    settings
                )
                print("\nOracle Analyzer Output")
                print(oracle_analysis)
                # oracle_results[(hostname, sid)] = oracle_analysis
                oracle_results.setdefault(hostname, {})
                # oracle_results[hostname][sid] = oracle_analysis
                oracle_results[hostname][sid] = {
                    "analysis": oracle_analysis,
                    "raw": oracle_data,
                }

                timeline.extend(oracle_analysis["timeline"])

        timeline = EventMerger().merge(timeline)

        self.printer.print(timeline)

        return {
            "timeline": timeline,
            "apache": apache_results,
            "tomcat": tomcat_results,
            "oracle": oracle_results,
}