from aggregation.instance_aggregator import aggregate_instance_df
from aggregation.oracle_aggregator import aggregate_oracle_instance
from aggregation.merge_utils import merge_dataframes


def build_flows(metrics_collection, config):

    flow_collection = {}

    # ✅ GLOBAL JMETER (IMPORTANT)
    jmeter_df = metrics_collection.get("jmeter")
    jmeter_df = aggregate_instance_df(jmeter_df)

    if jmeter_df is not None:
        jmeter_df = jmeter_df.add_prefix("jmeter_")

    # ============================================================
    # LOOP FLOWS
    # ============================================================
    for flow_id, flow in config.flows.items():

        web_h = flow["web"]["hostname"]
        web_i = flow["web"]["instance"]

        app_h = flow["app"]["hostname"]
        app_i = flow["app"]["instance"]

        db_h = flow["db"]["hostname"]
        db_sid = flow["db"]["sid"]

        server_data_web = metrics_collection["servers"][web_h]
        server_data_app = metrics_collection["servers"][app_h]
        server_data_db = metrics_collection["servers"][db_h]

        # --------------------------------------------------------
        # FETCH RAW DATA
        # --------------------------------------------------------
        apache_df = server_data_web["apache"].get(web_i)
        tomcat_df = server_data_app["tomcat"].get(app_i)
        oracle_data = server_data_db["oracle"].get(db_sid)

        cpu_df = server_data_web.get("cpu")
        mem_df = server_data_web.get("memory")

        # --------------------------------------------------------
        # AGGREGATE PER INSTANCE
        # --------------------------------------------------------
        apache_df = aggregate_instance_df(apache_df)
        tomcat_df = aggregate_instance_df(tomcat_df)
        cpu_df = aggregate_instance_df(cpu_df)
        mem_df = aggregate_instance_df(mem_df)
        oracle_df = aggregate_oracle_instance(oracle_data)

        # --------------------------------------------------------
        # PREFIX (important to avoid column clash)
        # --------------------------------------------------------
        if apache_df is not None:
            apache_df = apache_df.add_prefix("apache_")

        if tomcat_df is not None:
            tomcat_df = tomcat_df.add_prefix("tomcat_")

        if oracle_df is not None:
            oracle_df = oracle_df.add_prefix("oracle_")

        if cpu_df is not None:
            cpu_df = cpu_df.add_prefix("cpu_")

        if mem_df is not None:
            mem_df = mem_df.add_prefix("memory_")

        # --------------------------------------------------------
        # FINAL MERGE (INCLUDING JMETER ✅)
        # --------------------------------------------------------
        combined_df = merge_dataframes([
            apache_df,
            tomcat_df,
            oracle_df,
            cpu_df,
            mem_df,
            jmeter_df
        ])

        if combined_df is not None:
            combined_df["flow_id"] = flow_id

        flow_collection[flow_id] = combined_df

    return flow_collection