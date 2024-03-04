from aiogram.dispatcher.filters.state import StatesGroup, State


class FSM(StatesGroup):
    all_default_state = State()

    add_bot_state = State()
