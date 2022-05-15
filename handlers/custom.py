from main import dp, bot, anti_flood
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from tools.imsr_func import *
from keyboards.keyboard import keyboard_return
from states.state import Request_imsr
from .commands import menu


@dp.message_handler(text='Новое задание?')
@dp.throttled(anti_flood, rate=2)
async def new_task_info(message: Message):
    if check_new_task():
        return await message.answer(text='Новых заданий нет')
    num_task = int(len(get_data_task_imsr()))
    await message.answer(text=f'Внимание, появилось новое задание! №{num_task}')
    return await message.answer(text=get_task(num_task))


@dp.message_handler(text='Получить задание', state=None)
@dp.throttled(anti_flood, rate=2)
async def get_task1(message: Message):
    await message.answer(text='Чтобы получить описание задания, введите его номер (task_id)', reply_markup=keyboard_return)
    await Request_imsr.New_task_info.set()


@dp.message_handler(state=Request_imsr.New_task_info)
async def get_task_show(message: Message, state: FSMContext):
    answer = message.text
    if answer == 'Назад':
        await state.finish()
        return await menu(message)
    elif len(answer.split()) == 1 and check_task_id(answer):
        await message.answer(text=get_task(int(answer)))
    else:
        await message.answer(text='Такого задания не существует')


@dp.message_handler(text='Ответить на задание', state=None)
@dp.throttled(anti_flood, rate=2)
async def send_answer1(message: Message):
    await message.answer(text='Введите имя и фамилию через пробел', reply_markup=keyboard_return)
    await Request_imsr.Send_answer1.set()


@dp.message_handler(state=Request_imsr.Send_answer1)
async def send_answer2(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    if answer == 'Назад':
        await state.finish()
        return await menu(message)
    await message.answer(text='Введите номер задания', reply_markup=keyboard_return)
    await Request_imsr.next()


@dp.message_handler(state=Request_imsr.Send_answer2)
async def send_answer2(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    if answer == 'Назад':
        await state.finish()
        return await menu(message)
    await message.answer('Введите ответ на задание')
    await Request_imsr.next()


@dp.message_handler(state=Request_imsr.Send_answer3)
async def send_answer_show(message: Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    if answer == 'Назад':
        await state.finish()
        return await menu(message)
    print(data)
    if add_answer(data.get('answer1'), data.get('answer2'), answer):
        await message.answer('Ответ успешно отправлен')
    else:
        await message.answer('Что-то пошло не так, попробуйте снова')

    await state.finish()
    return await menu(message)


@dp.message_handler(text='Предложить задание', state=None)
@dp.throttled(anti_flood, rate=2)
async def give_task1(message: Message):
    await message.answer(text='Введите заголовок задания', reply_markup=keyboard_return)
    await Request_imsr.Request_task1.set()


@dp.message_handler(state=Request_imsr.Request_task1)
async def give_task2(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    if answer == 'Назад':
        await state.finish()
        return await menu(message)
    await message.answer('Введите задание')
    await Request_imsr.next()


@dp.message_handler(state=Request_imsr.Request_task2)
async def give_task3(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    if answer == 'Назад':
        await state.finish()
        return await menu(message)

    await message.answer('Введите начальный код')
    await Request_imsr.next()


@dp.message_handler(state=Request_imsr.Request_task3)
async def give_task4(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer3=answer)
    if answer == 'Назад':
        await state.finish()
        return await menu(message)

    await message.answer('Введите комментарий')
    await Request_imsr.next()


@dp.message_handler(state=Request_imsr.Request_task4)
async def give_task_show(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer4=answer)
    data = await state.get_data()
    if answer == 'Назад':
        await state.finish()
        return await menu(message)
    elif request_task(data['answer1'], data['answer2'], data['answer3'], data['answer4']):
        await message.answer(text='Задание успешно отправлено модератору')
    else:
        await message.answer(text='Что-то пошло не так, попробуйте снова')
    await state.finish()
    return await menu(message)


@dp.message_handler(text='Назад')
async def return_menu(message: Message):
    return await menu(message)