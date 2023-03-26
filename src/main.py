from src import yandex, phrases, image
from random import choice, randint
import os


def handler(event):
    # Начало
    if event['state']['session'] == {}:
        return yandex.send_text(event, choice(phrases.greeting), {'state': 'начнем?'})

    # Начинать или нет? да/нет
    if event['state']['session']['state'] == 'начнем?':
        if event['request']['original_utterance'].lower() in phrases.yes:
            rgb_base = (randint(0, 255), randint(0, 255), randint(0, 255))
            rgb_dec = (randint(0, 255), randint(0, 255), randint(0, 255))

            dirs = os.listdir('media')
            dirs.remove('temp')
            dirs.remove('misc')
            direct = choice(dirs)
            sample = f'{direct}/{str(randint(1, len(os.listdir(f"media/{direct}")) // 3))}'

            hand = image.recolor_hand(sample, rgb_base, rgb_dec)
            return yandex.send_text(event, choice(phrases.start_skill), {'state': 'случайный?', 'random_hand': hand})
        elif event['request']['original_utterance'].lower() in phrases.no:
            return yandex.end_session(event, choice(phrases.end_session))

        return yandex.send_text(event, choice(phrases.what))

    # Случайный или нет? да/нет
    if event['state']['session']['state'] == 'случайный?':
        if event['request']['original_utterance'].lower() in phrases.yes:
            return yandex.send_image(event, choice(phrases.random), [event['state']['session']['random_hand'], ],
                                     {'state': 'еще раз?'})

        elif event['request']['original_utterance'].lower() in phrases.no:
            return yandex.send_text(event, choice(phrases.random), {'state': 'цвет?'})

        return yandex.send_text(event, choice(phrases.what))


    else:
        return 'Ничерта не сработало, пишите админу. Для админа: \n' + str(event)
