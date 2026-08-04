from performance_analyzer.llm.prompt_builder import PromptBuilder

from performance_analyzer.llm.llm_client import LLMClient


def sanitize_analysis(data):

    clean = {}

    for hostname, instances in data.items():

        clean[hostname] = {}

        for instance, analysis in instances.items():

            clean[hostname][instance] = {

                "timeline": analysis.get("timeline", []),

                "findings": analysis.get("findings", [])

            }

    return clean

class LLMRCAEngine:

    def __init__(self):

        self.prompt = PromptBuilder()

        self.client = LLMClient()

    def generate(

        self,

        timeline,

        apache,

        tomcat,

        oracle,

        correlations,

        jmeter

    ):
        apache = sanitize_analysis(apache)

        tomcat = sanitize_analysis(tomcat)

        oracle = sanitize_analysis(oracle)

        prompt = self.prompt.build(

            timeline,

            apache,

            tomcat,

            oracle,

            correlations,

            jmeter

        )

        report = self.client.generate(prompt)
        print("report", report)

        return report