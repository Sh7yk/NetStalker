# '''импортируем модули'''
from threading import Thread
import os
import requests
from fake_user_agent import user_agent
from queue import Queue
from . import uri_generator
from colorama import Fore, Style

# '''объявляем переменую для хранения рандомного юзерагента'''
ua = {'user-agent': user_agent("Chrome")}
# '''объявляем переменную для хранения очереди'''
q = Queue()


def requester(queue, need_size):
    '''создаем функию для отправки запросов'''
    # '''объявляем переменную для хранения начального размера папки'''
    size = 0
    # '''циклом выполняем запросы'''
    while not queue.empty():
        # '''объявляем переменную для хранения элемента очереди'''
        uri = queue.get()
        # '''объявляем переменную для хранения ссылки на файл'''
        url = f'https://i.imgur.com/{uri}'
        # '''объявляем переменную для хранения списка расширений'''
        ext_list = ['.mp4', '.jpg']
        # '''циклом проходимся по каждому элементу списка'''
        for i in ext_list:
            # '''создаем условие проверки размера'''
            if size_check(size) <= need_size:
                # '''объявляем переменную для хранения результата запроса'''
                response = requests.get(url + i, headers=ua, allow_redirects=False)
                # '''создаем условие проверяющее статус ответа'''
                if response.status_code == 200:
                    print(f'{url}{Fore.GREEN} ==> Good!{Style.RESET_ALL}')
                    # '''вызывем функцию сохранения файла'''
                    save_file(response, uri + i)
                else:
                    print(url)
            else:
                # '''прерываем цикл после достижения необходимого размера папки'''
                break
        # '''завершаем задачу'''
        queue.task_done()


def save_file(resp, name):
    '''создаем функцию сохранения файла'''
    with open(f'content/{name}', 'wb') as file:
        file.write(resp.content)


def thread_func(threads, need_size):
    '''создаем функцию для запуска нескольких потоков'''
    # '''циклом помещаем все элементы списка в очередь'''
    for uri in uri_generator.generator():
        q.put(uri)
    # '''объявляем переменную для хранения списка потоков'''
    thread_list = []
    # '''циклом запускаем количество потоков, которое было передано пользователем'''
    for thread in range(threads):
        # '''объявляем переменную для хранения потока'''
        t = Thread(target=requester, args=(q, need_size))
        # '''старутем поток'''
        t.start()
        # '''помещаем поток в список'''
        thread_list.append(t)
    # '''дожидаемся обработки элементов очереди потоком'''
    q.join()
    # '''циклом дожидаемся завершения всех потоков'''
    for t in thread_list:
        t.join()


def size_check(size):
    '''создаем функцию проверки размера папки'''
    for path, dirs, files in os.walk('../content'):
        for file in files:
            file_path = os.path.join(path, file)
            size += os.path.getsize(file_path)
    result = round(size / (1024 * 1024), 2)
    return result
