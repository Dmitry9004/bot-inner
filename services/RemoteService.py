from config.Config import Config
from dao.UserDAO import UserDAO
from services.RouterService import RouterService
import re
import subprocess

TEMPLATE_PATH = "client-vpn.py"
FILE_PATH = "vpn.py"
EXEC_FILE_PATH = "dist\\vpn.exe"

class RemoteService:
	def __init__(self, cfg: Config, userDAO: UserDAO, routerService: RouterService):
		self.__cfg = cfg
		self.__userDAO = userDAO
		self.__routerService = routerService

	def getVPNFile(self, adUsername: str):
		vpnUsername = self.__userDAO.getVPNUsername(adUsername)
		print(vpnUsername)
		user = self.__routerService.getVPNUser(vpnUsername)

		# constrcution with ...
		f = open(TEMPLATE_PATH, "r")
		templateFile = f.read()
		f.close()

		pcName = self.__userDAO.getUserPC(adUsername)

		templateFile = templateFile.replace("?srv?", self.__cfg.getAttribute("vpn-server"))
		templateFile = templateFile.replace("?vpn-usr?", user[4])
		templateFile = templateFile.replace("?usr?", adUsername)
		templateFile = templateFile.replace("?psw?", user[2])
		templateFile = templateFile.replace("?ip?", user[0])
		templateFile = templateFile.replace("?pcName?", pcName)
		templateFile = templateFile.replace("?key?", self.__cfg.getAttribute("key"))

		resFile = open(FILE_PATH, "w")
		resFile.write(templateFile)
		resFile.close()

		# another class
		out = subprocess.Popen("pyinstaller --noconfirm --onefile --windowed D:\\tests\\vpn.py", stdout=subprocess.PIPE).communicate()

		return EXEC_FILE_PATH