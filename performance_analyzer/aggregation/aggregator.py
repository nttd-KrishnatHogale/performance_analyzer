from performance_analyzer.aggregation.flow_builder import build_flows
from performance_analyzer.aggregation.server_builder import build_servers


def aggregate_all(metrics_collection, config):

    flow_collection = build_flows(metrics_collection, config)
    server_collection = build_servers(metrics_collection)

    aggregated_data = {
        "flows": flow_collection,
        "servers": server_collection
    }

    return aggregated_data