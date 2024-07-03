# '''импортируем модули'''
import string
import random

# '''объявляем переменную для хранения списка символов'''
char_list = string.ascii_letters + string.digits


def generator():
    '''создаем функцию генератора комбинаций'''
    # '''объявляем переменную для хранения списка комбинаций'''
    random_permutations = ['q0M9WT4']
    for _ in range(100000):
        random_perm = ''.join(random.sample(char_list, 7))
        random_permutations.append(random_perm)
    return random_permutations
