import json
from dataclasses import asdict



from dataclasses import asdict, is_dataclass

def serialize(obj):
    if is_dataclass(obj):
        return asdict(obj)
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)

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

Return JSON only.

Timeline

{json.dumps(timeline_json, indent=2, default=str)}

Apache

{json.dumps(apache, indent=2, default=serialize)}

Tomcat

{json.dumps(tomcat, indent=2, default=serialize)}

Oracle

{json.dumps(oracle, indent=2, default=serialize)}

Correlations

{json.dumps(correlations, indent=2, default=serialize)}

JMeter

{json.dumps(jmeter, indent=2, default=serialize)}

"""

        return prompt