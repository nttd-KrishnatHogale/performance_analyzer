import json
import re
import xml.etree.ElementTree as ET
from backend.ssh.ssh_client import SSHClient


class ServerConfigurationCollector:

    def __init__(self, ssh_client):
        self.ssh = ssh_client

    def collect(self):

        # print("=" * 80)
        # print("COLLECTING SERVER CONFIGURATION")
        # print("=" * 80)

        self.ssh.connect()

        configuration = {
            "apache": self.get_apache_configuration(),
            "tomcat": self.get_tomcat_configuration(),
            "jdbc": self.get_jdbc_configuration(),
            "jvm": self.get_jvm_configuration()
        }

        self.ssh.close()

        # print("\nCollected Configuration")
        # print(json.dumps(configuration, indent=4))

        return configuration

    #####################################################################
    # Apache
    #####################################################################

    def get_apache_configuration(self):

        # print("\nReading Apache Configuration...")

        command = """
grep -E 'ServerLimit|MaxClients|MaxRequestWorkers|KeepAlive|KeepAliveTimeout|MaxKeepAliveRequests|MaxRequestsPerChild' /etc/httpd/conf/httpd.conf
"""

        output = self.ssh.execute_command(command)

        # print("\nApache Raw Output")
        # print(output)

        apache = {}

        for line in output.splitlines():

            line = line.strip()

            if not line:
                continue

            parts = line.split(None, 1)

            if len(parts) == 2:
                apache[parts[0]] = parts[1]

        # print("\nApache Parsed Configuration")
        # print(apache)

        return apache

    #####################################################################
    # Tomcat
    #####################################################################

    def get_tomcat_configuration(self):

        # print("\nReading Tomcat server.xml...")

        xml = self.ssh.execute_command(
            'sudo su - tomcat -c "cat /home/tomcat/tomcat-7.0.109/conf/server.xml"'
        )

        # print("\nTomcat XML")
        # print(xml)

        connector = {}

        try:

            root = ET.fromstring(xml)

            for node in root.iter("Connector"):

                protocol = node.attrib.get("protocol", "")

                if "AJP" in protocol or "HTTP" in protocol:

                    connector = {

                        "port": node.attrib.get("port"),

                        "protocol": protocol,

                        "maxThreads":
                                        node.attrib.get("maxThreads")
                                        or node.attrib.get("MaxThreads"),

                        "acceptCount": node.attrib.get("acceptCount"),

                        "connectionTimeout": node.attrib.get("connectionTimeout"),

                        "redirectPort": node.attrib.get("redirectPort")
                    }

                    break

        except Exception as e:
            print("Unable to parse server.xml")
            print(e)

        # print("\nTomcat Parsed Configuration")
        # print(connector)

        return connector

    #####################################################################
    # JDBC
    #####################################################################

    def get_jdbc_configuration(self):

        # print("\nReading JDBC Context...")

        xml = self.ssh.execute_command(
           'sudo su - tomcat -c "cat /home/tomcat/tomcat-7.0.109/webapps/jpetstore/META-INF/context.xml"'
        )

        # print("\nJDBC XML")
        # print(xml)

        jdbc = {}

        try:

            root = ET.fromstring(xml)

            for node in root.iter("Resource"):

                jdbc = {

                    "name": node.attrib.get("name"),

                    "maxActive": node.attrib.get("maxActive"),

                    "maxIdle": node.attrib.get("maxIdle"),

                    "maxWait": node.attrib.get("maxWait"),

                    "initialSize": node.attrib.get("initialSize")
                }

                break

        except Exception as e:
            print("Unable to parse context.xml")
            print(e)

        # print("\nJDBC Parsed Configuration")
        # print(jdbc)

        return jdbc

    #####################################################################
    # JVM
    #####################################################################

    def get_jvm_configuration(self):

        print("\nReading JVM Configuration...")

        text = self.ssh.execute_command(
            'sudo su - tomcat -c "cat /home/tomcat/tomcat-7.0.109/bin/setenv.sh"'
        )

        # print("\nsetenv.sh")
        # print(text)

        jvm = {}

        xms = re.search(r"-Xms(\S+)", text)

        if xms:
            jvm["Xms"] = xms.group(1)

        xmx = re.search(r"-Xmx(\S+)", text)

        if xmx:
            jvm["Xmx"] = xmx.group(1)

        if "UseG1GC" in text:
            jvm["GC"] = "G1GC"

        elif "UseParallelGC" in text:
            jvm["GC"] = "ParallelGC"

        elif "UseConcMarkSweepGC" in text:
            jvm["GC"] = "CMS"

        else:
            jvm["GC"] = "Unknown"

        # print("\nJVM Parsed Configuration")
        # print(jvm)

        return jvm