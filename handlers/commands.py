from main import dp, bot
from aiogram.types import Message
from keyboards.keyboard import keyboard_menu


@dp.message_handler(commands=['start', 'help'])
async def start_command(message: Message):
    text = "Этот бот поможет тебе взаимодействовать с сайтом imsr.ru\n/menu - основное меню"
    await message.delete()
    await bot.send_message(message.from_user.id, text)


@dp.message_handler(commands=['menu'])
async def menu(message: Message):
    text = 'Выбери операцию'
    await bot.send_message(message.from_user.id, text, reply_markup=keyboard_menu)












