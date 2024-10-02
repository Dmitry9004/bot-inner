from models.DateRange import DateRange
from models.Parser import Parser 

class AutoAnswer:
	
	def __init__(self):
		self.__userId = ""
		self.__dateRange = ""
		self.__replaceContent = ""
		self.__username = ""
		self.__fullMessage = ""
		self.__active = ""

	def setUserId(self, id):
		self.__userId = id

	def setDateRange(self, dateRange: DateRange):
		self.__dateRange = dateRange

	def setReplaceContent(self, content):
		self.__replaceContent = content

	def setFullMessage(self, message):
		self.__fullMessage = message

	def setUsername(self, username):
		self.__username = username

	def getDateRange(self):
		return self.__dateRange;

	def getDateBegin(self):
		return self.__dateRange.getDateBegin()

	def getDateEnd(self):
		return self.__dateRange.getDateEnd()

	def getTimeBegin(self):
		return self.__dateRange.getTimeBegin()

	def getTimeEnd(self):
		return self.__dateRange.getTimeEnd()

	def getReplaceContent(self):
		return self.__replaceContent

	def getFullMessage(self):
		return self.__fullMessage

	def getUsername(self):
		return self.__username
	def getActive(self):
		return self.__active
	def setActive(self, act):
		self.__active = act