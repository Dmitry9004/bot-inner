from config.Config import Config
from pypsrp.client import Client

SERVER_NAME = "serv-name"
USERNAME 	= "username"
PASSWORD 	= "password"

class UserDAO:
	def __init__(self, cfg: Config):
		serv = cfg.getAttribute(SERVER_NAME)
		if serv == "":
			raise Exception("Not valid server name")

		username = cfg.getAttribute(USERNAME)
		if username == "":
			raise Exception("Not valid usernmae")

		password = cfg.getAttribute(PASSWORD)
		if password == "":
			raise Exception("Not valid password")


		self.__client = Client(serv, username=username,
	              password=password,
	              cert_validation=False, 
	              ssl=False)

		self.__cfg = cfg

	#
	#REPLACE BY GET AD USER AND GET PROPERTIES, CONSTRUCTOR REQUESTS!!!!!
	#

	def getUsername(self, usernameEx: str):
		attribute = "extensionAttribute12"

		script = script = f"Get-ADuser -Filter '{attribute} -eq \"{usernameEx}\"' | Select SamAccountName | Format-List"
		output, strin, err = self.__client.execute_ps(script)

		username = output.split(" : ")
		if err or len(username) != 2:
			return ""

		return username[1].strip()		

		#переделать, оставить только username из ad, телеграмм только доп.
	def getVPNUsername(self, username: str):
		attribute = "extensionAttribute13"
		script = script = f"Get-ADuser {username} -Properties {attribute} | Select {attribute} | Format-List"
		output, strin, err = self.__client.execute_ps(script)

		if err: return ""

		print(output)

		return self.__getAttributeValue(output)
	
	def getUserPC(self, username: str):
		script = f"""Get-ADComputer -Filter "ManagedBy -eq '{username}'" | Select Name | Format-List """
		output, streams, err = self.__client.execute_ps(script)

		if err: return ""

		print(output)
		
		return self.__getAttributeValue(output)		

	def __getAttributeValue(self, attribute: str):
		value = attribute.split(" : ")
		if len(value) != 2:
			return ""

		return value[1].strip()