# from backend.configuration.server_configuration_collector import (
#     ServerConfigurationCollector
# )

# from backend.configuration.jmeter_config import JMeterConfig

# server_config = ServerConfigurationCollector().collect(

#     host="10.31.4.84",

#     username="ec2-user",

#     key_file="C:/KrishnatHOgale/PerformancePlatform/backend/keys/key-for-training 1.pem"
    
# )

# jmeter_config = JMeterConfig().collect(

#     users=300,

#     ramp_up=60,

#     duration=300,

#     loops="Forever"

# )

# test_configuration = {

#     "server": server_config,

#     "jmeter": jmeter_config

# }

# print(test_configuration)

# from backend.ssh.ssh_client import SSHClient
# from backend.configuration.server_configuration_collector import ServerConfigurationCollector

# ssh = SSHClient()

# collector = ServerConfigurationCollector(ssh)

# config = collector.collect()

# print(config)