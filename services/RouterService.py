import netmiko
from netmiko import ConnectHandler
import re

class RouterService:
	def __init__(self):
		#from server
		mk = {
			"device_type":"mikrotik_routeros",
			"username": "admin",
			"password": "CjabKjhty783",
			"host": "l2tp.a1tis.ru",
			"port": 22
		}

		self.__cli = ConnectHandler(**mk)
		print(self.__cli.find_prompt())

	def __getUser(self, user):
		#can use regexp
		print(user)
		userArr = []
		itemIndex = 0
		index = len(user)-1
		item = "" 
		while(itemIndex < 5 and index >= 0):
			if (user[index] == " "):
				while(user[index] == " "):
					index = index-1
				userArr.append(item)
				item = ""
				itemIndex = itemIndex+1

			item = user[index]+item
			index = index-1

		print(userArr)
		return userArr

	def getVPNUser(self, vpnUsername: str):
		#[ip, profile, password, vpn_type, login]
		return self.__getUser(self.__cli.send_command(f"/ppp/secret/print where name={vpnUsername}"))
