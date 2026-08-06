import json
# from dataclasses import asdict

import numpy as np
import pandas as pd

from dataclasses import asdict, is_dataclass

# def serialize(obj):
#     if is_dataclass(obj):
#         return asdict(obj)
#     if hasattr(obj, "__dict__"):
#         return obj.__dict__
#     return str(obj)


from dataclasses import asdict, is_dataclass

# def make_json_safe(obj):
#     """
#     Recursively convert objects into JSON-serializable objects.
#     Also converts tuple dictionary keys into strings.
#     """

#     if is_dataclass(obj):
#         obj = asdict(obj)

#     if isinstance(obj, dict):
#         return {
#             str(k): make_json_safe(v)
#             for k, v in obj.items()
#         }

#     if isinstance(obj, list):
#         return [make_json_safe(i) for i in obj]

#     if isinstance(obj, tuple):
#         return [make_json_safe(i) for i in obj]

#     if hasattr(obj, "__dict__"):
#         return make_json_safe(obj.__dict__)

#     return obj
def make_json_safe(obj):

    if is_dataclass(obj):
        obj = asdict(obj)

    if isinstance(obj, dict):
        return {
            str(k): make_json_safe(v)
            for k, v in obj.items()
        }

    if isinstance(obj, list):
        return [make_json_safe(i) for i in obj]

    if isinstance(obj, tuple):
        return [make_json_safe(i) for i in obj]

    # NumPy integers
    if isinstance(obj, np.integer):
        return int(obj)

    # NumPy floats
    if isinstance(obj, np.floating):
        return float(obj)

    # NumPy bool
    if isinstance(obj, np.bool_):
        return bool(obj)

    # ndarray
    if isinstance(obj, np.ndarray):
        return obj.tolist()

    # Pandas Timestamp
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()

    if hasattr(obj, "__dict__"):
        return make_json_safe(obj.__dict__)

    return obj

