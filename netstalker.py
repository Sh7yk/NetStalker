'''ипортируем модули'''
import platform
import os
import time
import scripts.check as check
import scripts.time_method as time_method
from colorama import Fore, Style
import scripts.counter_method as counter
import scripts.size_method as size

'''объявляем переменную для хранения логотипа'''
logo = r"""___  ___        _   _      _   _____ _        _ _             
|  \/  |       | \ | |    | | /  ___| |      | | |            
| .  . |_   _  |  \| | ___| |_\ `--.| |_ __ _| | | _____ _ __ 
| |\/| | | | | | . ` |/ _ \ __|`--. \ __/ _` | | |/ / _ \ '__|
| |  | | |_| | | |\  |  __/ |_/\__/ / || (_| | |   <  __/ |   
\_|  |_/\__, | \_| \_/\___|\__\____/ \__\__,_|_|_|\_\___|_|   
         __/ |                                                
        |___/ 
by Sh7yk"""
# '''объявлявем переменную для хранения словаря с целевыми сайтами'''
targets = {1: "imgur.com"}
# '''объявляем переменную для хранения словаря с функциями их параметрами'''
methods = {1: ["time", time_method.thread_func,
               Fore.GREEN + 'Set the time to work: ' + Style.RESET_ALL, 'second'],
           2: ["links count", counter.thread_func,
               Fore.GREEN + 'Select links qnt: ' + Style.RESET_ALL, 'links'],
           3: ["target size", size.thread_func,
               Fore.GREEN + 'Select max size: ' + Style.RESET_ALL, 'Mb']}
print(logo)


def make_dir():
    '''создаем функцию для проверки/создания папки'''
    if not os.path.exists('content'):
        os.mkdir('content')


def check_user_input(prompt, check_value, func_id):
    '''создаем функцию проверки корректности ввода пользователя'''
    while True:
        try:
            users_input = int(input(prompt))
            if func_id == 1:
                if users_input in check_value:
                    return users_input
                print("Invalid input. Please try again.")
            elif func_id == 2:
                if users_input > check_value:
                    return users_input
                print("Invalid input. Please try again.")
        except ValueError:
            print("Value must be an integer!")


def user_input():
    '''создаем функцию для приема пользовательского ввода'''
    print(Fore.GREEN + "\nAvailable targets: " + Style.RESET_ALL)
    for key, val in targets.items():
        print(f"{key}) {val}")

    target_choose = check_user_input("Your choice: ", targets.keys(), 1)
    print(f"Using {targets.get(target_choose)}", end="\n")

    threads = check_user_input(Fore.GREEN + "\nSelect threads: " + Style.RESET_ALL, 0, 2)
    print(f"Using {threads} threads", end="\n")

    print(Fore.GREEN + "\nChoose method: " + Style.RESET_ALL)
    for key, val in methods.items():
        print(f"{key}) {val[0]}")

    method_choose = check_user_input("Your choice: ", methods.keys(), 1)
    print(f"Using {methods.get(method_choose)[0]} method", end="\n")

    method_value = check_user_input(methods.get(method_choose)[2], 0, 2)
    print(f"Using {method_value} as method value", end="\n")
    base(target_choose, threads, method_value, method_choose)


def task_info(target_choose, threads, method_value, method_choose):
    '''создаем функцию для вывода информации о задаче'''
    # '''вывдим в консоль итоговые характеристики задачи'''
    print(
        f'Target: {Fore.BLUE + targets.get(target_choose) + Style.RESET_ALL} '
        f'with {Fore.BLUE}{threads} '
        f'threads{Style.RESET_ALL} for {Fore.BLUE}{method_value} '
        f'{methods.get(method_choose)[3] + Style.RESET_ALL}')


def base(target_choose, threads, method_value, method_choose):
    '''создаем функцию для вызова нужного метода и передачи в него параметров'''
    task_info(target_choose, threads, method_value, method_choose)
    # '''объявляем переменную для хранения стартового времени'''
    start_time = time.time()
    # '''вызываем функцию проверки соединения'''
    check.check(targets.get(target_choose))
    # '''вызываем функцию проверки/создания папки'''
    make_dir()
    # '''вызываем указанный метод и передаем в него параметры'''
    methods.get(method_choose)[1](threads, method_value)
    final_message(start_time)


def final_message(start_time):
    '''создаем функцию для вывода результатов выполнения'''
    print("=" * 45)
    print("Done!", '\n' * 2)
    # '''выводим в консоль результат выполненой задачи и характеристики'''
    print(Fore.MAGENTA +
          f"Ready for: {round((time.time() - start_time) / 3600, 0)} "
          f"hours {round((time.time() - start_time) / 60, 0)} "
          f"minutes {round(time.time() - start_time, 0)} seconds")
    print(f"Found links: {len(os.listdir('content'))}")
    total_size = 0
    for path, dirs, files in os.walk('content'):
        for file in files:
            file_path = os.path.join(path, file)
            total_size += os.path.getsize(file_path)
    print(f"Folder size: {total_size / (1024 * 1024):.2f}  Mb" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "\nResult saved in 'content' folder" + Style.RESET_ALL)


# '''создаем точку входа'''
if __name__ == "__main__":
    try:
        user_input()
    except KeyboardInterrupt:
        print("\nProgram has been manually interrupt")
        exit(0)
    # '''проверяем систему пользователя перед открытием папки'''
    if platform.system() == 'Windows':
        os.system(f'explorer content')
    os.system(f'xdg-open content')
