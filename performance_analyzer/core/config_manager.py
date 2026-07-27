import yaml


class ConfigManager:

    def __init__(self, config_path):

        with open(config_path, "r") as f:
            self.raw_config = yaml.safe_load(f)

        self.servers = {}
        self.instances = {}
        self.flows = {}

        self._parse_servers()
        self._parse_instances()
        self._parse_flows()

    # ============================================================
    # Parse Servers
    # ============================================================
    def _parse_servers(self):

        for server in self.raw_config.get("servers", []):
            hostname = server["hostname"]

            self.servers[hostname] = {
                "apache": [],
                "tomcat": [],
                "oracle": []
            }

    # ============================================================
    # Parse Instances
    # ============================================================
    def _parse_instances(self):

        for server in self.raw_config.get("servers", []):

            hostname = server["hostname"]

            # Apache
            for apache in server.get("apache", []):
                instance = apache["instance"]

                key = f"{hostname}::apache::{instance}"

                self.instances[key] = {
                    "type": "apache",
                    "hostname": hostname,
                    "instance": instance
                }

                self.servers[hostname]["apache"].append(instance)

            # Tomcat
            for tomcat in server.get("tomcat", []):
                instance = tomcat["instance"]

                key = f"{hostname}::tomcat::{instance}"

                self.instances[key] = {
                    "type": "tomcat",
                    "hostname": hostname,
                    "instance": instance
                }

                self.servers[hostname]["tomcat"].append(instance)

            # Oracle
            for db in server.get("oracle", []):
                sid = db["sid"]

                key = f"{hostname}::oracle::{sid}"

                self.instances[key] = {
                    "type": "oracle",
                    "hostname": hostname,
                    "sid": sid
                }

                self.servers[hostname]["oracle"].append(sid)

    # ============================================================
    # Parse Flows
    # ============================================================
    def _parse_flows(self):

        for flow in self.raw_config.get("architecture", []):

            flow_id = flow["flow_id"]

            self.flows[flow_id] = {
                "web": {
                    "hostname": flow["web"]["hostname"],
                    "instance": flow["web"]["instance"]
                },
                "app": {
                    "hostname": flow["app"]["hostname"],
                    "instance": flow["app"]["instance"]
                },
                "db": {
                    "hostname": flow["db"]["hostname"],
                    "sid": flow["db"]["sid"]
                }
            }

    # ============================================================
    # Utility Functions
    # ============================================================

    def get_apache_instances(self):
        return {k: v for k, v in self.instances.items() if v["type"] == "apache"}

    def get_tomcat_instances(self):
        return {k: v for k, v in self.instances.items() if v["type"] == "tomcat"}

    def get_oracle_instances(self):
        return {k: v for k, v in self.instances.items() if v["type"] == "oracle"}

    def print_summary(self):

        print("\n===== CONFIG SUMMARY =====\n")

        print("Servers:")
        for s in self.servers:
            print(f" - {s}")

        print("\nInstances:")
        for k, v in self.instances.items():
            print(f" - {k}")

        print("\nFlows:")
        for f, v in self.flows.items():
            print(f" - {f}: {v}")

        print("\n==========================\n")