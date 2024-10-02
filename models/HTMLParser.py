import re
from models.Parser import Parser
from models.AutoAnswer import AutoAnswer

HEAD_HELLO = "Добрый день!"
PERIOD = "C {} по {} не буду иметь доступ к почте."

EMAIL_PATTERN = "[\w]*[.]*[\w]*@a1tis.ru"
SEPARATOR = "#S!"

class HTMLParser(Parser):

	def __init__(self, answer: AutoAnswer):
		self.__content = "";
		self.__answer = answer

	def getContent(self):
		self.__content = "<p>"
	    
		self.__content += HEAD_HELLO + "<br>"
	    
		dateBegin = self.__answer.getDateBegin()
		dateEnd = self.__answer.getDateEnd()
		self.__content += PERIOD.format(dateBegin, dateEnd) + "<br>"

		replaceContent = self.__answer.getReplaceContent()

		emails = re.findall(EMAIL_PATTERN, replaceContent)
		if len(emails) != 0:	    
			replaceContent = re.sub(EMAIL_PATTERN, '{}', replaceContent)
			resEmailsRef = []
			for em in emails:
				a = "<a href = 'mailto:{}'>{}</a>"
				resEmailsRef.append(a.format(em, em))
			replaceContent = replaceContent.format(*resEmailsRef)

		self.__content += replaceContent
		self.__content += "</p>"
		return self.__content; 