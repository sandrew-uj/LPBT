from aiogram.dispatcher.filters.state import StatesGroup, State


class FSM(StatesGroup):
    all_default_state = State()

    add_bot_state = State()

    type_answer = State()
    type_comment = State()

    type_content = State()
    type_name = State()

    get_phone_state = State()
    get_group_state = State()
