from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dao.UserDAO import UserDAO
from typing import Any, Callable, Awaitable, Dict

class AuthMiddleware(BaseMiddleware):

	def __init__(self, userDAO: UserDAO):
		self.__userDAO = userDAO

	async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: Dict[str, Any]):
		print(data["event_from_user"])
		username = self.__userDAO.getUsername(data["event_from_user"].username)
		if username == "":
			data["username"] = ""
		else:
			data["username"] = username
		
		print(username)
		return await handler(event, data)