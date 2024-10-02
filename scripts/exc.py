from pypsrp.wsman import WSMan
from pypsrp.powershell import PowerShell, RunspacePool
from pypsrp.client import Client

user = "nt351\\ituser"
password = "22021870"

wsman = Client("eserv1.nt351.a1tis.ru", username=user,
	              password=password,
	              cert_validation=False, 
	              ssl=False)

print(wsman.execute_ps('powershell "& ""C:\\TEST\\auto-answer-data.ps1 volin.d"""')[0])