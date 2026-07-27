# PerformanceAnalyst – User Manual

This document explains how to configure and run the **PerformanceAnalyst** application.

> Project root: `c:\Nikhil P\SVN\Asset\13_PerformanceAnalyst\PerformanceAnalyst`  
> Entry point: `Main.py`

---

## 1. Prerequisites

### 1.1 Software

- **Python**: 3.x (3.8+ recommended)
- **Python packages** (typical set, inferred from code – adjust based on your environment):
  - `pandas`
  - `influxdb` or `influxdb-client` (depending on how `influx_reader.py` is implemented)
  - Any additional packages your `requirements.txt` or readers use

Install packages, for example:

```bash
pip install pandas influxdb
```

(or use your project-specific `requirements.txt` if present).

### 1.2 External Systems & Data

- **InfluxDB**
  - Running instance reachable from the machine running PerformanceAnalyst.
  - Database name: `macaDB` (default; configurable in `config/settings.py`).
  - Contains relevant time‑series metrics for the time window you plan to analyze.

- **JMeter Results**
  - JMeter aggregate and summary result files generated for the test run.
  - Placed under:
    - `JMeterResults/aggregate/`
    - `JMeterResults/summary/`
  - Filenames and formats must match what `data_sources/jmeter_reader.py` expects.

- **Other Metrics (Apache, Tomcat, Oracle, OS)**
  - Metric collection configured and stored in the way your respective readers expect:
    - `data_sources/apache_reader.py`
    - `data_sources/tomcat_reader.py`
    - `data_sources/oracle_reader.py`
    - `data_sources/os_loader.py`
  - These may pull from InfluxDB, logs, or other stores depending on your implementation.

---

## 2. Configuration

### 2.1 Global Settings (`config/settings.py`)

Key values:

- **InfluxDB Connection**
  - `INFLUX_HOST = "localhost"`
  - `INFLUX_PORT = 8086`
  - `INFLUX_USERNAME = "admin"`
  - `INFLUX_PASSWORD = "admin"`
  - `INFLUX_DB = "macaDB"`

- **Time Window**
  - `START_TIME = "2026-05-29T08:36:20Z"`
  - `END_TIME = "2026-05-29T11:18:52Z"`

  Set these to the time range you want to analyze (must align with both InfluxDB data and JMeter test period).

- **Thresholds**
  - CPU / Memory:
    - `CPU_HIGH_THRESHOLD = 85`
    - `MEMORY_HIGH_THRESHOLD = 80`
  - Latency and errors:
    - `LATENCY_HIGH_THRESHOLD = 1000`
    - `LATENCY_CRITICAL = 1500`
    - `ERROR_RATE_THRESHOLD = 0.05`
    - `ERROR_CRITICAL_THRESHOLD = 0.1`
  - Correlation and anomaly logic:
    - `CORRELATION_THRESHOLD`, `CPU_RT_CORR_THRESHOLD`, `MEMORY_LATENCY_CORR_THRESHOLD`
    - `MIN_SUSTAINED_DURATION`, `MIN_DURATION`, `TREND_THRESHOLD`, `ANOMALIES_THRESHOLD`
  - Apache, Tomcat, Oracle specific thresholds.

- **JMeter results path**
  - `JMeterResultPath = Path("JMeterResults/aggregate/")`

Adjust as needed for your environment (e.g., non‑localhost InfluxDB, different DB name, different JMeter directories, and tuned thresholds).

### 2.2 Monitoring Configuration (`config/monitoring_config.yaml`)

This YAML file is loaded by:

```python
config = ConfigManager("config/monitoring_config.yaml")
```

It typically defines:

- Which servers/hosts are monitored.
- Which metrics to pull for each component (CPU, memory, Apache, Tomcat, Oracle, etc.).
- Any per‑metric or per‑source configuration.

Before running:

1. Open `config/monitoring_config.yaml`.
2. Verify hostnames, measurement names, and other settings match your environment.
3. Save your changes.

---