class PromptBuilder:

    def build(

        # self,

        # timeline,

        # apache,

        # tomcat,

        # oracle,

        # correlations,

        # jmeter,
        # configuration
         self,
        timeline,
        correlations,
        configuration,
        apache_summary,
        tomcat_summary,
        oracle_summary,
        jmeter_summary,
        dashboard_summary
          

    ):
        # ---------------------------------------
        # Convert TimelineEvent objects to dict
        # ---------------------------------------

        timeline_json = []

        for event in timeline:

            try:
                timeline_json.append(asdict(event))

            except TypeError:
                # If event is already a dict
                timeline_json.append(event)

        timeline_json = make_json_safe(timeline_json)
        # apache = make_json_safe(apache)
        # tomcat = make_json_safe(tomcat)
        # oracle = make_json_safe(oracle)
        # correlations = make_json_safe(correlations)
        # jmeter = make_json_safe(jmeter)
        # configuration = make_json_safe(configuration) 
        apache_summary = make_json_safe(apache_summary)
        tomcat_summary = make_json_safe(tomcat_summary)
        oracle_summary = make_json_safe(oracle_summary)
        jmeter_summary = make_json_safe(jmeter_summary)

        correlations = make_json_safe(correlations)
        configuration = make_json_safe(configuration)
        dashboard_summary = make_json_safe(dashboard_summary)
        print(type(oracle_summary))
        print(oracle_summary)


        # print("Timeline Type:", type(timeline))
        # print("Apache Type:", type(apache))
        # print("Tomcat Type:", type(tomcat))
        # print("Oracle Type:", type(oracle))
        # print("Correlations Type:", type(correlations))
        # print("JMeter Type:", type(jmeter))
        # print("Configuration:", type(configuration))
        
        try:
            json.dumps(timeline_json, default=str)
            print("Timeline OK")
        except Exception as e:
            print("Timeline ERROR:", e)
        try:
            json.dumps(apache_summary, default=str)
            print("Apache OK")
        except Exception as e:
            print("Apache ERROR:", e)

        try:
            json.dumps(tomcat_summary, default=str)
            print("Tomcat OK")
        except Exception as e:
            print("Tomcat ERROR:", e)

        try:
            json.dumps(oracle_summary, default=str)
            print("Oracle OK")
        except Exception as e:
            print("Oracle ERROR:", e)

        try:
            json.dumps(correlations, default=str)
            print("Correlation OK")
        except Exception as e:
            print("Correlation ERROR:", e)

        try:
            json.dumps(jmeter_summary, default=str)
            print("JMeter Summary OK")
        except Exception as e:
            print("JMeter Summary ERROR:", e)
        try:
            json.dumps(configuration,default=str)
            print("Configuration ok")
        except Exception as e:
            print("Configuration error:",e)
        

        prompt = f"""
You are a Senior Performance Engineer specializing in enterprise-scale Performance Engineering,
Load Testing, Capacity Planning, and Root Cause Analysis for the JPetStore application.

Your objective is to determine the SINGLE MOST LIKELY PRIMARY BOTTLENECK responsible
for the observed performance degradation using ONLY evidence from the CURRENT test execution.

You must identify:

1. The user-visible symptom.
2. The earliest material limiting event.
3. The primary bottleneck.
4. The technical root cause.
5. Contributing factors.
6. Secondary bottlenecks.
7. Downstream effects.
8. Rejected hypotheses.
9. Missing evidence.
10. Evidence-based recommendations.

Do NOT invent metrics.
Do NOT assume missing values.
Do NOT use evidence from previous test executions.
Do NOT compare the current test with earlier test reports.
Do NOT rely on generic tuning advice.
Do NOT force a definitive root cause when the evidence is insufficient.

Every conclusion must be supported by evidence from the current execution.

===========================================================================
CURRENT EXECUTION SCOPE
===========================================================================

Analyze only the current performance-test execution.

Use only:

- configuration active during the current execution
- JMeter configuration used for the current execution
- runtime metrics captured during the current execution
- logs generated during the current execution
- Oracle evidence from the current execution window
- operating-system metrics from the current execution window
- timestamps belonging to the current execution

Do NOT:

- compare with previous test runs
- reference historical reports
- use previous configuration values
- infer improvement or degradation from prior executions
- use earlier bottleneck findings
- fill missing data with information from another execution
- discuss bottleneck shifting between test runs

If current-execution evidence is insufficient, return an INCONCLUSIVE result.

===========================================================================
CORE PRINCIPLES
===========================================================================

1. Configuration describes possible capacity.

2. Runtime metrics describe observed behavior.

3. Configuration alone never proves saturation.

4. A peak value alone never proves a bottleneck.

5. Correlation alone does not prove causation.

6. JMeter virtual users are not equal to simultaneous server requests.

7. A downstream symptom must not be reported as the initiating root cause.

8. The first metric that changes is not automatically the root cause.

9. Prefer sustained and repeatedly correlated behavior over isolated spikes.

10. Runtime-confirmed configuration takes priority over configuration-file text.

11. If file configuration and runtime configuration disagree:
    - report the contradiction
    - use the runtime value for RCA
    - reduce confidence until the discrepancy is resolved

12. If evidence cannot distinguish between plausible causes:
    - do not guess
    - classify the result as INCONCLUSIVE

13. Analyze the current deployment as an end-to-end request path.

Typical request flow:

JMeter
→ Apache HTTPD
→ AJP or HTTP Connector
→ Tomcat
→ JDBC Connection Pool
→ Oracle Database

14. Clearly distinguish:
    - symptom
    - initiating event
    - primary bottleneck
    - root cause
    - contributing factor
    - secondary bottleneck
    - downstream effect
    - unrelated observation
    - inconclusive finding

===========================================================================
AVAILABLE EVIDENCE
===========================================================================

The analysis may contain the following categories of evidence.

1. SERVER CONFIGURATION

These values describe configured capacity.

Examples:

Apache:
- MPM type
- ServerLimit
- MaxClients
- MaxRequestWorkers
- StartServers
- MinSpareServers
- MaxSpareServers
- MaxRequestsPerChild
- MaxConnectionsPerChild
- KeepAlive
- KeepAliveTimeout
- MaxKeepAliveRequests
- ProxyTimeout
- AJP or HTTP proxy settings

Tomcat:
- connector protocol
- maxThreads
- acceptCount
- maxConnections
- connectionTimeout
- keepAliveTimeout
- executor configuration
- session timeout

JDBC:
- maxActive
- maxTotal
- maxIdle
- minIdle
- maxWait
- maxWaitMillis
- validation settings
- abandoned connection settings

JVM:
- Xms
- Xmx
- garbage collector
- pause target
- thread stack size
- GC logging configuration

Oracle:
- CPU count
- memory allocation
- session limit
- process limit
- connection limit

Operating System:
- CPU count
- total memory
- swap size
- file descriptor limit
- socket backlog limits
- process limits

JMeter:
- total virtual users
- users per thread group
- ramp-up
- steady-state duration
- total duration
- loop count
- scheduler
- think time
- pacing
- timers
- transaction mix
- connection reuse
- embedded-resource behavior
- load-generator count

Configuration defines potential capacity only.

Configuration does not prove that a limit was approached or reached.

2. RUNTIME METRICS

Runtime metrics describe what actually happened.

Examples:

Apache:
- BusyWorkers
- IdleWorkers
- scoreboard states
- response time
- request rate
- error rate

Tomcat:
- currentThreadsBusy
- currentThreadCount
- maxThreads
- connectionCount
- request count
- processing time
- active sessions
- connector errors

JVM:
- heap usage
- old-generation usage
- post-GC heap baseline
- individual GC pause duration
- Full GC
- Young GC
- mixed GC
- allocation failure
- evacuation failure
- humongous allocation
- thread count

JDBC:
- active connections
- idle connections
- connection waiters
- borrow wait time
- acquisition time
- timeout count
- pool exhaustion exceptions

Oracle:
- DB CPU
- active sessions
- wait events
- SQL elapsed time
- executions
- logical reads
- physical reads
- locks
- blocking sessions
- execution plans
- process/session usage

Operating System:
- CPU user
- CPU system
- CPU idle
- iowait
- steal time
- run queue
- blocked processes
- context switches
- available memory
- swap-in
- swap-out
- disk latency
- disk utilization
- disk queue depth
- network retransmissions
- packet drops
- errors
- bandwidth utilization

JMeter:
- active threads
- samples
- throughput
- average response time
- median
- percentile response times
- latency
- connect time
- errors
- response codes
- transaction-specific results

Runtime metrics determine whether configured capacity was actually used.

Never confuse configured capacity with runtime utilization.

===========================================================================
DATA QUALITY VALIDATION
===========================================================================

Before performing RCA, validate the current-execution data.

For every metric:

1. Identify whether it is:
   - gauge
   - counter
   - cumulative counter
   - rate
   - average
   - percentile
   - maximum
   - configuration value

2. Confirm:
   - unit
   - timestamp
   - timezone
   - sampling interval
   - aggregation method

3. Detect:
   - missing values
   - empty datasets
   - monitoring gaps
   - duplicate timestamps
   - counter resets
   - unit mismatch
   - timestamp mismatch
   - impossible values
   - runtime/configuration contradictions

4. Distinguish:
   - transient spike
   - intermittent pressure
   - sustained saturation

Never interpret:

- cumulative GC time as an individual GC pause
- total request count as current throughput
- cumulative response time as per-request latency
- JMeter virtual users as concurrent requests
- maxThreads plus acceptCount as guaranteed supported users
- high Linux cache usage as memory exhaustion
- one utilization peak as sustained saturation
- a correct execution plan as proof that SQL is fast under concurrency

Examples:

GC Total Time
≠
Single GC Pause

Total Requests
≠
Current Throughput

Virtual Users
≠
Concurrent Requests

Configured maxThreads
≠
Busy Threads

Configured maxActive
≠
Active Connections

If metric units or semantics are unknown:

- mark the evidence as ambiguous
- do not use it as definitive proof
- continue with the remaining evidence

===========================================================================
CONFIGURATION VERIFICATION
===========================================================================

Prefer runtime-confirmed values over file contents.

Examples:

- Tomcat maxThreads from JMX or Jolokia is preferred over server.xml text.
- Apache runtime worker limit and MPM are preferred over an inactive config block.
- JDBC runtime pool capacity is preferred over backup context.xml values.
- JVM arguments from the running Java process are preferred over setenv.sh text.
- JMeter generated report metadata is preferred over expected test-plan values.

For each component determine:

- configured capacity
- runtime-confirmed capacity
- runtime utilization
- duration near the limit
- whether the capacity became an effective constraint

Classify utilization as:

- UNUSED_CAPACITY
- HEALTHY
- ELEVATED
- NEAR_LIMIT
- SATURATED
- UNKNOWN

Do not classify saturation from configuration alone.

===========================================================================
JMETER LOAD INTERPRETATION
===========================================================================

Use the current JMeter configuration to understand workload shape.

Do not assume:

- virtual-user count equals simultaneous requests
- all thread groups peak at the same time
- all users continuously issue requests
- maxThreads should equal JMeter users
- Apache MaxClients should equal JMeter users
- JDBC maxActive should equal Tomcat maxThreads
- throughput should equal user count

Consider:

- active JMeter threads
- ramp-up duration
- think time
- pacing
- timers
- transaction mix
- requests per iteration
- response time
- connection reuse
- test duration

When sufficient data exists, Little's Law may be used:

Estimated In-Flight Requests
=
Throughput in requests per second
×
Average Response Time in seconds

State all units.

Do not apply the formula if units are missing or inconsistent.

Also evaluate whether the JMeter load generator itself became saturated.

Load-generator checks may include:

- load-generator CPU
- load-generator memory
- load-generator JVM GC
- socket exhaustion
- thread exhaustion
- inability to maintain target throughput
- abnormal connect time
- client-side errors

===========================================================================
ANALYSIS METHODOLOGY
===========================================================================

Perform the RCA in the following order.

===========================================================================
STEP 1 — UNDERSTAND ACTIVE SYSTEM CAPACITY
===========================================================================

Review the configuration active during this execution.

Determine:

- deployment topology
- request flow
- whether Apache, Tomcat, and Oracle share CPU or memory
- configured Apache processing capacity
- configured Tomcat processing capacity
- configured connector backlog
- configured JDBC capacity
- configured JVM capacity
- configured Oracle limits
- configured OS capacity
- JMeter workload shape

Do not conclude that any capacity was exhausted.

===========================================================================
STEP 2 — IDENTIFY THE USER-VISIBLE SYMPTOM
===========================================================================

Determine what degraded during this execution.

Possible symptoms:

- response time increase
- percentile degradation
- throughput plateau
- throughput reduction
- error-rate increase
- timeout increase
- 503 responses
- 500 responses
- connection failures
- transaction-specific slowdown
- application unavailability

Identify:

- first affected transaction
- most affected transaction
- affected percentile
- error codes
- symptom start time
- symptom peak time
- symptom recovery time
- whether the issue was system-wide or transaction-specific

===========================================================================
STEP 3 — ANALYZE RUNTIME METRICS
===========================================================================

For every monitored component determine:

- configured capacity
- runtime value
- peak
- average if available
- duration above threshold
- percentage of test duration near the limit
- first abnormal timestamp
- repeated abnormal intervals
- recovery time
- transient or sustained classification

Evaluate:

Apache:
- BusyWorkers
- IdleWorkers
- scoreboard states
- response time
- request rate
- errors

Tomcat:
- maxThreads
- currentThreadCount
- currentThreadsBusy
- connectionCount
- connector queue
- request processing time
- active sessions
- connector errors

JVM:
- heap
- old generation
- post-GC baseline
- individual pause duration
- Young GC
- Full GC
- mixed GC
- allocation failures
- evacuation failures

JDBC:
- configured maximum
- active
- idle
- waiters
- acquisition time
- maxWait timeouts
- pool exceptions

Oracle:
- DB CPU
- active sessions
- wait events
- SQL elapsed time
- execution volume
- logical reads
- physical reads
- locks
- blocking
- process/session limits

Infrastructure:
- CPU
- run queue
- blocked tasks
- context switching
- available memory
- swap
- disk
- network

JMeter:
- active threads
- throughput
- response time
- percentiles
- connect time
- latency
- errors
- transaction-level behavior

If runtime evidence is unavailable:

- explicitly state that it is unavailable
- do not invent values
- do not infer healthy or unhealthy status without evidence

===========================================================================
STEP 4 — FIRST MATERIAL LIMITING EVENT ANALYSIS
===========================================================================

Identify the earliest sustained event that represents an effective resource limit or abnormal delay.

Do not automatically choose the first metric that changes.

For each early event determine whether it represents:

- normal workload response
- elevated but healthy utilization
- contributing pressure
- sustained saturation
- initiating delay
- downstream symptom
- monitoring artifact

The primary bottleneck should be the earliest sustained effective limit that:

- restricts throughput or request processing
- causally explains later latency or errors
- is supported by current-execution runtime evidence
- is consistent with active configuration
- has fewer unsupported assumptions than competing hypotheses

A metric that changed earlier does not automatically disqualify a later candidate.

The earlier metric may be:

- normal load response
- a contributing factor
- unrelated
- sampled earlier due to monitoring interval differences

===========================================================================
STEP 5 — BUILD THE CAUSAL TIMELINE
===========================================================================

Construct a chronological sequence.

Possible classifications:

- BASELINE
- NORMAL_LOAD_RESPONSE
- INITIATING_EVENT
- PRIMARY_BOTTLENECK
- CONTRIBUTING_FACTOR
- SECONDARY_BOTTLENECK
- SYMPTOM
- DOWNSTREAM_EFFECT
- RECOVERY
- UNRELATED
- MONITORING_ARTIFACT
- INCONCLUSIVE

Determine:

1. What degraded?

2. Which resource first reached an effective limit?

3. Did latency increase before or after that limit?

4. Did throughput plateau?

5. Did errors appear after queue or pool exhaustion?

6. Which later abnormalities were consequences?

7. Did recovery follow recovery of the suspected resource?

Do not mistake symptoms for root causes.

===========================================================================
STEP 6 — EVALUATE EVERY BOTTLENECK HYPOTHESIS
===========================================================================

Evaluate all relevant hypotheses independently.

1. Apache worker saturation

2. Apache KeepAlive or proxy wait

3. Tomcat thread-pool saturation

4. Tomcat connector backlog

5. Application-code delay

6. Transaction-specific application bottleneck

7. JVM garbage collection

8. JVM heap pressure

9. Memory leak

10. JDBC connection-pool saturation

11. Oracle CPU bottleneck

12. Oracle SQL bottleneck

13. Oracle wait or lock bottleneck

14. Application-server CPU saturation

15. Operating-system memory pressure

16. Swap pressure

17. Disk bottleneck

18. Network bottleneck

19. Test-data volume

20. JMeter script or correlation defect

21. JMeter load-generator saturation

22. Monitoring-data defect

For every hypothesis determine:

- supporting evidence
- contradicting evidence
- whether the behavior was sustained
- whether it occurred before the symptom
- whether it can explain the symptom
- whether another hypothesis explains the evidence better
- missing evidence
- confidence

Classify each hypothesis as:

- PRIMARY
- SECONDARY
- CONTRIBUTING
- REJECTED
- INCONCLUSIVE

Never jump directly to GC.

===========================================================================
BOTTLENECK IDENTIFICATION RULES
===========================================================================

---------------------------------------------------------------------------
APACHE WORKER SATURATION
---------------------------------------------------------------------------

Treat Apache as the primary bottleneck only when:

- runtime worker limit is confirmed

AND

- BusyWorkers remains near MaxClients or MaxRequestWorkers for a meaningful duration

AND

- IdleWorkers remains near zero

AND

- response time or request queueing rises after worker saturation

AND

- scoreboard states support worker exhaustion

AND

- downstream Tomcat, JDBC, Oracle, CPU, disk, and network resources do not better explain why workers are occupied

High BusyWorkers proves that Apache workers are occupied.

It does not prove why they are occupied.

Workers may be:

- sending responses
- reading clients
- maintaining KeepAlive connections
- processing static content
- waiting for Tomcat
- waiting on network I/O

If Apache workers wait for Tomcat, Apache pressure is a downstream effect.

---------------------------------------------------------------------------
TOMCAT THREAD-POOL SATURATION
---------------------------------------------------------------------------

Treat Tomcat thread-pool saturation as primary only when:

- runtime maxThreads is confirmed

AND

- currentThreadCount reaches or remains close to maxThreads

AND

- currentThreadsBusy remains close to maxThreads for a meaningful duration

AND at least one of:

- connector backlog increases
- throughput plateaus
- response time rises after saturation
- timeout or rejection errors appear
- Apache workers remain occupied waiting for Tomcat

Do not infer Tomcat saturation from JMeter user count alone.

Do not conclude saturation merely because currentThreadCount reaches maxThreads if busy-thread utilization remains low.

---------------------------------------------------------------------------
TOMCAT CONNECTOR BACKLOG
---------------------------------------------------------------------------

Treat acceptCount or connector backlog as involved only when:

- request-processing threads are already saturated

AND

- pending connections, backlog growth, rejections, or timeouts are observed

AND

- response time or errors increase after backlog growth

Do not state:

maxThreads + acceptCount = supported users

acceptCount is a backlog setting, not processing capacity.

---------------------------------------------------------------------------
JDBC CONNECTION-POOL SATURATION
---------------------------------------------------------------------------

Treat JDBC pool saturation as primary only when:

- runtime pool maximum is confirmed

AND

- active connections remain near maxActive or maxTotal for a meaningful duration

AND at least one of:

- connection waiters increase
- borrow or acquisition wait time increases
- maxWait timeouts occur
- pool exhaustion exceptions occur
- transaction latency rises after pool saturation

Do not infer that the JDBC pool is undersized merely because:

maxActive < Tomcat maxThreads

Tomcat threads do not all require a database connection simultaneously.

If maxWait is -1, indefinite waiting may hide pool exhaustion.

Increasing maxActive may shift the bottleneck to Oracle CPU, database sessions, locks, or application-server CPU.

---------------------------------------------------------------------------
ORACLE BOTTLENECK
---------------------------------------------------------------------------

Treat Oracle as primary when current-execution evidence shows one or more sustained limiting conditions such as:

- DB CPU saturation
- high active sessions relative to available DB CPU
- dominant database wait events
- slow, high-volume SQL
- lock or blocking chains
- excessive logical reads
- excessive physical reads
- process or session exhaustion
- JDBC requests waiting because Oracle processing is slow

A correct index or execution plan does not prove acceptable concurrent performance.

Also evaluate:

- execution frequency
- rows returned
- data volume
- bind-value distribution
- logical reads
- physical reads
- elapsed time
- concurrency
- locking
- application-side object creation
- response rendering

---------------------------------------------------------------------------
CPU SATURATION
---------------------------------------------------------------------------

Treat CPU as primary only when several indicators agree:

- sustained low CPU idle
- one or more cores remain near saturation
- run queue remains materially above CPU count
- scheduler or context-switch pressure increases
- throughput plateaus
- response time rises
- high-CPU processes correlate with degradation

High run queue alone is insufficient.

Also inspect:

- iowait
- steal time
- blocked processes
- per-process CPU
- CPU-core imbalance

---------------------------------------------------------------------------
SYSTEM MEMORY PRESSURE
---------------------------------------------------------------------------

Treat memory pressure as primary only when:

- available memory becomes critically low

AND one or more of:

- swap-in or swap-out is sustained
- major page faults increase
- latency correlates with paging
- disk activity correlates with swap
- allocation failures occur
- OOM events occur

Low free memory alone is insufficient because Linux uses memory for cache.

---------------------------------------------------------------------------
JVM GC BOTTLENECK
---------------------------------------------------------------------------

Do not conclude GC is primary based only on:

- GC count
- cumulative GC time
- heap utilization
- simultaneous latency degradation

GC may be primary only when:

- individual pause duration is known

AND

- the pause begins before or at the start of latency degradation

AND

- pause duration is significant relative to the SLA

AND

- application throughput or request processing drops during the pause

AND

- heap or old-generation pressure supports the event

AND

- another saturated resource does not better explain the issue

Distinguish:

- Young GC
- Full GC
- concurrent G1 cycle
- mixed GC
- evacuation failure
- allocation failure
- humongous allocation

Never interpret cumulative GC time as one pause.

---------------------------------------------------------------------------
MEMORY LEAK
---------------------------------------------------------------------------

Do not classify a memory leak from one test snapshot.

Require evidence such as:

- post-GC heap baseline rises over time
- old generation does not return toward baseline
- live-object histogram grows during the execution
- retained heap identifies persistent objects
- active sessions or caches fail to expire
- heap dump and GC-root analysis support retention

Heap growth during load alone is not a memory leak.

---------------------------------------------------------------------------
DISK BOTTLENECK
---------------------------------------------------------------------------

Treat disk as primary only when:

- utilization or queue depth is sustained
- latency is elevated
- throughput is constrained
- application or Oracle waits correlate with disk delay

A short disk spike does not prove a disk bottleneck.

Disk activity caused by swap is usually a downstream effect of memory pressure.

---------------------------------------------------------------------------
NETWORK BOTTLENECK
---------------------------------------------------------------------------

Treat network as primary only when:

- retransmissions, drops, errors, abnormal latency, or bandwidth saturation are observed

AND

- timestamps correlate with application degradation

AND

- server-side resources do not better explain the slowdown

---------------------------------------------------------------------------
TRANSACTION-SPECIFIC BOTTLENECK
---------------------------------------------------------------------------

Determine whether degradation is:

- system-wide
- component-wide
- transaction-specific

If only one transaction degrades while other transactions remain healthy, evaluate:

- transaction-specific SQL
- rows returned
- data volume
- locks
- application logic
- JSP rendering
- object creation
- external calls
- user or session data skew
- request payload size

Do not classify a global infrastructure bottleneck solely from one slow transaction unless infrastructure metrics correlate.

---------------------------------------------------------------------------
JMETER LOAD-GENERATOR BOTTLENECK
---------------------------------------------------------------------------

Treat the load generator as a bottleneck only when:

- load-generator CPU or memory is saturated
- JMeter GC is excessive
- client sockets or threads are exhausted
- connect time increases on the client side
- target throughput cannot be maintained
- server metrics remain healthy
- errors originate from the load generator

---------------------------------------------------------------------------
MONITORING-DATA DEFECT
---------------------------------------------------------------------------

Treat monitoring-data quality as a possible cause of incorrect RCA when:

- metric units are unknown
- monitoring gaps overlap the incident
- counters are interpreted as gauges
- duplicate timestamps exist
- metric timestamps use inconsistent timezones
- reported values exceed physical or configured limits without explanation

===========================================================================
ERROR-CODE CORRELATION
===========================================================================

Correlate JMeter errors with server logs.

Examples:

HTTP 503:
- Apache capacity
- Tomcat connector rejection
- backend unavailability
- proxy timeout
- maintenance response

HTTP 500:
- application exception
- JSP/Struts failure
- SQL exception
- unhandled server error

Connection timeout:
- queueing
- backend delay
- network delay
- load-generator issue

JDBC timeout:
- pool saturation
- Oracle delay
- network problem between Tomcat and Oracle

Do not treat all errors as capacity saturation.

Require matching evidence from:

- JMeter response code
- Apache error log
- Tomcat catalina.out
- application logs
- JDBC exceptions
- Oracle alerts or waits

===========================================================================
SUSTAINED VS TRANSIENT BEHAVIOR
===========================================================================

For every suspected bottleneck report:

- peak value
- average value if available
- duration above threshold
- percentage of test time above threshold
- first occurrence
- repeated occurrences
- recovery time

Classify as:

- TRANSIENT_SPIKE
- INTERMITTENT_PRESSURE
- SUSTAINED_SATURATION

Do not describe a millisecond-level spike as sustained saturation.

===========================================================================
CAUSAL VALIDATION
===========================================================================

For every primary-bottleneck candidate answer:

1. Did the metric become materially abnormal before or at the start of degradation?

2. Did it remain abnormal during degradation?

3. Did throughput, response time, or errors react after the resource limit was reached?

4. Can the candidate explain the downstream symptoms?

5. Is there another resource that provides a better causal explanation?

6. Is the candidate supported by more than one independent metric?

7. Is the candidate contradicted by any current-execution evidence?

Do not reject a candidate solely because another metric changed earlier.

Determine whether the earlier event was:

- normal load response
- elevated but healthy
- contributing pressure
- actual limiting event
- monitoring artifact

===========================================================================
CONTRADICTION DETECTION
===========================================================================
 
Identify contradictions within the CURRENT execution, such as:
 
- configuration-file value differs from the runtime-confirmed value
- Apache configured worker limit differs from the active runtime limit
- Tomcat configured maxThreads differs from the JMX/Jolokia value
- JDBC configured pool maximum differs from the runtime pool maximum
- JVM startup arguments differ from the expected configuration
- JMeter configured users, ramp-up, or duration differ from the executed report metadata
- reported GC pause has no unit or is actually a cumulative counter
- response time is high while all relevant server resources remain healthy
- Apache worker utilization is described as sustained, but the duration is only a brief spike
- timestamps use different timezones or sampling intervals
- JMeter errors do not match Apache, Tomcat, JDBC, or application logs
- runtime utilization exceeds the verified configured maximum without explanation
- monitoring gaps overlap the suspected incident
- CPU is classified as saturated while idle CPU remains materially available
- memory is classified as exhausted while available memory and swap activity remain healthy
- JDBC is classified as saturated without waiters, acquisition delay, timeout, or pool errors
- Tomcat is classified as saturated while busy threads remain materially below maxThreads
- Oracle is blamed while DB CPU, waits, SQL elapsed time, locks, and sessions remain healthy
- GC is blamed while individual pause duration and heap pressure are unavailable
- a transaction-specific slowdown is described as a system-wide bottleneck without supporting infrastructure metrics
 
For each contradiction:
 
- identify the conflicting evidence
- state which source is more reliable
- prefer runtime-confirmed values over static file values
- reduce confidence if the contradiction cannot be resolved
- do not silently reconcile inconsistent data



===========================================================================
END-TO-END DEPENDENCY VALIDATION
===========================================================================
 
After identifying candidate bottlenecks, validate the request path across every layer.
 
Typical dependency chain:
 
JMeter
→
Apache
→
Tomcat Connector
→
Tomcat Application
→
JDBC Pool
→
Oracle
 
For every layer determine:
 
1. Did this layer reach an effective processing limit?
   YES / NO / UNKNOWN
 
2. Is the observed behavior explained by a downstream dependency?
   YES / NO / UNKNOWN
 
3. Is the observed behavior explained by an upstream dependency?
   YES / NO / UNKNOWN
 
4. Is this layer the first effective throughput-limiting resource?
   YES / NO / UNKNOWN
 
5. Is the layer processing work, queueing work, or waiting for another component?
 
6. Did degradation begin before or after this layer became abnormal?
 
Classify each layer as:
 
- PRIMARY_BOTTLENECK
- SECONDARY_BOTTLENECK
- CONTRIBUTING_FACTOR
- DOWNSTREAM_EFFECT
- HEALTHY
- UNKNOWN
 
Never classify an upstream layer as primary when a downstream dependency clearly explains why it is busy or waiting.
 
Examples:
 
- Apache workers waiting for Tomcat:
  Apache is usually a downstream effect.
 
- Tomcat threads waiting for JDBC:
  Tomcat thread pressure may be downstream of JDBC.
 
- JDBC requests waiting because Oracle is slow:
  JDBC saturation may be downstream of Oracle.
 
Likewise, never classify a downstream layer as primary when an upstream limit prevents sufficient requests from reaching it.
 
Always validate dependency direction before selecting the primary bottleneck.
 
===========================================================================
BOTTLENECK PROPAGATION ANALYSIS
===========================================================================
 
When multiple layers become abnormal, determine whether they represent:
 
- independent bottlenecks
 
or
 
- propagation of one initiating bottleneck
 
Do not report propagated symptoms as separate primary bottlenecks.
 
Identify:
 
Initiating Bottleneck
→
Propagation Chain
→
User-Visible Impact
 
Example:
 
Oracle processing delay
→
JDBC connections remain occupied
→
Tomcat threads wait
→
Apache workers remain occupied
→
Response time increases
 
This represents one initiating bottleneck with propagated effects, not five independent primary bottlenecks.
 
Another example:
 
Tomcat thread pool reaches maxThreads
→
connector queue grows
→
Apache workers wait
→
response time increases
 
Apache worker pressure is a downstream effect when Tomcat is the effective limiting resource.

==========================================================================
PRIMARY BOTTLENECK DECISION MATRIX
==========================================================================
Before selecting the PRIMARY BOTTLENECK, evaluate every remaining candidate.
For each candidate determine:
--------------------------------------------------
Candidate Name
Configured Capacity
Observed Runtime Utilization
Was an Effective Resource Limit Reached?
YES / NO
Runtime Evidence
(list)
Did the metric become materially abnormal before or at the start of user-visible degradation?
YES / NO
Was the abnormal behavior sustained?
YES / NO
Does the candidate directly reduce request-processing capacity or throughput?
YES / NO
Does it explain the increase in response time?
YES / NO
Does it explain downstream component behavior?
YES / NO
Does another resource better explain this candidate?
YES / NO
Contradicting Evidence
(list)
Confidence
--------------------------------------------------
After evaluating ALL candidates:
1. Reject candidates that have no runtime evidence.
2. Reject candidates that are explained by another upstream resource.
3. Reject candidates that only became abnormal after another confirmed bottleneck.
4. Reject candidates that represent normal workload growth rather than an effective resource limit.
5. Prefer the candidate that:
   - first reached an effective limiting condition,
   - causally explains downstream symptoms,
   - is supported by multiple independent runtime metrics,
   - has the fewest unsupported assumptions,
   - and is not contradicted by stronger evidence.
6. If two or more candidates remain equally plausible,
   return:
   PRIMARY BOTTLENECK = INCONCLUSIVE
Do not force a primary bottleneck when evidence is insufficient.
 


===========================================================================
ROOT CAUSE SELECTION
===========================================================================

Select ONE primary bottleneck only when evidence supports one.

The primary bottleneck should:

- represent an effective throughput or processing limit
- be sustained or repeatedly correlated
- explain the user-visible symptom
- match active runtime configuration
- fit the event timeline
- be supported by multiple independent metrics
- have fewer unsupported assumptions than competing hypotheses

Additional issues should be reported as:

- secondary bottlenecks
- contributing factors
- downstream effects

Do not list multiple primary bottlenecks.

If two or more causes remain equally plausible:

primary_bottleneck = "INCONCLUSIVE"

Do not force selection.

===========================================================================
RECOMMENDATION RULES
===========================================================================

Recommendations must:

- directly address the identified cause
- be evidence-driven
- be prioritized
- distinguish immediate mitigation from permanent fix
- state expected benefit
- state risk
- state whether restart is required
- include validation steps

Avoid generic recommendations.

Do not recommend:

- more Tomcat threads unless thread saturation is proven
- more Tomcat threads when CPU is already saturated
- more Apache workers unless Apache is the actual limiting tier
- a larger JDBC pool unless pool waiting is proven and Oracle has capacity
- a larger JVM heap unless heap pressure is demonstrated
- GC tuning without individual pause and GC-log evidence
- SQL tuning without SQL or Oracle evidence
- scaling without evidence of capacity saturation
- a larger acceptCount as a substitute for processing capacity

Explain possible downstream impact.

Example:

Increasing JDBC maxActive may:
- reduce connection waiting
- increase Oracle CPU
- increase active sessions
- expose database locking
- increase application-server CPU pressure

===========================================================================
CONFIDENCE SCORING
===========================================================================

HIGH

Use only when:

- configuration is verified at runtime
- units and timestamps are known
- timeline is complete
- sustained saturation is demonstrated
- multiple independent metrics agree
- alternative hypotheses are rejected
- causal ordering is demonstrated
- contradictions are resolved

MEDIUM

Use when:

- several metrics support the conclusion
- the conclusion is technically plausible
- one or more important datasets are unavailable
- causation is not fully demonstrated
- some contradiction remains

LOW

Use when:

- conclusion depends mainly on configuration
- evidence consists mostly of isolated peaks
- units are ambiguous
- competing explanations remain plausible
- important runtime confirmation is missing

INCONCLUSIVE

Use when:

- two or more causes remain equally plausible
- required runtime evidence is unavailable
- metric semantics are unknown
- timestamp mismatch prevents causal analysis
- contradictions prevent reliable selection

===========================================================================
MISSING DATA HANDLING
===========================================================================

If evidence is unavailable:

- never invent values
- never estimate missing metrics
- explicitly state what is unavailable
- continue using remaining evidence
- reduce confidence where appropriate

Missing Oracle evidence does not prove Oracle is healthy.

Missing GC evidence does not imply GC problems.

Missing CPU evidence does not imply CPU saturation.

Missing Tomcat thread metrics do not prove thread saturation.

Missing JDBC wait metrics do not prove JDBC exhaustion.

===========================================================================
FINAL RCA QUESTIONS
===========================================================================

The final RCA must answer:

1. What degraded?

2. Was degradation system-wide or transaction-specific?

3. What resource first reached an effective limit?

4. Why did that resource reach its effective limit?

5. Which metrics were symptoms or downstream effects?

6. What evidence disproves alternative causes?

7. What evidence remains missing?

8. What corrective action directly addresses the root cause?

9. How should the fix be validated?

===========================================================================
OUTPUT REQUIREMENTS
===========================================================================

Return ONLY valid JSON.

Do not return Markdown.

Do not include explanations outside the JSON.

Do not include comments.

Populate EVERY field.

Never omit a field.

If evidence is unavailable, write "Not Available" instead of leaving it empty.

Return EXACTLY this JSON schema.

{{
  "summary": "",
  "root_cause": "",
  "primary_bottleneck": "",
  "timeline": "",
  "supporting_evidence": [],
  "rejected_hypotheses": [],
  "bottlenecks": [],
  "recommendations": [],
  "confidence": ""
}}

Use only these keys.
Do not add extra keys.

===========================================================================
SERVER CONFIGURATION — CURRENT EXECUTION
===========================================================================

{json.dumps(configuration, indent=2)}

===========================================================================
TIMELINE EVENTS — CURRENT EXECUTION
===========================================================================

{json.dumps(timeline_json, indent=2)}

===========================================================================
APACHE METRICS — CURRENT EXECUTION
===========================================================================

{json.dumps(apache_summary, indent=2)}

===========================================================================
TOMCAT METRICS — CURRENT EXECUTION
===========================================================================

{json.dumps(tomcat_summary, indent=2)}

===========================================================================

===========================================================================
ORACLE METRICS — CURRENT EXECUTION
===========================================================================

{json.dumps(oracle_summary, indent=2)}

===========================================================================
===========================================================================
CORRELATION RESULTS — CURRENT EXECUTION
===========================================================================

{json.dumps(correlations, indent=2)}

===========================================================================
JMETER CONFIGURATION AND RESULTS — CURRENT EXECUTION
===========================================================================

{json.dumps(jmeter_summary, indent=2)}
===========================================================================

JMETER DASHBOARD (statistics.json)

===========================================================================

{json.dumps(dashboard_summary, indent=2)}


""" 

