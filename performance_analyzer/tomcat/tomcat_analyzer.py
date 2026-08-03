from performance_analyzer.tomcat.tomcat_metrics import TomcatMetrics
from performance_analyzer.tomcat.tomcat_rules import TomcatFinding

from performance_analyzer.timeline.event_detector import EventDetector


class TomcatAnalyzer:

    def __init__(self):

        self.metrics = TomcatMetrics()

        self.detector = EventDetector()

    def analyze(

        self,

        jvm_df,

        thread_df,

        ds_df,

        session_df,

        settings

    ):

        findings = []

        timeline = []

        # --------------------------
        # Heap
        # --------------------------

        heap = self.metrics.heap_usage(jvm_df)

        if heap is not None:

            events = self.detector.detect(

                heap,

                column="heap_used_pct",

                threshold=settings.TOMCAT_HEAP_USAGE_THRESHOLD,

                component="Tomcat",

                metric="Heap Usage"

            )

            timeline.extend(events)

            if events:

                findings.append(

                    TomcatFinding(

                        finding="Heap Pressure",

                        severity="HIGH",

                        score=90,

                        description="Heap utilization is high.",

                        recommendation="Increase JVM heap or investigate object retention.",

                        evidence={

                            "peak":heap["heap_used_pct"].max()

                        }

                    )

                )

        # --------------------------
        # GC
        # --------------------------

        gc = self.metrics.gc(jvm_df)

        if gc is not None:

            events = self.detector.detect(

                gc,

                column="scavenge_time",

                threshold=settings.TOMCAT_GC_TIME_THRESHOLD,

                component="Tomcat",

                metric="GC Time"

            )

            timeline.extend(events)

            if events:

                findings.append(

                    TomcatFinding(

                        finding="GC Pause",

                        severity="MEDIUM",

                        score=82,

                        description="Garbage Collection pause increased.",

                        recommendation="Tune JVM or increase heap.",

                        evidence={

                            "peak":gc["scavenge_time"].max()

                        }

                    )

                )

        # --------------------------
        # Threads
        # --------------------------

        threads = self.metrics.thread_utilization(thread_df)

        if threads is not None:

            events = self.detector.detect(

                threads,

                column="thread_utilization",

                threshold=settings.TOMCAT_THREAD_UTIL_THRESHOLD,

                component="Tomcat",

                metric="Thread Pool"

            )

            timeline.extend(events)

            if events:

                findings.append(

                    TomcatFinding(

                        finding="Thread Saturation",

                        severity="HIGH",

                        score=93,

                        description="Tomcat thread pool is nearly exhausted.",

                        recommendation="Increase maxThreads or optimize request handling.",

                        evidence={

                            "peak":threads["thread_utilization"].max()

                        }

                    )

                )

        # --------------------------
        # JDBC Pool
        # --------------------------

        jdbc = self.metrics.jdbc_pool(ds_df)

        if jdbc is not None:

            events = self.detector.detect(

                jdbc,

                column="jdbc_utilization",

                threshold=settings.TOMCAT_DB_CONN_THRESHOLD,

                component="Tomcat",

                metric="JDBC Pool"

            )

            timeline.extend(events)

            if events:

                findings.append(

                    TomcatFinding(

                        finding="JDBC Pool Saturation",

                        severity="HIGH",

                        score=95,

                        description="Database connection pool is saturated.",

                        recommendation="Increase maxActive or optimize SQL.",

                        evidence={

                            "peak":jdbc["jdbc_utilization"].max()

                        }

                    )

                )

        # --------------------------
        # Sessions
        # --------------------------

        sessions = self.metrics.sessions(session_df)

        if (

            sessions is not None and

            "activeSessions" in sessions.columns

        ):

            peak = sessions["activeSessions"].max()

            findings.append(

                TomcatFinding(

                    finding="Session Growth",

                    severity="LOW",

                    score=55,

                    description="Application sessions increased.",

                    recommendation="Monitor session growth.",

                    evidence={

                        "peak":peak

                    }

                )

            )

        return {

            "timeline":timeline,

            "findings":findings

        }