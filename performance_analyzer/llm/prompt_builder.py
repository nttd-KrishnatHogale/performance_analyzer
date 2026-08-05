import json
# from dataclasses import asdict



from dataclasses import asdict, is_dataclass

# def serialize(obj):
#     if is_dataclass(obj):
#         return asdict(obj)
#     if hasattr(obj, "__dict__"):
#         return obj.__dict__
#     return str(obj)


from dataclasses import asdict, is_dataclass

def make_json_safe(obj):
    """
    Recursively convert objects into JSON-serializable objects.
    Also converts tuple dictionary keys into strings.
    """

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

    if hasattr(obj, "__dict__"):
        return make_json_safe(obj.__dict__)

    return obj

class PromptBuilder:

    def build(

        self,

        timeline,

        apache,

        tomcat,

        oracle,

        correlations,

        jmeter,
        configuration

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
        apache = make_json_safe(apache)
        tomcat = make_json_safe(tomcat)
        oracle = make_json_safe(oracle)
        correlations = make_json_safe(correlations)
        jmeter = make_json_safe(jmeter)
        configuration = make_json_safe(configuration)




        print("Timeline Type:", type(timeline))
        print("Apache Type:", type(apache))
        print("Tomcat Type:", type(tomcat))
        print("Oracle Type:", type(oracle))
        print("Correlations Type:", type(correlations))
        print("JMeter Type:", type(jmeter))
        print("Configuration:", type(configuration))

        try:
            json.dumps(apache, default=str)
            print("Apache OK")
        except Exception as e:
            print("Apache ERROR:", e)

        try:
            json.dumps(tomcat, default=str)
            print("Tomcat OK")
        except Exception as e:
            print("Tomcat ERROR:", e)

        try:
            json.dumps(oracle, default=str)
            print("Oracle OK")
        except Exception as e:
            print("Oracle ERROR:", e)

        try:
            json.dumps(correlations, default=str)
            print("Correlation OK")
        except Exception as e:
            print("Correlation ERROR:", e)

        try:
            json.dumps(jmeter, default=str)
            print("JMeter OK")
        except Exception as e:
            print("JMeter ERROR:", e)
        try:
            json.dumps(configuration,default=str)
            print("Configuration ok")
        except Exception as e:
            print("Configuration error:",e)




        prompt = f"""
You are a Senior Performance Engineer performing an enterprise-grade Root Cause Analysis (RCA)
for a performance test.

Your objective is to determine the MOST LIKELY primary bottleneck using ALL available evidence.

===========================================================================
AVAILABLE EVIDENCE
===========================================================================

You have two categories of evidence.

1. SERVER CONFIGURATION (Static Capacity)
   These values describe the configured capacity of the system before the test.

2. RUNTIME METRICS (Observed Behaviour)
   These values describe what actually happened during the load test.

Never confuse configured capacity with runtime utilization.

===========================================================================
ANALYSIS METHODOLOGY
===========================================================================

Perform the RCA in the following order.

STEP 1
-------
Understand the deployment configuration.

Use configuration such as:

• Apache
    - MaxClients
    - ServerLimit
    - KeepAlive
    - KeepAliveTimeout

• Tomcat
    - maxThreads
    - acceptCount
    - connectionTimeout

• JDBC
    - maxActive
    - maxIdle
    - maxWait

• JVM
    - Heap Size (Xms/Xmx)
    - Garbage Collector

• JMeter
    - Users
    - Ramp-up
    - Duration
    - Loop Count

These values describe SYSTEM CAPACITY ONLY.

Do NOT assume the limits were reached.

===========================================================================
STEP 2
===========================================================================

Analyze runtime metrics.

Determine whether there is evidence of:

• Apache worker saturation
• Apache response time increase
• Tomcat thread saturation
• Tomcat GC pauses
• JVM heap pressure
• JDBC connection pool exhaustion
• Oracle latency
• CPU saturation
• Memory saturation
• Disk bottlenecks
• Network latency

===========================================================================
STEP 3
===========================================================================

Correlate the timeline.

Determine the order of events.

Example:

Configuration
↓

Workload starts

↓

First abnormal metric

↓

Downstream effects

↓

Response time increase

↓

Recovery

The earliest abnormal event is generally more important than later symptoms.

===========================================================================
STEP 4
===========================================================================

Evaluate ALL possible hypotheses.

Possible bottlenecks include:

1. Apache
2. Tomcat Thread Pool
3. Tomcat GC
4. JVM Memory
5. JDBC Pool
6. Oracle Database
7. CPU
8. Memory
9. Disk
10. Network

Compare every hypothesis against the evidence.

Reject hypotheses that are unsupported.

Do NOT jump directly to GC.

===========================================================================
ROOT CAUSE RULES
===========================================================================

Thread Pool Saturation

Treat thread-pool saturation as the primary bottleneck when:

• Runtime workload exceeds configured capacity

AND

• Runtime metrics indicate thread utilization is near maximum

OR

• Apache workers wait on Tomcat

OR

• Request queueing increases

OR

• Response time rises immediately afterwards

GC Analysis

Do NOT conclude GC is the primary bottleneck unless ALL of the following are true:

• GC activity begins BEFORE response time degradation

• GC pauses are excessive

• Heap pressure supports the conclusion

• Thread saturation alone cannot explain the slowdown

• Timeline supports GC as the initiating event

Apache Workers

High Apache worker utilization only proves Apache is waiting.

It does NOT identify WHY Apache is waiting.

Determine the downstream cause.

Database

Do not conclude Oracle or JDBC caused the slowdown unless database metrics support it.

Configuration

Configuration alone never proves a bottleneck.

Runtime metrics alone never prove the system configuration caused it.

Both must agree.

===========================================================================
CONFIDENCE
===========================================================================

HIGH

Configuration
+
Timeline
+
Runtime metrics
+
Correlation analysis

all support the same conclusion.

MEDIUM

Several metrics support the conclusion,
but one or more important pieces of evidence are missing.

LOW

The conclusion is mostly based on assumptions.

===========================================================================
MISSING DATA
===========================================================================

If any configuration or metric is unavailable:

• Do NOT invent values.
• Do NOT guess.
• State that the evidence is unavailable.
• Continue with the remaining evidence.

===========================================================================
OUTPUT
===========================================================================

Return ONLY valid JSON.

Do not include Markdown.

Do not explain your reasoning outside the JSON.

Return EXACTLY this schema.

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

===========================================================================
SERVER CONFIGURATION
===========================================================================

{json.dumps(configuration, indent=2)}

===========================================================================
TIMELINE
===========================================================================

{json.dumps(timeline_json, indent=2)}

===========================================================================
APACHE METRICS
===========================================================================

{json.dumps(apache, indent=2)}

===========================================================================
TOMCAT METRICS
===========================================================================

{json.dumps(tomcat, indent=2)}

===========================================================================
ORACLE METRICS
===========================================================================

{json.dumps(oracle, indent=2)}

===========================================================================
CORRELATION RESULTS
===========================================================================

{json.dumps(correlations, indent=2)}

===========================================================================
JMETER METRICS
===========================================================================

{json.dumps(jmeter, indent=2)}
"""

#         prompt = f"""

# You are a Senior Performance Engineer.

# Analyze the following performance evidence.

# Identify:

# 1. Primary bottleneck

# 2. Exact timeline

# 3. Root cause chain

# 4. Why user response time increased

# 5. Confidence (LOW/MEDIUM/HIGH)

# 6. Action items

# Return EXACTLY this JSON schema:

# {{
#     "summary": "",
#     "root_cause": "",
#     "primary_bottleneck": "",
#     "timeline": "",
#     "supporting_evidence": [],
#     "bottlenecks": [],
#     "recommendations": [],
#     "confidence": ""
# }}

# Do not add any other fields.
# Return only valid JSON.

# Configuration

# {json.dumps(configuration, indent=2)}


# Timeline

# {json.dumps(timeline_json, indent=2)}

# Apache

# {json.dumps(apache, indent=2)}

# Tomcat

# {json.dumps(tomcat, indent=2)}

# Oracle

# {json.dumps(oracle, indent=2)}

# Correlations

# {json.dumps(correlations, indent=2)}

# JMeter

# {json.dumps(jmeter, indent=2)}

# """

        return prompt