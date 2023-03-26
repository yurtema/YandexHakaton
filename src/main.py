from src import yandex, phrases, image
from random import choice, randint
import os
import threading


def start_generating_random():
    rgb_base = (randint(0, 255), randint(0, 255), randint(0, 255))
    rgb_dec = (randint(0, 255), randint(0, 255), randint(0, 255))

    dirs = os.listdir('media')
    dirs.remove('temp')
    dirs.remove('misc')
    direct = choice(dirs)
    sample = f'{direct}/{str(randint(1, len(os.listdir(f"media/{direct}")) // 3))}'

    thread = threading.Thread(target=image.recolor_hand, args=(sample, rgb_base, rgb_dec))
    thread.start()

    return f'{sample[-1]}_{rgb_base}_{rgb_dec}.png'


def overlaps(user, target):
    return [1 for i in user.lower().replace(',', ' ').replace('.', ' ').split() if
            i in target] is not {}


def handler(event):
    # Начало
    if event['state']['session'] == {}:
        return yandex.send_text(event, choice(phrases.greeting), {'state': 'начнем?'})

    user_text = event['request']['original_utterance']
    state = event['state']['session']['state']

    # Начинать или нет?
    # да - запустить генерацию изображения со случайными параметрами
    # нет - закончить навык
    if state == 'начнем?':
        if overlaps(user_text, phrases.yes):
            return yandex.send_text(event, choice(phrases.start_skill),
                                    {'state': 'случайный?', 'hand': start_generating_random()})

        elif overlaps(user_text, phrases.no):
            return yandex.end_session(event, choice(phrases.end_session))

        return yandex.send_text(event, choice(phrases.what))

    # Случайный или нет?
    # рандом - прислать сгенерированное изображение если уже есть такое, если нет - вернуть с кодом ожидания
    # конкретный - спросить про цвет
    if state == 'случайный?':
        if overlaps(user_text, phrases.user_random):
            # извлечь из запроса название файла с рукой
            hand = event['state']['session']['hand']
            # если оно еще не было сгенерировано, вернуть код ожидания
            if hand not in os.listdir('media/temp'):
                return yandex.send_text(event, choice(phrases.wait),
                                        {'state': 'ждите генерации случайного изображения'})
            # если было, отправить его
            return yandex.send_image(event, choice(phrases.random), [hand, ])

        if overlaps(user_text, phrases.specific_choise):
            return yandex.send_text(event, choice(phrases.random), {'state': 'цвет?'})

        return yandex.send_text(event, choice(phrases.what))

    # подождать пока пользователь отправит чето, как отправит - чекнуть, сгенерировалось оно или еще нет.
    # если сгенерировалось - отправить, если нет - вернуть сюда
    if state == 'ждите генерации случайного изображения':
        # извлечь из запроса название файла с рукой
        hand = event['state']['session']['hand']
        # если оно еще не было сгенерировано, вернуть код ожидания
        if hand not in os.listdir('media/temp'):
            return yandex.send_text(event, choice(phrases.wait),
                                    {'state': 'ждите генерации случайного изображения'})
        # если было, отправить его
        return yandex.send_image(event, choice(phrases.random), [hand, ],
                                 {'state': 'еще случайный?', 'hand': start_generating_random()})

    # спросить, отправлять ли еще одно случайное изображение
    # да - начать генерировать и вернуть код ожидания
    # нет - закончить навык
    if state == 'еще случайный?':
        if overlaps(user_text, phrases.yes):
            return yandex.send_text(event, choice(phrases.start_skill),
                                    {'state': 'ждите генерации случайного изображения',
                                     'hand': start_generating_random()})

        elif overlaps(user_text, phrases.no):
            return yandex.end_session(event, choice(phrases.end_session))

        return yandex.send_text(event, choice(phrases.what))

    else:
        return 'Ничерта не сработало, пишите админу. Для админа: \n' + str(event)
