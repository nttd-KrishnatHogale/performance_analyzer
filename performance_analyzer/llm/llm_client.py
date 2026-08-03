# import json


# class LLMClient:

#     def generate(self, prompt):

#         #
#         # Replace this with actual LLM call
#         #

#         response = """

# {

# "summary":"CPU saturation caused Oracle slowdown",

# "root_cause":"CPU saturation increased Tomcat threads which increased Oracle SQL latency and finally Apache response time.",

# "timeline":"13:42 CPU spike -> 13:44 JDBC saturation -> 13:46 SQL latency -> 13:47 User latency",

# "bottlenecks":[

# "CPU",

# "Oracle",

# "Apache"

# ],

# "recommendations":[

# "Increase CPU",

# "Tune SQL",

# "Increase JDBC pool"

# ],

# "confidence":"HIGH"

# }

# """

#         return json.loads(response)

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

class LLMClient:

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set."
            )

        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt):

        response = self.client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Senior Performance Engineer specializing in "
                        "JMeter, Apache, Tomcat, Oracle, Linux, JVM, and "
                        "Performance Root Cause Analysis."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            response_format={"type": "json_object"},
        )

        return json.loads(
            response.choices[0].message.content
        )