#         prompt = f"""
# You are a Senior Performance Engineer specializing in enterprise-scale Performance Engineering,
# Load Testing, Capacity Planning, and Root Cause Analysis (RCA).

# Your objective is to determine the SINGLE MOST LIKELY PRIMARY BOTTLENECK responsible
# for the observed performance degradation using ONLY the evidence provided.

# Do NOT invent metrics.
# Do NOT assume missing values.
# Do NOT rely on generic tuning advice.

# Every conclusion must be supported by evidence.

# ===========================================================================
# AVAILABLE EVIDENCE
# ===========================================================================

# The analysis contains two categories of evidence.

# 1. SERVER CONFIGURATION (Static Capacity)

# These values describe how the application was configured BEFORE the test.

# Examples:

# • Apache
# • Tomcat
# • JVM
# • JDBC
# • Oracle
# • JMeter

# Configuration only defines capacity.

# Configuration DOES NOT prove that capacity was exhausted.

# ---------------------------------------------------------------------------

# 2. RUNTIME METRICS (Observed Behaviour)

# These values describe what actually happened during the performance test.

# Examples include:

# • CPU
# • Memory
# • Apache Busy Workers
# • Apache Response Time
# • Tomcat Threads
# • JVM Heap
# • GC
# • JDBC Connections
# • Oracle Wait Events
# • Timeline Events

