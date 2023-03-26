from src import yandex, phrases, image
from random import choice, randint
import os
import threading


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

            thread = threading.Thread(target=image.recolor_hand, args=(sample, rgb_base, rgb_dec))
            thread.start()

            filename = f'{sample[-1]}_{rgb_base}_{rgb_dec}.png'

            return yandex.send_text(event, choice(phrases.start_skill), {'state': 'случайный?', 'hand': filename})

        elif event['request']['original_utterance'].lower() in phrases.no:
            return yandex.end_session(event, choice(phrases.end_session))

        return yandex.send_text(event, choice(phrases.what))

    # Случайный или нет? да/нет
    if event['state']['session']['state'] == 'случайный?':
        if event['request']['original_utterance'].lower() in phrases.yes:
            hand = event['state']['session']['hand']
            if hand not in os.listdir('media/temp'):
                return yandex.send_text(event, choice(phrases.wait),
                                        {'state': 'ждите генерации случайного изображения'})
            return yandex.send_image(event, choice(phrases.random), [hand, ],
                                     {'state': 'еще случайный?'})

        elif event['request']['original_utterance'].lower() in phrases.no:
            return yandex.send_text(event, choice(phrases.random), {'state': 'цвет?'})

        return yandex.send_text(event, choice(phrases.what))

    if event['state']['session']['state'] == 'ждите генерации случайного изображения':
        hand = event['state']['session']['hand']
        if hand not in os.listdir('media/temp'):
            return yandex.send_text(event, choice(phrases.wait),
                                    {'state': 'ждите генерации случайного изображения'})
        return yandex.send_image(event, choice(phrases.random), [hand, ],
                                 {'state': 'еще случайный?'})

    else:
        return 'Ничерта не сработало, пишите админу. Для админа: \n' + str(event)
