from src import yandex, phrases
from random import choice


def handler(event, context):
    if event['state']['session'] == {}:
        return yandex.send_text(event, choice(phrases.greeting), 'начнем?', [])

    elif event['state']['session']['state'] == 'начнем?':
        if event['request']['original_utterance'].lower() in phrases.yes:
            return yandex.send_text(event, choice(phrases.start_skill), 'случайный?', [])
        else:
            return yandex.end_session(event, choice(phrases.end_session))

