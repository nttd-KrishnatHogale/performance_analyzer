from performance_analyzer.llm.prompt_builder import PromptBuilder

from performance_analyzer.llm.llm_client import LLMClient
from performance_analyzer.summarizer.metrics_summary import MetricsSummary


# from backend.configuration.server_configuration_collector import (
#     ServerConfigurationCollector)
# from backend.ssh.ssh_client import SSHClient

# ssh = SSHClient()

# configuration = ServerConfigurationCollector(
#         ssh
#     ).collect()


# def sanitize_analysis(data):

#     clean = {}

#     for hostname, instances in data.items():

#         clean[hostname] = {}

#         for instance, analysis in instances.items():

#             clean[hostname][instance] = {

#                 "timeline": analysis.get("timeline", []),

#                 "findings": analysis.get("findings", [])

#             }

#     return clean

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

        jmeter,
        configuration,
            dashboard_summary


    ):
        # apache = sanitize_analysis(apache)

        # tomcat = sanitize_analysis(tomcat)

        # oracle = sanitize_analysis(oracle)


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

            # apache,

            # tomcat,

            # oracle,
        )

        report = self.client.generate(prompt)
        print("report", report)

        return report