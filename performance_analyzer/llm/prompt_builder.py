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

        jmeter

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




        print("Timeline Type:", type(timeline))
        print("Apache Type:", type(apache))
        print("Tomcat Type:", type(tomcat))
        print("Oracle Type:", type(oracle))
        print("Correlations Type:", type(correlations))
        print("JMeter Type:", type(jmeter))

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

        prompt = f"""

You are a Senior Performance Engineer.

Analyze the following performance evidence.

Identify:

1. Primary bottleneck

2. Exact timeline

3. Root cause chain

4. Why user response time increased

5. Confidence (LOW/MEDIUM/HIGH)

6. Action items

Return EXACTLY this JSON schema:

{{
    "summary": "",
    "root_cause": "",
    "primary_bottleneck": "",
    "timeline": "",
    "supporting_evidence": [],
    "bottlenecks": [],
    "recommendations": [],
    "confidence": ""
}}

Do not add any other fields.
Return only valid JSON.

Timeline

{json.dumps(timeline_json, indent=2)}

Apache

{json.dumps(apache, indent=2)}

Tomcat

{json.dumps(tomcat, indent=2)}

Oracle

{json.dumps(oracle, indent=2)}

Correlations

{json.dumps(correlations, indent=2)}

JMeter

{json.dumps(jmeter, indent=2)}

"""

        return prompt