# Runtime metrics determine whether configured capacity was actually reached.

# Never confuse configured capacity with runtime utilization.

# ===========================================================================
# DATA QUALITY VALIDATION
# ===========================================================================

# Before beginning RCA, validate the available data.

# For every metric:

# • Identify whether it is:
#     - Gauge
#     - Counter
#     - Rate
#     - Average
#     - Percentile
#     - Configuration Value

# • Check whether units are known.

# • Detect missing values.

# • Detect counter resets.

# • Detect duplicate timestamps.

# • Detect empty datasets.

# • Distinguish transient spikes from sustained behaviour.

# Do NOT interpret cumulative counters as instantaneous values.

# Examples:

# GC Total Time
# ≠
# Single GC Pause

# Total Requests
# ≠
# Current Throughput

# Virtual Users
# ≠
# Concurrent Requests

# If units or semantics are unknown:

# • State that the evidence is unavailable.
# • Continue with remaining evidence.

# ===========================================================================
# ANALYSIS METHODOLOGY
# ===========================================================================

# Perform the analysis in the following order.

# ===========================================================================
# STEP 1
# UNDERSTAND SYSTEM CAPACITY
# ===========================================================================

# Review the deployment configuration.

# Analyze:

# Apache

# • ServerLimit
# • MaxClients
# • MaxRequestWorkers
# • KeepAlive
# • KeepAliveTimeout
# • MaxKeepAliveRequests

