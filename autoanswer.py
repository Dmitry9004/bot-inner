import subprocess, sys

subprocess.Popen(["powershell.exe", "-noexit", "-command", "\\\\eserv1\\C$\\'Program Files'\\Microsoft\\'Exchange Server'\\V14\\Bin\\Remote-test.ps1", "\\\\eserv1\\C$\\Soft\\TEST\\test.ps1"], stdout=sys.stdout).communicate()

# import paramiko, sys

# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect("storeserv", "volin.d", "dima8968!", 22, sys.stdin, sys.stdout, sys.stderr)
# data = sys.stdout.read() + sys.stderr.read()
# print(data)

# client.close()