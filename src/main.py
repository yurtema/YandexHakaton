from src import yandex, phrases
from random import choice


def handler(event, context):

    # Начало
    if event['state']['session'] == {}:
        return yandex.send_text(event, choice(phrases.greeting), {'state': 'начнем?'})

    # Начинать или нет? да/нет
    if event['state']['session']['state'] == 'начнем?':
        if event['request']['original_utterance'].lower() in phrases.yes:
            return yandex.send_text(event, choice(phrases.start_skill), {'state': 'слуйчаный?'})
        elif event['request']['original_utterance'].lower() in phrases.no:
            return yandex.end_session(event, choice(phrases.end_session))

        return yandex.send_text(event, choice(phrases.what))

    # Случайный или нет? да/нет
    if event['state']['session']['state'] == 'случайный?':
        if event['request']['original_utterance'].lower() in phrases.yes:
            return yandex.send_text(event, choice(phrases.random), {'state': 'слуйчаный'})
        elif event['request']['original_utterance'].lower() in phrases.no:
            return yandex.send_text(event, choice(phrases.random), {'state': 'цвет?'})

        return yandex.send_text(event, choice(phrases.what))

    # Прислать случайный дизайн
    if event['state']['session']['state'] == 'случайный':
        pass