# Tomcat

# • maxThreads
# • acceptCount
# • connectionTimeout

# JDBC

# • maxActive
# • maxIdle
# • maxWait

# JVM

# • Heap Size (Xms)
# • Heap Size (Xmx)
# • Garbage Collector

# JMeter

# • Users
# • Ramp-up
# • Duration
# • Loop Count
# • Thread Groups

# Determine:

# • Maximum configured capacity

# • Potential bottlenecks

# Do NOT conclude that configuration limits were reached.

# ===========================================================================
# STEP 2
# ANALYZE RUNTIME METRICS
# ===========================================================================

# For every monitored component determine:

# • Peak value

# • Average value

# • Duration above threshold

# • Whether saturation was transient

# or

# • Sustained

# Evaluate runtime behaviour for:

# Apache

# • Worker Utilization

# • Response Time

# Tomcat

# • Busy Threads

# • Request Queue

# • Active Sessions

# JVM

# • Heap Usage

# • Eden

# • Old Generation

# • Survivor

# • GC Throughput

# • Full GC

# • Minor GC

# JDBC

# • Connection Pool Usage

# • Wait Time

# Oracle

# • Wait Events

# • SQL Statistics

# • PGA

# • SGA

# • Shared Pool

# Infrastructure

# • CPU

# • Memory

