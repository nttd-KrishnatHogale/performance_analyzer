from performance_analyzer.utils.json_utils import make_json_safe
from performance_analyzer.oracle.oracle_metrics import OracleMetrics
from performance_analyzer.oracle.oracle_rules import OracleFinding
from performance_analyzer.oracle.sql_plan_parser import SQLPlanParser

from dataclasses import asdict

class OracleAnalyzer:

    def __init__(self):

        self.metrics=OracleMetrics()

        self.plan_parser=SQLPlanParser()

    def analyze(

        self,

        oracle_data,

        settings

    ):

        findings=[]

        timeline=[]

        sql_stats=oracle_data.get("sql_stats")

        timed=oracle_data.get("timed")

        efficiency=oracle_data.get("efficiency")

        counts=oracle_data.get("count_stats")

        plans=oracle_data.get("plan")

        # -------------------------------------

        # Top SQL

        # -------------------------------------

        top_sql=self.metrics.top_elapsed_sql(sql_stats)

        if top_sql is not None:

            row=top_sql.iloc[0]

            elapsed=float(row["elapsed_time"])

            if elapsed>settings.DB_EXEC_TIME_THRESHOLD:

                findings.append(

                    OracleFinding(

                        finding="Slow SQL",

                        severity="HIGH",

                        score=95,

                        description="High SQL elapsed time detected.",

                        recommendation="Tune SQL or create indexes.",

                        evidence={

                            "sql_id":str(row["sql_id"]),

                            "elapsed":float(row["elapsed_time"]),

                            "sql":str(row["sql_text"])

                        }

                    )

                )

        # -------------------------------------

        # DB CPU

        # -------------------------------------

        cpu=self.metrics.top_cpu_sql(timed)

        if cpu is not None:

            peak=float(cpu["db_cpu"].max())

            findings.append(

                OracleFinding(

                    finding="High Database CPU",

                    severity="MEDIUM",

                    score=80,

                    description="Database CPU utilization increased.",

                    recommendation="Investigate expensive SQL.",

                    evidence={

                        "peak":peak

                    }

                )

            )

        # -------------------------------------

        # Wait Events

        # -------------------------------------

        waits=self.metrics.top_waits(efficiency)

        if waits is not None:

            findings.append(

                OracleFinding(

                    finding="Database Wait Events",

                    severity="MEDIUM",

                    score=78,

                    description="Database wait events observed.",

                    recommendation="Analyze wait classes.",

                    evidence={

                        "rows":len(waits)

                    }

                )

            )

        # -------------------------------------

        # Executions

        # -------------------------------------

        execution=self.metrics.execution_rate(sql_stats)

        if execution is not None:

            peak=float(execution["executions"].max())

            findings.append(

                OracleFinding(

                    finding="High SQL Execution",

                    severity="LOW",

                    score=60,

                    description="SQL execution frequency increased.",

                    recommendation="Verify repetitive SQL.",

                    evidence={

                        "peak":peak

                    }

                )

            )

        # -------------------------------------

        # Execution Plans

        # -------------------------------------

        # parsed_plans=self.plan_parser.parse(plans)
        parsed_plans = make_json_safe(self.plan_parser.parse(plans))

        for plan in parsed_plans:

            p=plan["plan"].upper()

            if "FULL" in p:

                findings.append(

                    OracleFinding(

                        finding="Full Table Scan",

                        severity="HIGH",

                        score=98,

                        description="Execution plan contains FULL TABLE SCAN.",

                        recommendation="Create index or rewrite SQL.",

                        evidence=plan

                    )

                )

            if "HASH JOIN" in p:

                findings.append(

                    OracleFinding(

                        finding="Hash Join",

                        severity="MEDIUM",

                        score=80,

                        description="Hash Join detected.",

                        recommendation="Review join strategy.",

                        evidence=plan

                    )

                )


        # top_sql_records = []

        # if top_sql is not None:

        #     top_sql = top_sql.copy()

        #     for col in top_sql.columns:

        #         top_sql[col] = top_sql[col].apply(
        #             lambda x: x.item() if hasattr(x, "item") else x
        #         )

        #     top_sql_records = top_sql.to_dict(orient="records")
        return make_json_safe({
            "timeline": timeline,
            "findings": [asdict(f) for f in findings],
            "top_sql": (
                top_sql.to_dict(orient="records")
                if top_sql is not None else []
            ),
            "plans": parsed_plans
        })
        # return {
        #     "timeline": timeline,
        #     "findings": [asdict(f) for f in findings],
        #     "top_sql": top_sql_records,
        #     "plans": parsed_plans
        # }
        # return {

        #     "timeline":timeline,

        #     "findings":findings,

        #     "top_sql":top_sql,

        #     "plans":parsed_plans

        # }