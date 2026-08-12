import json
import requests
import  os
from dotenv import load_dotenv

load_dotenv()

class EnablerLLMClient:

    def __init__(self, axet_url=None, bearer_token=None):

        self.axet_url = axet_url or os.getenv("AXET_LLM_URL")
        self.bearer_token = (
            bearer_token
            or os.getenv("AXET_BEARER_TOKEN")
        )

        if not self.axet_url:
            raise ValueError("AXET_LLM_URL is not configured")

        if not self.bearer_token:
            raise ValueError("AXET_BEARER_TOKEN is not configured")

    def generate(self, prompt):

        payload = {
                    "prompt": prompt
                }
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            self.axet_url,
            json=payload,
            headers=headers,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        return result

#     def generate(self, prompt):

#         payload = {
#             "messages": [
#                 {
#                     "role": "system",
#                     "content": """
# You are a performance engineering RCA expert.

# Analyze the supplied performance data and generate
# a root cause analysis.

# Return ONLY valid JSON.

# Do not return markdown.
# Do not return ```json.
# Do not add text outside the JSON.

# Required fields:

# summary
# root_cause
# primary_bottleneck
# timeline
# supporting_evidence
# rejected_hypotheses
# bottlenecks
# recommendations
# confidence
# """
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],

#             "max_tokens": 4000,
#             "temperature": 0.2,
#             "top_p": 1.0,
#             "n": 1
#         }

#         response = requests.post(
#             self.flow_url,
#             json=payload,
#             timeout=300
#         )

#         response.raise_for_status()

#         result = response.json()

#         # AXET enabler-llm output
#         llm_output = result.get("payload")

#         if llm_output is None:
#             raise ValueError(
#                 "AXET response does not contain msg.payload"
#             )

#         # If payload is already a dictionary
#         if isinstance(llm_output, dict):
#             return llm_output

#         # If payload is JSON string
#         if isinstance(llm_output, str):

#             llm_output = llm_output.strip()

#             # Remove accidental markdown wrapper
#             if llm_output.startswith("```json"):
#                 llm_output = llm_output[7:]

#             if llm_output.startswith("```"):
#                 llm_output = llm_output[3:]

#             if llm_output.endswith("```"):
#                 llm_output = llm_output[:-3]

#             llm_output = llm_output.strip()

#             return json.loads(llm_output)

#         raise TypeError(
#             f"Unexpected AXET payload type: "
#             f"{type(llm_output)}"
#         )