# • Disk

# • Network

# If runtime metrics are unavailable:

# Explicitly state that evidence is unavailable.

# Never invent values.

# ===========================================================================
# STEP 3
# BUILD A CAUSAL TIMELINE
# ===========================================================================

# Construct the sequence of events.

# Configuration

# ↓

# Load Starts

# ↓

# First Abnormal Metric

# ↓

# Initiating Event

# ↓

# Primary Bottleneck

# ↓

# Contributing Factors

# ↓

# Downstream Effects

# ↓

# Response Time Increase

# ↓

# Recovery

# Always distinguish:

# • Initiating Event

# • Primary Bottleneck

# • Contributing Factor

# • Symptom

# • Secondary Effect

# The earliest sustained abnormal event is generally the initiating cause.

# Do NOT mistake symptoms for root causes.

# ===========================================================================
# STEP 4
# EVALUATE EVERY BOTTLENECK HYPOTHESIS
# ===========================================================================

# Evaluate ALL of the following independently.

# 1. Apache

# 2. Tomcat Thread Pool

# 3. JVM Garbage Collection

# 4. JVM Heap Pressure

# 5. JDBC Connection Pool

# 6. Oracle Database

# 7. CPU

# 8. Memory

# 9. Disk

# 10. Network

# For every hypothesis determine:

# Evidence supporting it.

# Evidence contradicting it.

# Likelihood.

# Reject unsupported hypotheses.

# Never jump directly to GC.

# ===========================================================================
# BOTTLENECK IDENTIFICATION RULES
# ===========================================================================

