"""
app.py

Performance Engineering Platform Dashboard
"""

from datetime import datetime

import streamlit as st

from backend.jmeter.runner import JMeterRunner
from config.config_service import ConfigService
from backend.utils.logger import Logger
from backend.orchestrator.status_manager import status_manager
from backend.database.repository import (
    TestRunRepository,
    ExecutionLogRepository,
)


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------

config = ConfigService()
logger = Logger.get_logger()

st.set_page_config(
    page_title=config.get("application.name"),
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

from backend.ssh.ssh_client import SSHClient
from backend.configuration.server_configuration_collector import (
    ServerConfigurationCollector
)

print("=" * 80)
print("APP STARTED")
print("=" * 80)

try:
    ssh = SSHClient()

    collector = ServerConfigurationCollector(ssh)

    server_config = collector.collect()

    print(server_config)

except Exception as e:
    print("SERVER CONFIG COLLECTION FAILED")
    print(e)


logger.info("Dashboard loaded")


# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------

if "run_started" not in st.session_state:
    st.session_state.run_started = False

if "current_run_id" not in st.session_state:
    st.session_state.current_run_id = None

if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = True

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now()


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🚀 Performance Engineering Platform")

st.caption(
    f"Version {config.get('application.version')}"
)

st.divider()


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙ Configuration")

    st.subheader("JMeter")

    st.text_input(
        "JMeter Executable",
        value=config.get("jmeter.executable"),
        disabled=True
    )

    st.text_input(
        "JMX File",
        value=config.get("jmeter.jmx_file"),
        disabled=True
    )

    st.text_input(
        "Result CSV",
        value=config.get("jmeter.result_csv"),
        disabled=True
    )

    st.divider()

    st.subheader("InfluxDB")

    st.text_input(
        "Host",
        value=config.get("influxdb.host"),
        disabled=True
    )

    st.text_input(
        "Database",
        value=config.get("influxdb.database"),
        disabled=True
    )

    st.divider()

    st.subheader("Linux Server")

    st.text_input(
        "Host",
        value=config.get("linux.host"),
        disabled=True
    )

    st.text_input(
        "User",
        value=config.get("linux.username"),
        disabled=True
    )

    st.divider()

    st.checkbox(
        "Auto Refresh Dashboard",
        key="auto_refresh"
    )



from backend.health.connection_checker import ConnectionChecker

checker = ConnectionChecker()

results = checker.run_all()

st.subheader("Environment Health Check")

for component, result in results.items():

    success, message = result

    if success:

        st.success(f"{component}: {message}")

    else:

        st.error(f"{component}: {message}")

# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------

runs = TestRunRepository.get_all_runs()

total_runs = len(runs)

completed = len(
    [r for r in runs if r.status == "Completed"]
)

failed = len(
    [r for r in runs if r.status == "Failed"]
)

running = len(
    [r for r in runs if r.status == "Running"]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Runs",
    total_runs
)

col2.metric(
    "Completed",
    completed
)

col3.metric(
    "Running",
    running
)

col4.metric(
    "Failed",
    failed
)

st.divider()


# ---------------------------------------------------------
# Run Test
# ---------------------------------------------------------

left, right = st.columns([2, 1])

with left:

    st.subheader("Performance Test")

    st.write(
        "Click the button below to start a new "
        "performance execution."
    )

with right:

    run_clicked = st.button(
        "▶ Run Performance Test",
        use_container_width=True,
        type="primary"
    )

from backend.orchestrator.orchestrator import TestOrchestrator
col1, col2 = st.columns(2)

with col1:
    orchestrator = TestOrchestrator()

    if run_clicked:

        logger.info("Run button clicked")

     
        run_id = orchestrator.start_test()
        logger.info(
            f"Performance Test Started (Run ID: {run_id})"
        )
        st.session_state.current_run_id = run_id
        st.session_state.run_started = True
        st.success(
            f"Performance Test Started (Run ID: {run_id})"
        )
  
with col2:

    if st.button("🛑 Stop Test"):

        from backend.monitoring.execution_monitor import ExecutionManager

        if ExecutionManager.stop():

            st.success("Execution stopped.")

        else:

            st.warning("No running execution.")
st.divider()


# ---------------------------------------------------------
# Placeholder for next sections
# ---------------------------------------------------------

st.info(
    "Next section: Live Status, Progress Bar, "
    "Execution Logs and Report History."
)


# ---------------------------------------------------------
# Live Execution Status
# ---------------------------------------------------------

st.header("📊 Live Execution Status")


status = status_manager.get_status()

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    st.metric(
        label="Status",
        value=status["status"]
    )

with status_col2:
    st.metric(
        label="Current Stage",
        value=status["stage"]
    )

with status_col3:
    st.metric(
        label="Progress",
        value=f"{status['progress']} %"
    )

st.progress(status["progress"] / 100)

st.write(f"**Message:** {status['message']}")

if status["start_time"]:
    st.write(f"**Started:** {status['start_time']}")

if status["end_time"]:
    st.write(f"**Finished:** {status['end_time']}")

if status["error"]:
    st.error(status["error"])

st.divider()

# ---------------------------------------------------------
# Auto Refresh
# ---------------------------------------------------------

import time

refresh_col1, refresh_col2 = st.columns([4, 1])

with refresh_col1:

    st.caption(
        f"Last Refresh : {st.session_state.last_refresh.strftime('%H:%M:%S')}"
    )

with refresh_col2:

    refresh = st.button(
        "🔄 Refresh",
        use_container_width=True
    )

if refresh:

    st.session_state.last_refresh = datetime.now()

    st.rerun()


# Auto refresh every 5 seconds
if (
    st.session_state.auto_refresh
    and status["status"] == "Running"
):

    time.sleep(5)

    st.session_state.last_refresh = datetime.now()

    st.rerun()


if st.session_state.current_run_id is not None:
    logger.info(
        f"Current Run ID: {st.session_state.current_run_id}"
    )
    run = TestRunRepository.get_test_run(
        st.session_state.current_run_id
    )

    if run is not None:
        st.metric("Status", run.status)
        st.metric("Stage", run.stage)
        st.metric("Progress", f"{run.progress}%")
    else:
        st.warning("Current test run not found in the database.")
    logger.info(f"Database returned: {run}")
else:
    st.info("No active test run.")

# ---------------------------------------------------------
# Execution Logs
# ---------------------------------------------------------

st.header("📄 Execution Logs")

if st.session_state.current_run_id is None:

    st.info("No execution has started.")

else:

    logs = ExecutionLogRepository.get_logs(
        st.session_state.current_run_id
    )

    if not logs:

        st.warning("No logs available.")

    else:

        for log in logs:

            with st.container():

                col1, col2 = st.columns([2, 8])

                with col1:

                    st.write(
                        log.created_at.strftime(
                            "%H:%M:%S"
                        )
                    )

                with col2:

                    st.markdown(
                        f"**{log.stage}**  \n"
                        f"{log.message}"
                    )

                st.divider()


# ---------------------------------------------------------
# Running Indicator
# ---------------------------------------------------------

if status["status"] == "Running":

    st.success("🟢 Test Execution In Progress")

elif status["status"] == "Completed":

    st.success("✅ Execution Completed Successfully")

elif status["status"] == "Failed":

    st.error("❌ Execution Failed")

else:

    st.info("Waiting for execution...")

import json
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# Report History
# ---------------------------------------------------------

st.header("📜 Test Execution History")

runs = TestRunRepository.get_all_runs()

if not runs:

    st.info("No executions found.")

else:

    history = []

    for run in runs:

        history.append(
            {
                "Run ID": run.id,
                "Run Name": run.run_name,
                "Status": run.status,
                "Duration (sec)": round(run.duration, 2),
                "Bottleneck": run.bottleneck,
                "Confidence": run.confidence,
                "Start Time": run.start_time,
                "End Time": run.end_time
            }
        )

    df = pd.DataFrame(history)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


st.divider()

st.subheader("📂 View Generated Reports")

if runs:

    report_ids = [run.id for run in runs]

    selected_run = st.selectbox(

        "Select Test Run",

        report_ids,

        format_func=lambda x: f"Run {x}"

    )

    selected = next(

        r for r in runs

        if r.id == selected_run

    )

else:

    selected = None


# ---------------------------------------------------------
# HTML Report
# ---------------------------------------------------------

if selected:

    st.subheader("🌐 HTML Report")

    html_path = selected.html_report

    if html_path and Path(html_path).exists():

        with open(

            html_path,

            "r",

            encoding="utf-8"

        ) as f:

            html = f.read()

        st.components.v1.html(

            html,

            height=700,

            scrolling=True

        )

    else:

        st.warning(

            "HTML report not found."

        )

# ---------------------------------------------------------
# JSON Report
# ---------------------------------------------------------

if selected:

    st.subheader("📄 JSON Report")

    json_path = selected.json_report

    if json_path and Path(json_path).exists():

        with open(

            json_path,

            "r",

            encoding="utf-8"

        ) as f:

            report = json.load(f)

        st.json(report)

    else:

        st.warning(

            "JSON report not found."

        )


# ---------------------------------------------------------
# Report Summary
# ---------------------------------------------------------

if selected:

    st.subheader("📈 Report Summary")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Status",

            selected.status

        )

    with c2:

        st.metric(

            "Duration",

            f"{selected.duration:.2f} sec"

        )

    with c3:

        st.metric(

            "Confidence",

            selected.confidence

        )

    st.write(

        "**Detected Bottleneck:**",

        selected.bottleneck

    )

