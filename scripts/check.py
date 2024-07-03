# '''импортируем модули'''
import requests
from fake_user_agent import user_agent
from colorama import Fore, Style

# '''объявляем переменную для хранения рандомного юзерагента'''
ua = {"user-agent": user_agent("Chrome")}


def check(url):
    '''создаем функцию-чекер соединения, который проверяет
    интернет соединение и доступность сайта'''
    url = f"https://{url}"
    try:
        internet_check = requests.get("https://google.com", headers=ua)
    except Exception:
        print("Check your internet connection!")
        exit(0)
    try:
        site_check = requests.get(url, headers=ua)
    except Exception:
        print("Site is not available!")
        exit(0)
    print("\nSite available!", Fore.RED + "Starting stalking!" + Style.RESET_ALL + '\n')
