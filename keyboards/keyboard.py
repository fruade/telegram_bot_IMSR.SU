from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

imsr_data_button = ['Новое задание?', 'Получить задание', 'Ответить на задание', 'Предложить задание']

keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard_menu.add(*imsr_data_button)

keyboard_return = ReplyKeyboardMarkup(resize_keyboard=True).add('Назад')
