import pandas as pd


class CorrelationRules:

    def cpu_vs_tomcat(self, cpu, tomcat):

        if cpu is None or tomcat is None:
            return None
        
        thread_df = tomcat.get("thread")
        if thread_df is None or thread_df.empty:
            return None
        
        if cpu.empty:
            return None
 

        # Create thread utilization if it doesn't exist
        if "thread_utilization" not in thread_df.columns:

            if (
                "used_thread_count" not in thread_df.columns or
                "max_thread_count" not in thread_df.columns
            ):
                return None

            # tomcat = tomcat.copy()
            thread_df = thread_df.copy()

            thread_df["thread_utilization"] = (
            thread_df["used_thread_count"]
            / thread_df["max_thread_count"]
        ) * 100
        print(cpu.index)
        print(cpu.index.is_unique)

        print(thread_df.index)
        print(thread_df.index.is_unique)
        cpu_series = cpu["cpu_usage"].reset_index(drop=True)

        thread_series = thread_df["thread_utilization"].reset_index(drop=True)

        df = pd.concat(
            [cpu_series, thread_series],
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

        # if tomcat is None:
        #     return None
        if tomcat is None or oracle is None:
            return None
        # if oracle is None:
        #     return None
        jdbc_df = tomcat.get("datasource")
        if jdbc_df is None or jdbc_df.empty:
            return None

        # if tomcat.empty:
        #     return None
        timed = oracle.get("raw", {}).get("time_model")
        # timed = oracle.get("timed")

        if timed is None or timed.empty:
            return None

   
        if "elapsed_time" not in timed.columns:
            return None

        if "jdbc_utilization" not in jdbc_df.columns:

            if (
                "used_connection_pool" not in jdbc_df.columns or
                "max_connection_pool" not in jdbc_df.columns
            ):
                return None

            jdbc_df = jdbc_df.copy()

            jdbc_df["jdbc_utilization"] = (
                jdbc_df["used_connection_pool"]
                / jdbc_df["max_connection_pool"]
            ) * 100

        jdbc = jdbc_df["jdbc_utilization"].reset_index(drop=True)
        elapsed = timed["elapsed_time"].reset_index(drop=True)

        df = pd.concat(
            [jdbc, elapsed],
            axis=1
        ).dropna()

        # df = pd.concat(
        #         [
        #             jdbc_df["jdbc_utilization"],
        #             timed["elapsed_time"]
        #         ],
        #         axis=1
        #     ).dropna()

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

        if apache is None or oracle is None:
            return None

        throughput = apache.get("throughput")

        if throughput is None or throughput.empty:
            return None

        timed = oracle.get("raw", {}).get("time_model")

        if timed is None or timed.empty:
            return None

        if "response_time" not in throughput.columns:
            return None

        if "elapsed_time" not in timed.columns:
            return None

        # df = pd.concat(
        #     [
        #         throughput["response_time"],
        #         timed["elapsed_time"]
        #     ],
        #     axis=1
        # ).dropna()
        response = throughput["response_time"].reset_index(drop=True)
        elapsed = timed["elapsed_time"].reset_index(drop=True)

        df = pd.concat(
            [response, elapsed],
            axis=1
        ).dropna()

        if len(df) < 5:
            return None

        corr = df.corr().iloc[0, 1]

        if corr > 0.70:

            return {
                "source": "Oracle",
                "target": "Apache",
                "relation": "Database latency propagating to Apache",
                "confidence": round(corr, 2),
                "evidence": [f"Correlation={corr:.2f}"]
            }

        return None

    ###########################################################

    
    def apache_vs_jmeter(self, apache, jmeter):

        if apache is None or jmeter is None:
            return None

        throughput = apache.get("throughput")

        if throughput is None or throughput.empty:
            return None

        if jmeter.empty:
            return None

        if "response_time" not in throughput.columns:
            return None

        if "response_time" not in jmeter.columns:
            return None

        # df = pd.concat(
        #     [
        #         throughput["response_time"],
        #         jmeter["response_time"]
        #     ],
        #     axis=1
        # ).dropna()
        response = throughput["response_time"].reset_index(drop=True)
        jmeter_rt = jmeter["response_time"].reset_index(drop=True)

        df = pd.concat(
            [response, jmeter_rt],
            axis=1
        ).dropna()

        if len(df) < 5:
            return None

        corr = df.corr().iloc[0, 1]

        if corr > 0.70:

            return {
                "source": "Apache",
                "target": "JMeter",
                "relation": "Apache latency causing user response time increase",
                "confidence": round(corr, 2),
                "evidence": [f"Correlation={corr:.2f}"]
            }

        return None