import pandas as pd


class CorrelationRules:

    def cpu_vs_tomcat(self, cpu, tomcat):

        if cpu is None or tomcat is None:
            return None

        if cpu.empty or tomcat.empty:
            return None

        # df = pd.concat(
        #     [
        #         cpu["cpu_usage"],
        #         tomcat["thread_utilization"]
        #     ],
        #     axis=1
        # ).dropna()

        # Create thread utilization if it doesn't exist
        if "thread_utilization" not in tomcat.columns:

            if (
                "used_thread_count" not in tomcat.columns or
                "max_thread_count" not in tomcat.columns
            ):
                return None

            tomcat = tomcat.copy()

            tomcat["thread_utilization"] = (
                tomcat["used_thread_count"] /
                tomcat["max_thread_count"]
            ) * 100

        df = pd.concat(
            [
                cpu["cpu_usage"],
                tomcat["thread_utilization"]
            ],
            axis=1
        ).dropna()

        if len(df) < 5:
            return None

        corr = df.corr().iloc[0,1]

        if corr > 0.70:

            return {

                "source":"CPU",

                "target":"Tomcat Threads",

                "relation":"CPU saturation increasing Tomcat thread utilization",

                "confidence":round(corr,2),

                "evidence":[
                    f"Correlation={corr:.2f}"
                ]
            }

        return None

    ###########################################################

    def tomcat_vs_db(self, tomcat, oracle):

        if tomcat is None:
            return None

        if oracle is None:
            return None

        if tomcat.empty:
            return None

        timed = oracle.get("timed")

        if timed is None:

            return None

        if timed.empty:

            return None

        # df = pd.concat(

        #     [

        #         tomcat["jdbc_pool_used"],

        #         timed["elapsed_time"]

        #     ],

        #     axis=1

        # ).dropna()

        df = pd.concat(
                [
                    tomcat["jdbc_utilization"],
                    timed["elapsed_time"]
                ],
                axis=1
            ).dropna()

        if len(df)<5:

            return None

        corr=df.corr().iloc[0,1]

        if corr>0.70:

            return {

                "source":"Tomcat",

                "target":"Oracle",

                "relation":"JDBC pool saturation increasing DB latency",

                "confidence":round(corr,2),

                "evidence":[

                    f"Correlation={corr:.2f}"

                ]

            }

        return None

    ###########################################################

    def db_vs_apache(self, oracle, apache):

        if apache is None:

            return None

        if oracle is None:

            return None

        throughput=apache

        timed=oracle.get("timed")

        if throughput.empty:

            return None

        if timed is None:

            return None

        if timed.empty:

            return None

        df=pd.concat(

            [

                throughput["response_time"],

                timed["elapsed_time"]

            ],

            axis=1

        ).dropna()

        if len(df)<5:

            return None

        corr=df.corr().iloc[0,1]

        if corr>0.70:

            return {

                "source":"Oracle",

                "target":"Apache",

                "relation":"Database latency propagating to Apache",

                "confidence":round(corr,2),

                "evidence":[

                    f"Correlation={corr:.2f}"

                ]

            }

        return None

    ###########################################################

    def apache_vs_jmeter(self, apache, jmeter):

        if apache is None:

            return None

        if jmeter is None:

            return None

        if apache.empty:

            return None

        if jmeter.empty:

            return None

        df=pd.concat(

            [

                apache["response_time"],

                # jmeter["elapsed"]
                jmeter["response_time"]

            ],

            axis=1

        ).dropna()

        if len(df)<5:

            return None

        corr=df.corr().iloc[0,1]

        if corr>0.70:

            return {

                "source":"Apache",

                "target":"JMeter",

                "relation":"Apache latency causing user response time increase",

                "confidence":round(corr,2),

                "evidence":[

                    f"Correlation={corr:.2f}"

                ]

            }

        return None