# '''импортируем модули'''
import time
import requests
from threading import Thread, Event
from fake_user_agent import user_agent
from queue import Queue
from . import uri_generator
from colorama import Fore, Style

# '''объявляем переменную для хранения заголовка юзерагента'''
ua = {'user-agent': user_agent('Chrome')}
# '''объявляевм переменную для хранения очереди'''
q = Queue()
# '''объявляем переменную для хранения события остановки'''
stop_event = Event()


def requester(queue, sec):
    '''создаем функцию для отправки запросов'''
    # '''объявляем переменную для хранения стартового значения времени'''
    start_time = time.time()
    # '''объявляем переменную для хранения конечного значения времени'''
    end_time = start_time + sec
    # '''циклом выполняем запросы'''
    while not queue.empty():
        # '''объявляем переменную для хранения элемента очереди'''
        uri = queue.get()
        # '''объявляем переменную для хранения ссылки на файл'''
        url = f'https://i.imgur.com/{uri}'
        # '''объявляем переменную для хранения списка расширений'''
        ext_list = ['.mp4', '.jpg']
        # '''циклом проходимся по каждому элементу списка'''
        for ext in ext_list:
            # '''создаем условие проверки времени'''
            if end_time > time.time():
                # '''бъявляем переменную для хранения результата запроса'''
                response = requests.get(url + ext, headers=ua, allow_redirects=False)
                # '''создаем условие проверяющее статус ответа'''
                if response.status_code == 200:
                    print(f'{url}{Fore.GREEN} ==> Good!{Style.RESET_ALL}')
                    # '''вызывем функцию сохранения файла'''
                    save_file(response, uri + ext)
                else:
                    print(url)
            else:
                # '''прерываем цикл после истечения времени'''
                stop_event.set()
                break
        # '''завершаем задачу'''
        queue.task_done()


def save_file(resp, name):
    '''создаем функцию сохранения файла'''
    with open(f'content/{name}', 'wb') as file:
        file.write(resp.content)


def thread_func(threads, sec):
    '''создаем функцию для запуска нескольких потоков'''
    # '''циклом помещаем все элементы списка в очередь'''
    for uri in uri_generator.generator():
        q.put(uri)
    # '''объявляем переменную для хранения списка потоков'''
    thread_list = []
    # '''циклом запускаем количество потоков, которое было передано пользователем'''
    for thread in range(threads):
        # '''объявляем переменную для хранения потока'''
        t = Thread(target=requester, args=(q, sec))
        # '''старутем поток'''
        t.start()
        # '''помещаем поток в список'''
        thread_list.append(t)
    # '''дожидаемся завершения потоков'''
    q.join()
    # '''прерываем цикл'''
    stop_event.set()
    # '''циклом дожидаемся завершения всех потоков'''
    for t in thread_list:
        t.join()
