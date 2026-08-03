from performance_analyzer.apache.apache_metrics import ApacheMetrics
from performance_analyzer.apache.apache_rules import ApacheFinding

from performance_analyzer.timeline.event_detector import EventDetector


class ApacheAnalyzer:

    def __init__(self):

        self.metrics = ApacheMetrics()

        self.detector = EventDetector()

    def analyze(

        self,

        modstatus_df,

        throughput_df,

        settings

    ):

        findings=[]

        timeline=[]

        # ------------------------------------------------

        # Worker Utilization

        # ------------------------------------------------

        workers=self.metrics.worker_utilization(modstatus_df)

        if workers is not None:

            events=self.detector.detect(

                workers,

                column="worker_utilization",

                threshold=settings.APACHE_WORKER_UTIL_THRESHOLD,

                component="Apache",

                metric="Worker Utilization"

            )

            timeline.extend(events)

            if events:

                findings.append(

                    ApacheFinding(

                        finding="Apache Worker Saturation",

                        severity="HIGH",

                        score=90,

                        description="Apache workers became saturated.",

                        recommendation="Increase MaxRequestWorkers or tune KeepAlive.",

                        evidence={

                            "peak":

                            workers["worker_utilization"].max()

                        }

                    )

                )

        # ------------------------------------------------

        # Latency

        # ------------------------------------------------

        latency=self.metrics.latency(throughput_df)

        if latency is not None:

            events=self.detector.detect(

                latency,

                column="latency",

                threshold=settings.APACHE_LATENCY_THRESHOLD,

                component="Apache",

                metric="Response Time"

            )

            timeline.extend(events)

            if events:

                findings.append(

                    ApacheFinding(

                        finding="Apache Latency",

                        severity="HIGH",

                        score=85,

                        description="Apache response time increased.",

                        recommendation="Investigate backend response delay.",

                        evidence={

                            "peak":

                            latency["latency"].max()

                        }

                    )

                )

        # ------------------------------------------------

        # Error Rate

        # ------------------------------------------------

        errors=self.metrics.error_rate(throughput_df)

        if errors is not None:

            errors["error_rate"]=(

                errors["errors"]/

                errors["total"]

            )*100

            events=self.detector.detect(

                errors,

                column="error_rate",

                threshold=settings.APACHE_ERROR_THRESHOLD,

                component="Apache",

                metric="HTTP Error Rate"

            )

            timeline.extend(events)

            if events:

                findings.append(

                    ApacheFinding(

                        finding="HTTP Errors",

                        severity="HIGH",

                        score=95,

                        description="Apache returned many HTTP 5xx errors.",

                        recommendation="Inspect Tomcat or backend failures.",

                        evidence={

                            "peak":

                            errors["error_rate"].max()

                        }

                    )

                )

        return {

            "timeline":timeline,

            "findings":findings
        }