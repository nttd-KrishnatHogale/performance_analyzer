# import paramiko


# class SSHClient:

#     def __init__(
#         self,
#         host,
#         username,
#         password=None,
#         key_file=None,
#         port=22
#     ):

#         self.host = host
#         self.username = username
#         self.password = password
#         self.key_file = key_file
#         self.port = port

#         self.client = None

#     def connect(self):

#         self.client = paramiko.SSHClient()

#         self.client.set_missing_host_key_policy(
#             paramiko.AutoAddPolicy()
#         )

#         if self.key_file:

#             self.client.connect(
#                 hostname=self.host,
#                 username=self.username,
#                 key_filename=self.key_file,
#                 port=self.port
#             )

#         else:

#             self.client.connect(
#                 hostname=self.host,
#                 username=self.username,
#                 password=self.password,
#                 port=self.port
#             )

#     def execute(self, command):

#         stdin, stdout, stderr = self.client.exec_command(command)

#         error = stderr.read().decode()

#         if error.strip():
#             print(error)

#         return stdout.read().decode()

#     def close(self):

#         if self.client:
#             self.client.close()