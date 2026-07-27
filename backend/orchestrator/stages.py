"""
Execution Stages
"""

INITIALIZING = "Initializing"

JMETER_START = "Starting JMeter"

JMETER_RUNNING = "Running JMeter"

READING_RESULTS = "Reading JMeter Results"

CONNECTING_INFLUX = "Connecting InfluxDB"

FETCHING_METRICS = "Fetching Metrics"

AGGREGATION = "Aggregating Data"

ANOMALY = "Detecting Anomalies"

RULE_ENGINE = "Running Rule Engine"

GENERATING_HTML = "Generating HTML Report"

GENERATING_JSON = "Generating JSON Report"

COMPLETED = "Completed"

FAILED = "Failed"