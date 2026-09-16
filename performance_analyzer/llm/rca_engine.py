from performance_analyzer.llm.prompt_builder import PromptBuilder

from performance_analyzer.llm.llm_client import LLMClient
from performance_analyzer.summarizer.metrics_summary import MetricsSummary

class LLMRCAEngine:

    def __init__(self):

        self.prompt = PromptBuilder()

        self.client = LLMClient()
        # self.client = EnablerLLMClient(
        #     # flow_url="YOUR_AXET_URL",
        #     # bearer_token="YOUR_BEARER_TOKEN"
        # )

    def generate(

        self,
        timeline,
        apache,
        tomcat,
        oracle,
        correlations,
        jmeter,
        configuration,
        dashboard_summary

    ):
        apache_summary = MetricsSummary.summarize_apache(apache)
        tomcat_summary = MetricsSummary.summarize_tomcat(tomcat)
        oracle_summary = MetricsSummary.summarize_oracle(oracle)
        jmeter_summary = MetricsSummary.summarize_jmeter(jmeter)

        prompt = self.prompt.build(

            timeline,
            correlations,
            configuration,
            apache_summary,
            tomcat_summary,
            oracle_summary,
            jmeter_summary,
            dashboard_summary
        )

        report = self.client.generate(prompt)
        # print("from rca_engine report", report)

        return report