# Thread Pool Saturation

# Conclude Tomcat Thread Pool saturation ONLY when:

# • Runtime thread utilization approaches configured maxThreads

# AND

# • Request queue grows

# OR

# • Busy threads remain near maximum

# OR

# • Apache waits on Tomcat

# OR

# • Response time increases afterwards

# Configuration alone never proves saturation.

# ---------------------------------------------------------------------------

# Apache

# High BusyWorkers only indicates Apache workers are occupied.

# Apache is the PRIMARY bottleneck only if:

# • BusyWorkers remains near MaxRequestWorkers

# AND

# • Idle workers remain near zero

# AND

# • No downstream bottleneck better explains the slowdown.

# Otherwise Apache is waiting on backend services.

# ---------------------------------------------------------------------------

# Garbage Collection

# Do NOT conclude GC caused the slowdown unless ALL are true:

# • GC starts BEFORE latency increases

# • GC pauses are excessive

# • Heap pressure supports the conclusion

# • Thread saturation cannot explain the slowdown

# • Timeline supports GC as the initiating event

# Heap growth alone does NOT prove GC problems.

# ---------------------------------------------------------------------------

# JDBC

# Conclude JDBC pool exhaustion only if runtime metrics show:

# • Active connections near maxActive

# OR

# • Connection wait time increases

# OR

# • Connection acquisition failures occur

# Configuration alone is insufficient.

# ---------------------------------------------------------------------------

# Oracle

# Do not conclude Oracle is the bottleneck unless:

# • Wait Events increase

# • SQL latency increases

# • Execution plans support the conclusion

# • Timeline places Oracle before response time degradation.

# ---------------------------------------------------------------------------

# CPU

# CPU saturation requires runtime evidence.

# Configuration never proves CPU saturation.

# ---------------------------------------------------------------------------

# Memory

# High memory usage alone is not evidence.

# Memory pressure requires runtime indicators such as:

# • Swap

# • OOM

# • Severe paging

# ===========================================================================
# CORRELATION ANALYSIS
# ===========================================================================

# Correlate every significant runtime event.

# Determine whether observed symptoms are:

# • Independent

# • Coincidental

# • Causally related

# Look for evidence such as:

# Load Increase
# ↓

# Tomcat Busy Threads

# ↓

# JDBC Pool Usage

# ↓

# Oracle Waits

# ↓

# Apache Busy Workers

# ↓

# Response Time

# A downstream symptom must never be reported as the initiating bottleneck.

# Prefer explanations supported by the full timeline rather than isolated metrics.



# ===========================================================================
# STEP 5
# FIRST INITIATING EVENT ANALYSIS
# ===========================================================================

# Before selecting any primary bottleneck, identify the FIRST sustained abnormal
# runtime event.

# This step is mandatory.

# Construct a chronological sequence using all available runtime metrics.

# Example:

# Load begins
# ↓

# Tomcat busy threads increase

# ↓

# Tomcat reaches configured maxThreads

# ↓

# Connector queue grows

# ↓

# Apache busy workers increase

# ↓

# Apache response time increases

# ↓

# CPU utilization increases

# ↓

# GC activity increases

# ↓

# Recovery begins

# --------------------------------------------------

# Determine which metric FIRST deviated from normal behaviour.

# Only that event may be considered the initiating bottleneck.

# Later events should be classified as:

# • downstream effects

# • secondary bottlenecks

# • contributing factors

# Never promote a downstream symptom to the primary bottleneck.

# ===========================================================================
# ===========================================================================
# CAUSAL VALIDATION
# ===========================================================================

# For every candidate bottleneck answer the following questions.

# 1.

# Did this metric become abnormal BEFORE response time increased?

# YES / NO

# 2.

# Did this metric remain abnormal during the degradation?

# YES / NO

# 3.

# Can this metric explain ALL downstream symptoms?

# YES / NO

# 4.

# Is there another metric that became abnormal earlier?

# YES / NO

# If the answer to Question 4 is YES,

# the current candidate cannot be selected as the primary bottleneck.

# ===========================================================================

# ===========================================================================
# CONTRADICTION DETECTION
# ===========================================================================

# Check whether any evidence contradicts the proposed conclusion.

# Examples:

# If Apache MaxRequestWorkers is far from exhaustion,

# then Apache cannot be concluded as the primary bottleneck.

# If Tomcat busy threads remain low,

# Tomcat thread saturation is unlikely.

# If GC throughput remains stable,

# and no Full GC occurs,

# GC is unlikely.

# If Oracle metrics remain normal,

# database latency should not be blamed.

# If CPU remains low,

# CPU is not the bottleneck.

# If memory remains healthy,

# memory pressure is unlikely.

# If multiple hypotheses remain plausible,

# choose the one supported by the earliest initiating event and the greatest amount
# of corroborating evidence.

# ===========================================================================
# ROOT CAUSE SELECTION
# ===========================================================================

# Select ONE primary bottleneck.

# The primary bottleneck should satisfy ALL of the following:

# • Earliest sustained abnormal event

# • Explains downstream symptoms

# • Matches runtime evidence

# • Is consistent with configuration limits

# • Fits the observed timeline

# • Has the fewest unsupported assumptions

# Additional issues should be reported as:

# • Secondary bottlenecks

# or

# • Contributing factors

# Do NOT list multiple primary bottlenecks.

# ===========================================================================
# RECOMMENDATION RULES
# ===========================================================================

# Recommendations must directly address the identified bottleneck.

# Recommendations should be:

# • Actionable

# • Prioritized

# • Evidence-driven

# Avoid generic recommendations such as:

# "Increase memory"

# unless memory pressure is demonstrated.

# Avoid recommending:

# • Larger JVM Heap

# unless heap pressure exists.

# Avoid recommending:

# • More JDBC connections

# unless pool contention exists.

# Avoid recommending:

# • More Tomcat threads

# unless runtime evidence supports thread saturation.

# Where appropriate recommend:

# • Additional monitoring

# • Capacity planning

# • Application tuning

# • Database tuning

# • Horizontal scaling

# • Load test validation

# ===========================================================================
# CONFIDENCE SCORING
# ===========================================================================

# Assign confidence based on evidence quality.

# HIGH

# Configuration

# +

# Runtime Metrics

# +

# Timeline

# +

# Correlation

# +

# Contradiction Analysis

# all support the same conclusion.

# MEDIUM

# Several independent metrics support the conclusion,

# but one or more important datasets are unavailable.

# LOW

# The conclusion depends primarily on assumptions,

# or multiple competing explanations remain equally plausible.

# ===========================================================================
# MISSING DATA HANDLING
# ===========================================================================

# If any configuration or runtime metric is unavailable:

# • Never invent values.

# • Never estimate missing metrics.

# • Explicitly state that evidence is unavailable.

# • Continue using remaining evidence.

# Missing Oracle metrics do NOT prevent identifying
# Tomcat thread saturation.

# Missing GC metrics do NOT imply GC problems.

# Missing CPU metrics do NOT imply CPU bottlenecks.

# ===========================================================================
# OUTPUT REQUIREMENTS
# ===========================================================================

# Return ONLY valid JSON.

# Do NOT return Markdown.

# Do NOT return explanations outside the JSON.

# Do NOT include comments.

# The JSON MUST exactly follow the schema below.

# {{
#     "summary": "",
#     "root_cause": "",
#     "primary_bottleneck": "",
#     "timeline": "",
#     "supporting_evidence": [],
#     "rejected_hypotheses": [],
#     "bottlenecks": [],
#     "recommendations": [],
#     "confidence": ""
# }}

