import paramiko

from config.config_service import ConfigService
from backend.utils.logger import Logger


class SSHClient:

    def __init__(self):

        self.logger = Logger.get_logger()
        self.config = ConfigService()

        self.client = None

    def connect(self):

        self.client = paramiko.SSHClient()

        self.client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        self.client.connect(
            hostname=self.config.get("application.ssh.host"),
            username=self.config.get("application.ssh.username"),
            key_filename=self.config.get("application.ssh.pem_file")
        )

        self.logger.info("SSH Connected")

    def execute_command(self, command):

        stdin, stdout, stderr = self.client.exec_command(command)

        return (
            stdout.read().decode(),
            stderr.read().decode()
        )

    def upload(self, local_file, remote_file):

        sftp = self.client.open_sftp()

        sftp.put(local_file, remote_file)

        sftp.close()

    def download(self, remote_file, local_file):

        sftp = self.client.open_sftp()

        sftp.get(remote_file, local_file)

        sftp.close()

    def close(self):

        if self.client:

            self.client.close()

            self.logger.info("SSH Connection Closed")