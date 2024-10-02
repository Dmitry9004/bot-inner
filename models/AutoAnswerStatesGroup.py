from aiogram.fsm.state import State, StatesGroup

class AutoAnswerStatesGroup(StatesGroup):
	chooseDate = State()
	chooseReplaceContent = State()
	chooseUser = State()