# from performance_analyzer.correlation.correlation_rules import CorrelationRules


# class CorrelationEngine:

#     def __init__(self):
#         self.rules = CorrelationRules()

#     def analyze( 
#         self,
#         metrics_collection,
#         apache_analysis,
#         tomcat_analysis,
#         oracle_analysis):

#         correlations=[]

#         jmeter=metrics_collection["jmeter"]

#         for hostname,server in metrics_collection["servers"].items():

#             # cpu=server["cpu"]

#             # apache=list(server["apache"].values())[0]

#             # tomcat=list(server["tomcat"].values())[0]

#             # oracle=list(server["oracle"].values())[0]

#             cpu = server["cpu"]

#             apache = apache_analysis.get(hostname, {})

#             tomcat = tomcat_analysis.get(hostname, {})

#             oracle = oracle_analysis.get(hostname, {})

#             result=self.rules.cpu_vs_tomcat(cpu,tomcat)

#             if result:
#                 correlations.append(result)

#             result=self.rules.tomcat_vs_db(tomcat,oracle)

#             if result:
#                 correlations.append(result)

#             result=self.rules.db_vs_apache(oracle,apache)

#             if result:
#                 correlations.append(result)

#             result=self.rules.apache_vs_jmeter(apache,jmeter)

#             if result:
#                 correlations.append(result)

#         return correlations
from performance_analyzer.correlation.correlation_rules import CorrelationRules


class CorrelationEngine:

    def __init__(self):
        self.rules = CorrelationRules()

    def analyze(
        self,
        metrics_collection,
        apache_analysis,
        tomcat_analysis,
        oracle_analysis
    ):

        correlations = []

        jmeter = metrics_collection["jmeter"]

        for hostname, server in metrics_collection["servers"].items():

            cpu = server.get("cpu")

            apache_instances = apache_analysis.get(hostname, {})
            tomcat_instances = tomcat_analysis.get(hostname, {})
            oracle_instances = oracle_analysis.get(hostname, {})

            # ------------------------------
            # CPU -> Tomcat
            # ------------------------------
            for _, tomcat_result in tomcat_instances.items():

                result = self.rules.cpu_vs_tomcat(
                    cpu,
                    tomcat_result
                )

                if result:
                    correlations.append(result)

            # ------------------------------
            # Tomcat -> Oracle
            # ------------------------------
            for _, tomcat_result in tomcat_instances.items():

                for _, oracle_result in oracle_instances.items():

                    result = self.rules.tomcat_vs_db(
                        tomcat_result,
                        oracle_result
                    )

                    if result:
                        correlations.append(result)

            # ------------------------------
            # Oracle -> Apache
            # ------------------------------
            for _, oracle_result in oracle_instances.items():

                for _, apache_result in apache_instances.items():

                    result = self.rules.db_vs_apache(
                        oracle_result,
                        apache_result
                    )

                    if result:
                        correlations.append(result)

            # ------------------------------
            # Apache -> JMeter
            # ------------------------------
            for _, apache_result in apache_instances.items():

                result = self.rules.apache_vs_jmeter(
                    apache_result,
                    jmeter
                )

                if result:
                    correlations.append(result)

        return correlations