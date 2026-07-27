from aggregation.instance_aggregator import aggregate_instance_df
from aggregation.oracle_aggregator import aggregate_oracle_instance
from aggregation.merge_utils import merge_dataframes


def build_servers(metrics_collection):

    server_collection = {}

    # ✅ GLOBAL JMETER (also include in server view)
    jmeter_df = metrics_collection.get("jmeter")
    jmeter_df = aggregate_instance_df(jmeter_df)

    if jmeter_df is not None:
        jmeter_df = jmeter_df.add_prefix("jmeter_")

    # ============================================================
    # LOOP SERVERS
    # ============================================================
    for hostname, data in metrics_collection["servers"].items():

        dfs = []

        # --------------------------------------------------------
        # CPU + MEMORY
        # --------------------------------------------------------
        cpu_df = aggregate_instance_df(data.get("cpu"))
        mem_df = aggregate_instance_df(data.get("memory"))

        if cpu_df is not None:
            dfs.append(cpu_df.add_prefix("cpu_"))

        if mem_df is not None:
            dfs.append(mem_df.add_prefix("memory_"))

        # --------------------------------------------------------
        # APACHE (ALL INSTANCES)
        # --------------------------------------------------------
        for inst, df in data.get("apache", {}).items():

            df = aggregate_instance_df(df)

            if df is not None:
                dfs.append(df.add_prefix(f"apache_{inst}_"))

        # --------------------------------------------------------
        # TOMCAT
        # --------------------------------------------------------
        for inst, df in data.get("tomcat", {}).items():

            df = aggregate_instance_df(df)

            if df is not None:
                dfs.append(df.add_prefix(f"tomcat_{inst}_"))

        # --------------------------------------------------------
        # ORACLE
        # --------------------------------------------------------
        for sid, db_data in data.get("oracle", {}).items():

            df = aggregate_oracle_instance(db_data)

            if df is not None:
                dfs.append(df.add_prefix(f"oracle_{sid}_"))

        # --------------------------------------------------------
        # ✅ INCLUDE JMETER (GLOBAL CONTEXT)
        # --------------------------------------------------------
        dfs.append(jmeter_df)

        # --------------------------------------------------------
        # FINAL MERGE
        # --------------------------------------------------------
        combined_df = merge_dataframes(dfs)

        if combined_df is not None:
            combined_df["server"] = hostname

        server_collection[hostname] = combined_df

    return server_collection