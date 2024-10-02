import models.Parser
class DateRange:
	def __init__(self, parser: models.Parser, text):
		self._parser = parser
		self._dateBegin = ""
		self._dateEnd = ""
		if not self._setDatesFromString(text):
			raise Exception("Not valid format dates")	

	def _setDatesFromString(self, dateString):
		try:
			listDates = self._parser.parse(dateString)
			#IN 'MM/DD/YY'
			self._dateBegin = listDates[0]
			self._timeBegin = listDates[1]
			#IN 'HH/MM/SS'
			self._dateEnd = listDates[2]
			self._timeEnd = listDates[3]	
		except Exception as e:
			print(e)
			return False

		return True

	def getDateBegin(self):
		return self._dateBegin

	def getTimeBegin(self):
		return self._timeBegin

	def getDateEnd(self):
		return self._dateEnd

	def getTimeEnd(self):
		return self._timeEnd

	def getDatesStringWithTime(self):
		form = "{} {} - {} {}"
		return form.format(self._dateBegin, self._timeEnd, self._dateEnd, self._timeEnd)