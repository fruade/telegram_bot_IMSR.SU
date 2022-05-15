from aiogram.dispatcher.filters.state import StatesGroup, State

class Request_imsr(StatesGroup):
    New_task_info = State()
    Send_answer1 = State()
    Send_answer2 = State()
    Send_answer3 = State()
    Request_task1 = State()
    Request_task2 = State()
    Request_task3 = State()
    Request_task4 = State()