from datetime import datetime, timedelta
from models.Parser import Parser
from models.DateRange import DateRange

class DateParser(Parser):

	def parse(self, datesString):
		res = datesString.split(" - ")
		dateBeginArr = res[0].split(" ")
		dateEndArr   = res[1].split(" ")

		dateBegin = dateBeginArr[0].split(".")
		dateEnd = dateEndArr[0].split(".")

		resTimeBegin = dateBeginArr[1]
		resTimeEnd = dateEndArr[1]

		if not self.__isValidDates(dateBegin, dateEnd, resTimeBegin, resTimeEnd):
			raise Exception("Not valid dates")

		resBegin = dateBegin[0] + "." + dateBegin[1] + "." + dateBegin[2]
		resEnd   = dateEnd[0] + "." + dateEnd[1] + "." + dateEnd[2]

		return [resBegin, resTimeBegin, resEnd, resTimeEnd]

	def toADFormat(self, date, time):
		date = date.split(".")
		resDate = date[1] + "/" + date[0] + "/" + date[2] + " " + time

		return resDate

	def __isValidDates(self, numsBegin, numsEnd, timeBegin, timeEnd):
		resBegin = filter(str.isdigit, numsBegin)
		resEnd   = filter(str.isdigit, numsEnd)

		if len(list(resBegin)) != 3 or len(list(resEnd)) != 3:
			return False

		dateBegin = datetime.strptime(numsBegin[0]+numsBegin[1]+numsBegin[2]+" "+timeBegin, "%d%m%Y %H:%M:%S")
		dateEnd   = datetime.strptime(numsEnd[0]+numsEnd[1]+numsEnd[2]+" "+timeEnd, "%d%m%Y %H:%M:%S")

		print(dateBegin)
		print(dateEnd)
		print(datetime.now())
		if dateBegin >= dateEnd or dateEnd <= datetime.now():
			return False

		return True
		# ADD IF  
