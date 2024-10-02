from pypsrp.client import Client

import subprocess, sys, os
import asyncio
import logging
import models
import sqlite3

import io

from models.DateRange import DateRange
from models.AutoAnswerStatesGroup import AutoAnswerStatesGroup as AutoAnswerState
from models.AutoAnswer import AutoAnswer
from models.DateParser import DateParser
from models.HTMLParser import HTMLParser
from services.AutoAnswerService import AutoAnswerService
from services.RemoteService import RemoteService
from dao.AutoAnswerDAO import AutoAnswerDAO
from dao.UserDAO import UserDAO
from config.Config import Config
from models.Manual import Manual
from services.RouterService import RouterService

from middleware.AuthMiddleware import AuthMiddleware

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

AUTOANSWER_MODE = {
	"Disabled" : "выключен",
	"Scheduled": "включен",
	"Enabled"  : "включен",
}
AUTOANSWER_DO = "Укажите, что бы вы хотели сделать"
AUTOANSWER_HINT = "Выберите действие"
# CONFIG NAMES
SECURE_TOKEN = "secure-token"

#PRIMARY CONSTANTS MESSAGES
HELLO_MESSAGE = "С помощью этого бота вы можете устaновить автоответ, а также узнать решения других проблемах"
LOGIN_MESSAGE = "Укажите ваш логин \n(пример: pupkin.name)"
DATE_MESSAGE = "Укажите время автоответа в формате дд.мм.гг чч:мм:cc - дд.мм.гг чч:мм:сс \n (пример: 22.05.2024 17:00:00 - 22.06.2024 19:00:00)"
REPLACE_MESSAGE = "Укажите замещающего сотрудника или номер телефона: \n (пример: Замещающий менджер Анатолий Петров petrov.a@a1tis.ru)\n НЕ указывайте даты и приветствие!"
AUTOANSWER_ON_SUCCESS = "Автоответ установлен!"
AUTOANSWER_FAILED = "Что-то пошло не так..."
AUTOANSWER_OFF_SUCCESS = "Автоответ отключен!"
#ADDITIONAL CONST
HINT = "Укажите проблему"
NOT_FOUND_USERNAME = "Для того чтобы использовать бота, нужно отправить ваш username на почту ИТ"
#ERRORS MESSAGES CONST
NOT_VALID_DATES_ERROR = "Неправильный формат дат или недействительный диапазон"

dp = Dispatcher()

cfg = Config("config.env")
userDAO = UserDAO(cfg)
autoAnswerService = AutoAnswerService(cfg) 
autoAnswerDAO = AutoAnswerDAO()
bot = Bot(token=cfg.getAttribute(SECURE_TOKEN))

remoteService = RemoteService(cfg, userDAO, RouterService())

connection = sqlite3.connect("auto_answers.db")
qu = """CREATE TABLE IF NOT EXISTS auto_answers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT,
	dates TEXT,
	content TEXT,
	active INTEGER,
	updated_at TEXT);"""
connection.cursor().execute(qu)

@dp.message(F.text == "Главная")
@dp.message(Command("start"))
async def cmd_start(message: types.Message, username: str):
	
	if username == "":
		await message.answer(NOT_FOUND_USERNAME)
		return

	actions = [
		[
			types.KeyboardButton(text = "Автоответ"),
			types.KeyboardButton(text = "Удаленный рабочий стол")
		]
	]

	keyboard = types.ReplyKeyboardMarkup(
			keyboard = actions,
			resize_keyboard = True,
			input_field_placeholder = HINT
		)

	await message.answer(HELLO_MESSAGE, reply_markup = keyboard)


@dp.message(F.text == "Удаленный рабочий стол")
async def getVPNFile(message: types.Message, state: FSMContext, username: str):
	await message.answer("Подождите, идет генерация файла для удаленного подключения")
	file = remoteService.getVPNFile(username)
	await message.answer_document(FSInputFile(file))

# @dp.message(Manual.question)
# async def manual(message: types.Message, state: FSMContext):
# 	await message.answer(message.text.split("\n"))

@dp.message(F.text == "Автоответ")
async def getDataAutoAnswer(message: types.Message, state: FSMContext, username: str):
	data = autoAnswerService.getData(username)
	if data == "":
		await message.answer(NOT_FOUND_USERNAME)
		return

	state = data["AutoReplyState"]

	if state == "":
		await message.answer(AUTOANSWER_FAILED)
		return

	await message.answer("Ваш автоответ " + AUTOANSWER_MODE[state])

	actions = [
		[
			types.KeyboardButton(text = "Включить автоответ"),
			types.KeyboardButton(text = "Выключить автоответ"),
		],
		[
			types.KeyboardButton(text = "Главная"),
		]
	]

	keyboard = types.ReplyKeyboardMarkup(
			keyboard = actions,
			resize_keyboard = True,
			input_field_placeholder = AUTOANSWER_HINT
		)

	await message.answer(AUTOANSWER_DO, reply_markup = keyboard)


@dp.message(F.text == "Включить автоответ")
async def autoanswer(message: types.Message, state: FSMContext, username: str):
	global temp
	temp = AutoAnswer()
	
	if username == "":
		await message.answer(NOT_FOUND_USERNAME)
		return

	temp.setUsername(username)

	await message.answer(DATE_MESSAGE)
	await state.set_state(AutoAnswerState.chooseDate)	

@dp.message(F.text == "Выключить автоответ")
async def offAutoAnswer(message: types.Message, state: FSMContext, username: str):
	#reg off auto answer

	if username == "":
		await message.answer(NOT_FOUND_USERNAME)
		return

	err = autoAnswerService.offAutoAnswer(username)
	if err:
		await message.answer(AUTOANSWER_FAILED)
		return

	#async/await need (mutex)
	autoAnswer = autoAnswerDAO.getByUsername(username)
	if not (autoAnswer is None) or autoAnswer != "":
		autoAnswer.setActive(True)
		autoAnswerDAO.insert(autoAnswer)

	await message.answer(AUTOANSWER_OFF_SUCCESS)

@dp.message(AutoAnswerState.chooseDate)
async def setDateForAutoAnswer(message: types.Message, state: FSMContext):
	# PARSE DATES IN ANOTHER METHOD
	try:
		dateRange = DateRange(DateParser(), message.text)
		temp.setDateRange(dateRange)
	except Exception as e:
		print(e)
		await message.reply(NOT_VALID_DATES_ERROR)
		return

	await message.answer(REPLACE_MESSAGE) 
	await state.set_state(AutoAnswerState.chooseReplaceContent)

@dp.message(AutoAnswerState.chooseReplaceContent)
async def setMessageForAutoAnswer(message: types.Message, state: FSMContext):
	htmlParser = HTMLParser(temp)
	temp.setReplaceContent(message.text)
	temp.setFullMessage(htmlParser.getContent())

	err = autoAnswerService.setAutoAnswer(temp, DateParser())
	if err:
		await message.answer(AUTOANSWER_FAILED)
		return

	#async/await need (mutex)
	temp.setActive(True)
	autoAnswerDAO.insert(temp)
	await message.answer(AUTOANSWER_ON_SUCCESS)

async def main():
	logging.basicConfig(level=logging.INFO)
	dp.message.middleware(AuthMiddleware(userDAO))

	await dp.start_polling(bot)

if __name__ == "__main__":
	asyncio.run(main())
