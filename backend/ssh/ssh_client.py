# import paramiko

# from config.config_service import ConfigService
# from backend.utils.logger import Logger


# class SSHClient:

#     def __init__(self):

#         self.logger = Logger.get_logger()
#         self.config = ConfigService()

#         self.client = None

#     def connect(self):

#         self.client = paramiko.SSHClient()

#         self.client.set_missing_host_key_policy(
#             paramiko.AutoAddPolicy()
#         )

#         self.client.connect(
#             hostname=self.config.get("application.ssh.host"),
#             username=self.config.get("application.ssh.username"),
#             key_filename=self.config.get("application.ssh.pem_file")
#         )

#         self.logger.info("SSH Connected")

#     def execute_command(self, command):

#         stdin, stdout, stderr = self.client.exec_command(command)

#         return (
#             stdout.read().decode(),
#             stderr.read().decode()
#         )

#     def upload(self, local_file, remote_file):

#         sftp = self.client.open_sftp()

#         sftp.put(local_file, remote_file)

#         sftp.close()

#     def download(self, remote_file, local_file):

#         sftp = self.client.open_sftp()

#         sftp.get(remote_file, local_file)

#         sftp.close()

#     def close(self):

#         if self.client:

#             self.client.close()

#             self.logger.info("SSH Connection Closed")
# import paramiko

# from config.config_service import ConfigService
# from backend.utils.logger import Logger


# class SSHClient:

#     def __init__(
#         self,
#         host=None,
#         username=None,
#         password=None,
#         key_file=None,
#         port=22
#     ):

#         self.logger = Logger.get_logger()
#         self.config = ConfigService()

#         self.host = host or self.config.get("application.host")
#         self.username = username or self.config.get("application.ssh.username")
#         self.password = password
#         self.key_file = key_file or self.config.get("application.ssh.pem_file")
#         self.port = port

#         self.client = None

#     ########################################################

#     def connect(self):
#         print("Inside SSHClient.connect()")
#         self.client = paramiko.SSHClient()
#         print("SSHClient created")
#         self.client.set_missing_host_key_policy(
#             paramiko.AutoAddPolicy()
#         )

#         self.logger.info(f"Connecting to {self.host}")
#         print("Connecting to server...")
#         if self.key_file:

#             self.client.connect(
#                 hostname=self.host,
#                 port=self.port,
#                 username=self.username,
#                 key_filename=self.key_file,
#                 timeout=15
#             )

#         else:

#             self.client.connect(
#                 hostname=self.host,
#                 port=self.port,
#                 username=self.username,
#                 password=self.password,
#                 timeout=15
#             )

#         self.logger.info("SSH Connected")

#     ########################################################

#     def execute_command(self, command):

#         self.logger.info(f"Executing: {command}")

#         stdin, stdout, stderr = self.client.exec_command(command)

#         output = stdout.read().decode()

#         error = stderr.read().decode()

#         if error.strip():
#             self.logger.warning(error)

#         return output

#     ########################################################

#     def upload(self, local_file, remote_file):

#         sftp = self.client.open_sftp()

#         sftp.put(local_file, remote_file)

#         sftp.close()

#     ########################################################

#     def download(self, remote_file, local_file):

#         sftp = self.client.open_sftp()

#         sftp.get(remote_file, local_file)

#         sftp.close()

#     ########################################################

#     def close(self):

#         if self.client:

#             self.client.close()

#             self.logger.info("SSH Connection Closed")

import subprocess

from config.config_service import ConfigService
from backend.utils.logger import Logger


class SSHClient:

    def __init__(
        self,
        host=None,
        username=None,
        password=None,
        key_file=None,
        port=22

    ):
       

        self.logger = Logger.get_logger()
        self.config = ConfigService()

        self.host = host or self.config.get("application.host")
        self.username = username or self.config.get("application.ssh.username")
        self.key_file = key_file or self.config.get("application.ssh.pem_file")
        self.port = port

        # Path to OpenSSH
        self.ssh_exe = r"C:\OpenSSH-Win32\OpenSSH-Win32\ssh.exe"

    ##################################################

    def connect(self):

        self.logger.info(f"SSH Ready for {self.host}")

    ##################################################

    def execute_command(self, command):

        ssh_command = [

            self.ssh_exe,

            "-o", "HostKeyAlgorithms=+ssh-rsa",

            "-o", "PubkeyAcceptedAlgorithms=+ssh-rsa",

            "-i", self.key_file,

            f"{self.username}@{self.host}",

            command

        ]

        self.logger.info("Executing command:")
        self.logger.info(command)

        result = subprocess.run(

            ssh_command,

            capture_output=True,

            text=True

        )

        if result.stderr.strip():

            print("SSH ERROR:")
            print(result.stderr)

        return result.stdout

    ##################################################

    def close(self):

        self.logger.info("SSH Closed")