## 3. Running the Application

### 3.1 From Command Line

1. **Open a terminal / command prompt.**
2. **Navigate to the project root:**

   ```bash
   cd "c:\Nikhil P\SVN\Asset\13_PerformanceAnalyst\PerformanceAnalyst"
   ```

3. **Ensure your Python environment is activated** (if you use virtualenv/conda).

4. **Run the main script:**

   ```bash
   python Main.py
   ```

5. The application will:
   1. Load configuration from `config/monitoring_config.yaml` via `ConfigManager`.
   2. Load metrics from all configured data sources via `dataLoader(config)`.
   3. Aggregate metrics (`aggregate_all(metrics_collection, config)`).
   4. Run anomaly detection and pattern/correlation analysis (`detect_anomalies_and_patterns`).
   5. Execute the rule engine (`run_rule_engine_with_output`).
   6. Print a short summary to the console (`print_short_output`).
   7. Save detailed outputs and an HTML report (`save_detailed_output`, `generate_html_report`).

### 3.2 What You See in the Console

`Main.py` calls:

```python
print_short_output(final_results)
```

This prints, per flow:

- Major **bottlenecks** (HIGH severity issues).
- **Risks** (MEDIUM severity issues).
- Top **action items** / recommendations.
- An overall **confidence** level (and how to interpret it).

There are also more verbose debug/inspection helpers in `Main.py`:

- `print_sample_data(metrics_collection, rows=5)`
- `print_actionable_output(final_results)`

These are currently commented out in the main block and can be enabled if you want more detailed CLI output.

---

## 4. Outputs

### 4.1 File Outputs

`Main.py` uses:

```python
save_detailed_output(final_results)
generate_html_report(final_results)
```

These functions in `utils/output_writer.py` will:

- Write structured, detailed results (per flow and server) to files under the configured output directory (commonly `output/`).
- Generate an HTML report summarizing anomalies, evidence, and recommendations.

Check:

- `output/` (or the directory used in `output_writer.py`) for:
  - JSON or similar structured exports.
  - An HTML summary report you can open in a browser.

### 4.2 Design / Architecture Documentation

For deeper understanding of the internals, see:

- `Docs/SystemDesign.html` – opens in a browser.
- It covers:
  - Architecture.
  - Data flow.
  - Modules.
  - Anomaly detection.
  - Rule engine behavior.

---

## 5. Typical Run Checklist

Before running:

1. [ ] InfluxDB is up and reachable.
2. [ ] JMeter result files are in `JMeterResults/aggregate/` and `JMeterResults/summary/`.
3. [ ] `config/settings.py`:
   - [ ] Influx host/port/DB are correct.
   - [ ] Time window matches your test.
   - [ ] Thresholds are reasonable for your environment.
4. [ ] `config/monitoring_config.yaml` is aligned with your hosts and metrics.
5. [ ] Python dependencies are installed and the correct environment is active.

Then:

1. [ ] Run `python Main.py` from the project root.
2. [ ] Review console output for a quick summary.
3. [ ] Open generated HTML report(s) and detailed outputs for deeper analysis.

---

## 6. Troubleshooting

- **No data found / empty analysis:**
  - Check `START_TIME` / `END_TIME` and that the InfluxDB/JMeter data covers that interval.
  - Verify hostnames and measurement names in `monitoring_config.yaml` and data source readers.

- **Connection errors to InfluxDB:**
  - Confirm host/port/credentials in `config/settings.py`.
  - Ensure InfluxDB is running and accessible from this machine.

- **JMeter file parsing errors:**
  - Confirm file formats (CSV/TXT columns) match what `jmeter_reader.py` expects.
  - Check that the correct directory paths and filenames are used.

- **Unexpected or missing Apache/Tomcat/DB metrics:**
  - Review `apache_reader.py`, `tomcat_reader.py`, `oracle_reader.py`, and `os_loader.py` for their specific expectations.
  - Ensure the backing data sources (logs, Influx measurements, etc.) are present and correctly named.