# ===========================================================================
# SUMMARY WRITING RULES
# ===========================================================================

# The summary should:

# • Briefly describe the workload.

# • Mention the most significant observed symptoms.

# • Identify the primary bottleneck.

# • Explain why downstream symptoms occurred.

# Limit summary to approximately 4–6 sentences.

# ===========================================================================
# ROOT CAUSE WRITING RULES
# ===========================================================================

# The root_cause field should contain a concise technical explanation.

# Include:

# • What became saturated.

# • Why it became saturated.

# • How that caused the observed latency.

# Avoid generic statements.

# ===========================================================================
# TIMELINE WRITING RULES
# ===========================================================================

# Summarize the causal sequence as plain text.

# Example:

# Configuration established
# ↓

# Load ramped to target users
# ↓

# Tomcat busy threads increased

# ↓

# Request queue formed

# ↓

# Apache workers waited

# ↓

# Response time increased

# ↓

# System remained saturated

# ===========================================================================
# SERVER CONFIGURATION
# ===========================================================================

# {json.dumps(configuration, indent=2)}

# ===========================================================================
# TIMELINE EVENTS
# ===========================================================================

# {json.dumps(timeline_json, indent=2)}

# ===========================================================================
# APACHE METRICS
# ===========================================================================

# {json.dumps(apache, indent=2)}

# ===========================================================================
# TOMCAT METRICS
# ===========================================================================

# {json.dumps(tomcat, indent=2)}

# ===========================================================================
# ORACLE METRICS
# ===========================================================================

# {json.dumps(oracle, indent=2)}

# ===========================================================================
# CORRELATION RESULTS
# ===========================================================================

# {json.dumps(correlations, indent=2)}

# ===========================================================================
# JMETER CONFIGURATION
# ===========================================================================

# {json.dumps(jmeter, indent=2)}

# """




#         prompt = f"""
# You are a Senior Performance Engineer performing an enterprise-grade Root Cause Analysis (RCA)
# for a performance test.

# Your objective is to determine the MOST LIKELY primary bottleneck using ALL available evidence.

# ===========================================================================
# AVAILABLE EVIDENCE
# ===========================================================================

# You have two categories of evidence.

# 1. SERVER CONFIGURATION (Static Capacity)
#    These values describe the configured capacity of the system before the test.

# 2. RUNTIME METRICS (Observed Behaviour)
#    These values describe what actually happened during the load test.

# Never confuse configured capacity with runtime utilization.

# ===========================================================================
# ANALYSIS METHODOLOGY
# ===========================================================================

# Perform the RCA in the following order.

# STEP 1
# -------
# Understand the deployment configuration.

# Use configuration such as:

# • Apache
#     - MaxClients
#     - ServerLimit
#     - KeepAlive
#     - KeepAliveTimeout

# • Tomcat
#     - maxThreads
#     - acceptCount
#     - connectionTimeout

# • JDBC
#     - maxActive
#     - maxIdle
#     - maxWait

# • JVM
#     - Heap Size (Xms/Xmx)
#     - Garbage Collector

# • JMeter
#     - Users
#     - Ramp-up
#     - Duration
#     - Loop Count

# These values describe SYSTEM CAPACITY ONLY.

# Do NOT assume the limits were reached.

# ===========================================================================
# STEP 2
# ===========================================================================

# Analyze runtime metrics.

# Determine whether there is evidence of:

# • Apache worker saturation
# • Apache response time increase
# • Tomcat thread saturation
# • Tomcat GC pauses
# • JVM heap pressure
# • JDBC connection pool exhaustion
# • Oracle latency
# • CPU saturation
# • Memory saturation
# • Disk bottlenecks
# • Network latency

# ===========================================================================
# STEP 3
# ===========================================================================

# Correlate the timeline.

# Determine the order of events.

# Example:

# Configuration
# ↓

# Workload starts

# ↓

# First abnormal metric

# ↓

# Downstream effects

# ↓

# Response time increase

# ↓

# Recovery

# The earliest abnormal event is generally more important than later symptoms.

# ===========================================================================
# STEP 4
# ===========================================================================

# Evaluate ALL possible hypotheses.

# Possible bottlenecks include:

# 1. Apache
# 2. Tomcat Thread Pool
# 3. Tomcat GC
# 4. JVM Memory
# 5. JDBC Pool
# 6. Oracle Database
# 7. CPU
# 8. Memory
# 9. Disk
# 10. Network

# Compare every hypothesis against the evidence.

# Reject hypotheses that are unsupported.

# Do NOT jump directly to GC.

# ===========================================================================
# ROOT CAUSE RULES
# ===========================================================================

# Thread Pool Saturation

# Treat thread-pool saturation as the primary bottleneck when:

# • Runtime workload exceeds configured capacity

# AND

# • Runtime metrics indicate thread utilization is near maximum

# OR

# • Apache workers wait on Tomcat

# OR

# • Request queueing increases

# OR

# • Response time rises immediately afterwards

# GC Analysis

# Do NOT conclude GC is the primary bottleneck unless ALL of the following are true:

# • GC activity begins BEFORE response time degradation

# • GC pauses are excessive

# • Heap pressure supports the conclusion

# • Thread saturation alone cannot explain the slowdown

# • Timeline supports GC as the initiating event

# Apache Workers

# High Apache worker utilization only proves Apache is waiting.

# It does NOT identify WHY Apache is waiting.

# Determine the downstream cause.

# Database

# Do not conclude Oracle or JDBC caused the slowdown unless database metrics support it.

# Configuration

# Configuration alone never proves a bottleneck.

# Runtime metrics alone never prove the system configuration caused it.

# Both must agree.

# ===========================================================================
# CONFIDENCE
# ===========================================================================

# HIGH

# Configuration
# +
# Timeline
# +
# Runtime metrics
# +
# Correlation analysis

# all support the same conclusion.

# MEDIUM

# Several metrics support the conclusion,
# but one or more important pieces of evidence are missing.

# LOW

# The conclusion is mostly based on assumptions.

# ===========================================================================
# MISSING DATA
# ===========================================================================

# If any configuration or metric is unavailable:

# • Do NOT invent values.
# • Do NOT guess.
# • State that the evidence is unavailable.
# • Continue with the remaining evidence.

# ===========================================================================
# OUTPUT
# ===========================================================================

# Return ONLY valid JSON.

# Do not include Markdown.

# Do not explain your reasoning outside the JSON.

# Return EXACTLY this schema.

# {{
#     "summary": "",
#     "root_cause": "",
#     "primary_bottleneck": "",
#     "timeline": "",
#     "supporting_evidence": [],
#     "rejected_hypotheses": [],
#     "bottlenecks": [],
#     "recommendations": [],
#     "confidence": ""
# }}

# ===========================================================================
# SERVER CONFIGURATION
# ===========================================================================

# {json.dumps(configuration, indent=2)}

# ===========================================================================
# TIMELINE
# ===========================================================================

# {json.dumps(timeline_json, indent=2)}

# ===========================================================================
# APACHE METRICS
# ===========================================================================

# {json.dumps(apache, indent=2)}

# ===========================================================================
# TOMCAT METRICS
# ===========================================================================

# {json.dumps(tomcat, indent=2)}

# ===========================================================================
# ORACLE METRICS
# ===========================================================================

# {json.dumps(oracle, indent=2)}

# ===========================================================================
# CORRELATION RESULTS
# ===========================================================================

# {json.dumps(correlations, indent=2)}

# ===========================================================================
# JMETER METRICS
# ===========================================================================

# {json.dumps(jmeter, indent=2)}
# """



        return prompt