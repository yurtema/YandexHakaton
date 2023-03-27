from src import yandex, phrases, image
from random import choice, randint
from os import listdir, remove
import threading


def start_generating_random():
    rgb_base = (randint(0, 255), randint(0, 255), randint(0, 255))
    rgb_dec = (randint(0, 255), randint(0, 255), randint(0, 255))

    dirs = listdir('media')
    dirs.remove('temp')
    dirs.remove('разное')
    direct = choice(dirs)
    sample = f'{direct}/{str(randint(1, len(listdir(f"media/{direct}")) // 3))}'

    thread = threading.Thread(target=image.recolor_hand, args=(sample, rgb_base, rgb_dec))
    thread.start()

    if len(listdir('media/temp')) >= 100:
        for i in range(70):
            remove('media/temp/' + choice(listdir('media/temp')))

    return f'{sample[-1]}_{rgb_base}_{rgb_dec}.png'


def overlaps(user, target):
    return [1 for i in user.replace(',', ' ').replace('.', ' ').split() if i in target] != []


def handler(event):
    # Начало
    if event['state']['session'] == {}:
        return yandex.send_text(event, choice(phrases.greeting), {'state': 'начнем?'})

    user_text = event['request']['original_utterance'].lower()
    state = event['state']['session']['state']
    start_generating_random()

    # Начинать или нет?
    # да - запустить генерацию изображения со случайными параметрами
    # нет - закончить навык
    if state == 'начнем?':
        if overlaps(user_text, phrases.yes):
            return yandex.send_text(event, choice(phrases.start_skill),
                                    {'state': 'случайный?'})

        if overlaps(user_text, phrases.no):
            return yandex.end_session(event, choice(phrases.end_session))

        return yandex.send_text(event, choice(phrases.what))

    # Случайный или нет?
    # рандом - прислать случайное изображение из папки temp
    # конкретный - спросить про цвет
    if state == 'случайный?':
        if overlaps(user_text, phrases.user_random):
            return yandex.send_image(event, choice(phrases.random), [choice(listdir('media/temp')), ],
                                     {'state': 'еще случайный?'})

        if overlaps(user_text, phrases.specific_choise):
            return yandex.send_text(event, choice(phrases.what_color) + '\nВарианты:\n' + 'случайный\n' + '\n'.join(
                phrases.colors.keys()), {'state': 'цвет?'})

        return yandex.send_text(event, choice(phrases.what))

    # Отправлять ли еще одно случайное изображение или закончить?
    # случайное - отправить случайное изображение из папки temp и спросить снова
    # нет - закончить навык
    if state == 'еще случайный?':
        if overlaps(user_text, phrases.user_random):
            return yandex.send_image(event, choice(phrases.random), [choice(listdir('media/temp'))],
                                     {'state': 'еще случайный?'})

        if overlaps(user_text, phrases.no):
            return yandex.end_session(event, choice(phrases.end_session))

        return yandex.send_text(event, choice(phrases.what))

    # Какой цвет?
    # рандом - выбрать случайный цвет
    # цвет - записать выбранный
    if state == 'цвет?':
        if overlaps(user_text, phrases.user_random):
            rgb_base = (randint(0, 255), randint(0, 255), randint(0, 255))
            return yandex.send_text(event, choice(phrases.what_theme), {'state': 'тема дек?', 'base_color': rgb_base})

        if overlaps(user_text, phrases.colors):
            dirs = listdir('media')
            dirs.remove('temp')
            return yandex.send_text(event,
                                    choice(phrases.what_theme) + '\nВарианты:\n' + 'случайный\n' + '\n'.join(dirs),
                                    {'state': 'тема дек?', 'base_color': phrases.colors[user_text]})

        return yandex.send_text(event, choice(phrases.error_color) + '\nВарианты:\n' + 'случайный\n' + '\n'.join(
            phrases.colors.keys()))

    # Из какой папки брать декор?
    # рандом - выбрать случайную тему
    # тема - записать выбранную
    if state == 'тема дек?':

        dirs = listdir('media')
        dirs.remove('temp')
        random_theme = choice(dirs)

        if overlaps(user_text, phrases.user_random):
            return yandex.send_text(event, choice(phrases.what_theme), {'state': 'тема дек?',
                                                                        'dec_theme': random_theme})

        if overlaps(user_text, dirs):
            return yandex.send_text(event, choice(phrases.what_theme), {'state': 'тема дек?',
                                                                        'dec_theme': user_text})

        return yandex.send_text(event, choice(phrases.error_theme) + '\nВарианты:\n' + 'случайный\n' + '\n'.join(dirs))

    else:
        return 'Ничерта не сработало, пишите админу. Для админа: \n' + str(event)
