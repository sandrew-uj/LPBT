import requests
from aiogram import types, Bot

import config
from exceptions.backend_exceptions import BackendDead
from utils.dbs.tokens import TokensDB


# async def get_modules_kb(bot: Bot, start: int = 0):
#     res = TokensDB.get_modules(bot).json()
#     keyboard = types.InlineKeyboardMarkup()
#
#     bottom_buttons=[]
#
#     categories = res.json()
#
#     if start > 0:
#         button_back = types.InlineKeyboardButton(text="<",
#                                                  callback_data=subcategory_keyboard_cb.new(
#                                                      category_id=start - 5,
#                                                      subcategory_id=int(data['subcategory_id']),
#                                                      type="arrow_dish",
#                                                      name=""
#                                                  ))
#         bottom_buttons.append(button_back)
#
#     for idx in range(start, min(start + 5, len(categories))):
#         dish = categories[idx]
#         button = types.InlineKeyboardButton(text=dish["name"],
#                                             callback_data=dish_cb.new(dish_id=dish["id"],
#                                                                       type="dish"))
#         keyboard.add(button)
#
#     back_button = types.InlineKeyboardButton(text="Назад", callback_data=dish_cb.new(dish_id=data["category_id"],
#                                                                                      type="back"))
#     bottom_buttons.append(back_button)
#
#     if start + 9 < len(categories):
#         button_forward = types.InlineKeyboardButton(text=">",
#                                                     callback_data=subcategory_keyboard_cb.new(
#                                                         category_id=start + 5,
#                                                         subcategory_id=int(data['subcategory_id']),
#                                                         type="arrow_dish",
#                                                         name=""
#                                                     ))
#         bottom_buttons.append(button_forward)
#
#     keyboard.add(*bottom_buttons)
#     return keyboard