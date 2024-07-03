# '''импортируем модули'''
from threading import Thread
import requests
from fake_user_agent import user_agent
from queue import Queue
from . import uri_generator
from colorama import Fore, Style

# '''объявляем переменую для хранения рандомного юзерагента'''
ua = {'user-agent': user_agent("Chrome")}
# '''объявляем переменную для хранения функции очередей'''
q = Queue()

link_count = 0


def requester(queue, qnt):
    '''создаем функию для отправки запросов'''
    # '''объявляем глобальную переменную счетчика'''
    global link_count
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
            # '''работаем через замок, чтобы многопоточность не вызывала "переработок" по задаче'''
            # '''условием проверяем количество обработанных ссылок'''
            if link_count < qnt:
                # '''объявляем переменную для хранения ответа'''
                response = requests.get(url + i, headers=ua, allow_redirects=False)
                # '''проверяем статус код ответа'''
                if response.status_code == 200:
                    print(f'{url}{Fore.GREEN} ==> Good!{Style.RESET_ALL}')
                    # '''вызываем функцию сохранения файла'''
                    save_file(response, uri + i)
                    # '''прибавляем к счетчику единицу после завершения каждого цикла'''
                    link_count += 1
                else:
                    continue
            else:
                # '''прерываем выполнение после достижения необходимого количества запросов'''
                break
        # '''завершаем задачу'''
        queue.task_done()


def save_file(resp, name):
    '''создаем функцию сохранения файла'''
    with open(f'content/{name}', 'wb') as file:
        file.write(resp.content)


def thread_func(threads, qnt):
    '''создаем функцию для запуска нескольких потоков'''
    # '''условием проверяем количкство потоков и количество ссылок,
    # если потоков больше чем ссылок, уравниваем'''
    if qnt < threads:
        threads = qnt
    # '''циклом помещаем все элементы списка в очередь'''
    for uri in uri_generator.generator():
        q.put(uri)
    # '''объявляем переменную для хранения списка потоков'''
    thread_list = []
    # '''циклом запускаем количество потоков, которое было передано пользователем'''
    for _ in range(threads):
        # '''объявляем переменную для хранения потока'''
        t = Thread(target=requester, args=(q, qnt))
        # '''старутем поток'''
        t.start()
        # '''помещаем поток в список'''
        thread_list.append(t)
    # '''дожидаемся завершения потоков'''
    q.join()
    # '''циклом дожидаемся завершения всех потоков'''
    for t in thread_list:
        t.join()
