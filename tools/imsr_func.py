import aiohttp
import requests


def get_data_task_imsr():
    responce_main = requests.get('https://api.imsr.su/main/get_tasks').json().get('data')
    responce_archive = requests.get('https://api.imsr.su/archive/get_tasks').json().get('data')
    responce = responce_archive + responce_main
    return responce


def check_new_task():
    with open('tools/len_task.txt', 'r', encoding='utf-8') as file:
        len_now = file.read()
    len_task = len(get_data_task_imsr())
    if int(len_now) == len_task:
        return True
    with open('tools/len_task.txt', 'w', encoding='utf-8') as file:
        file.write(str(len_task))
    return False


def add_answer(full_name: str, task_id, answer):
    f_name, l_name = full_name.split()[0], full_name.split()[1]
    data = {
        'first_name': f_name,
        'last_name': l_name,
        'answer': answer,
        'task_id': task_id
    }

    send = requests.post('https://api.imsr.su/add_answer', data=data).json()
    print(send)
    print(send['status'])
    return send['status']


def get_task(task_id):
    responce = get_data_task_imsr()
    return responce[task_id - 1]['description']


def check_task_id(check: str):
    if check.isdigit():
        return 0 < int(check) <= len(get_data_task_imsr())
    return False


def request_task(title, description, start_code, comment):
    data = {
        'title': title,
        'description': description,
        'start_code': start_code,
        'comment': comment
    }

    send = requests.post('https://api.imsr.su/add_request', data=data).json()
    return send['status']


