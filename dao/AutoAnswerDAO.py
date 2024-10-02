import sqlite3
from models.AutoAnswer import AutoAnswer
import datetime
from models.DateRange import DateRange
from models.DateParser import DateParser

class AutoAnswerDAO:

	def __init__(self):
		self.__conn = sqlite3.connect("auto_answers.db")
		self.__cursor = self.__conn.cursor()

	def getByUsername(self, username):
		qu = "SELECT * FROM auto_answers WHERE username = '{}';"
		self.__cursor.execute(qu.format(username))		

		userAutoAnswer = self.__cursor.fetchone()

		if len(userAutoAnswer) == 0:
			return "";

		resAutoAnswer = AutoAnswer()
		resAutoAnswer.setDateRange(DateRange(DateParser(), userAutoAnswer[2]))
		resAutoAnswer.setFullMessage(userAutoAnswer[3])
		resAutoAnswer.setUsername(userAutoAnswer[1])
		resAutoAnswer.setActive(userAutoAnswer[4])

		return resAutoAnswer

	def insert(self, autoAnswer: AutoAnswer):
		qu = '''INSERT INTO auto_answers (username, dates, content, active, updated_at) 
				VALUES ('{}', '{}', '{}', {}, '{}') '''

		quWithArgs = qu.format(autoAnswer.getUsername(), autoAnswer.getDateRange().getDatesStringWithTime(), autoAnswer.getFullMessage(), autoAnswer.getActive(), datetime.datetime.now())
		self.__cursor.execute(quWithArgs)
		self.__conn.commit()
