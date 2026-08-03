from performance_analyzer.llm.prompt_builder import PromptBuilder

from performance_analyzer.llm.llm_client import LLMClient


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

        prompt = self.prompt.build(

            timeline,

            apache,

            tomcat,

            oracle,

            correlations,

            jmeter

        )

        report = self.client.generate(prompt)

        return report