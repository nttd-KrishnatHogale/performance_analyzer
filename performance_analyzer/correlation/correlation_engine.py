from performance_analyzer.correlation.correlation_rules import CorrelationRules


class CorrelationEngine:

    def __init__(self):

        self.rules = CorrelationRules()

    def analyze(self, metrics_collection):

        correlations=[]

        jmeter=metrics_collection["jmeter"]

        for hostname,server in metrics_collection["servers"].items():

            cpu=server["cpu"]

            apache=list(server["apache"].values())[0]

            tomcat=list(server["tomcat"].values())[0]

            oracle=list(server["oracle"].values())[0]

            result=self.rules.cpu_vs_tomcat(cpu,tomcat)

            if result:
                correlations.append(result)

            result=self.rules.tomcat_vs_db(tomcat,oracle)

            if result:
                correlations.append(result)

            result=self.rules.db_vs_apache(oracle,apache)

            if result:
                correlations.append(result)

            result=self.rules.apache_vs_jmeter(apache,jmeter)

            if result:
                correlations.append(result)

        return correlations