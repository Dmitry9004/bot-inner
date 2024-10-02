from models.AutoAnswer import AutoAnswer
from models.DateParser import DateParser
from config.Config import Config
import subprocess, sys, os
from pypsrp.client import Client

POWERSHELL = "powershell"

SERVER_NAME = "serv-name"
USERNAME 	= "username"
PASSWORD 	= "password"

class AutoAnswerService:

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

		self.__client = Client("eserv1.nt351.a1tis.ru", username="nt351\\"+username,
	              password=password,
	              cert_validation=False, 
	              ssl=False)

	def setAutoAnswer(self, autoAnswer: AutoAnswer, parser: DateParser):
		parsedDateFrom = parser.toADFormat(autoAnswer.getDateBegin(), autoAnswer.getTimeBegin())
		parsedDateTo   = parser.toADFormat(autoAnswer.getDateEnd(), autoAnswer.getTimeEnd()) 

		# nameScript = "./app/scripts/auto-answer-en.ps1"

		script = 'powershell "& ""C:\\TEST\\auto-answer-en.ps1 \'{}\' \'{}\' \'{}\' \'{}\' {}"""'
		execScript = script.format(parsedDateFrom, parsedDateTo, autoAnswer.getFullMessage(), autoAnswer.getFullMessage(), autoAnswer.getUsername())
		
		return self.__client.execute_ps(execScript)[2]

	def offAutoAnswer(self, username: str):
		# nameScript = "./app/scripts/auto-answer-off.ps1 {}" 
 		script = 'powershell "& ""C:\\TEST\\auto-answer-off.ps1""" {}'
 		execScript = script.format(username)

 		return self.__client.execute_ps(execScript)[2]

	def getData(self, username: str):
		# nameScript = "./app/scripts/auto-answer-data.ps1"
		script = 'powershell "& ""C:\\TEST\\auto-answer-data.ps1""" {}'
		execScript = script.format(username)
		
		res = self.__client.execute_ps(execScript)[0]
		mode = res.split(":")
		return { mode[0]: mode[1].strip() }



	# def __exec(self, script: str, args: str):
	# 	try:
	# 		stdout, err = subprocess.Popen([POWERSHELL, script, args], stdout=subprocess.PIPE).communicate()

	# 		if err != None or stdout.decode('windows-1251') != "":
	# 			raise Exception("Not valid data")

	# 		return True
	# 	except Exception as e: 
	# 		print(e)
	# 		return False


	# def __execWithData(self, script: str, args: str):
	# 	try:
	# 		stdout, err = subprocess.Popen([POWERSHELL, script, args], stdout=subprocess.PIPE).communicate()

	# 		autoReplyState = stdout.decode("windows-1251").split(":")
	# 		print(autoReplyState)
	# 		if err != None or len(autoReplyState) != 2:
	# 			raise Exception("Not valid data")

	# 		return { "autoReplyState": autoReplyState[1].strip() }
	# 	except Exception as e:
	# 		print(e)
	# 		return { "autoReplyState": "" }
