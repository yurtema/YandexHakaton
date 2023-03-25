import requests
import os


def end_session(event, text):
    """ Закончить сессию, отправив заданный текст """
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {

            'text': text,

            'end_session': 'true'

        }
    }


def send_text(event, text, state_change: dict = ()):
    """ Отправить текст и изменить заданные переменные """

    # Записать существующие переменные
    state = event['state']['session']
    # Заменить нужные
    for i in state_change:
        state[i] = state_change[i]

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {

            'text': text,

            'end_session': 'false'

        },
        "session_state": state
    }


def send_image(event, text, images: list):
    """ Отправить изображение """

    # Подсоедениться к сессии http запроса и отправить все нужные изображения в хранилище Яндекса
    session = requests.Session()
    session.headers.update({'Authorization': 'OAuth y0_AgAAAABFyZJlAAT7owAAAADfKD6vZDWCeWvtTCmOD6vqlbc6ZwlirQo'})
    image_ids = []
    for image in images:
        # записывая id всех изображений в список
        image_ids.append(
            session.post('https://dialogs.yandex.net/api/v1/skills/6c8cbf72-0a69-4c8b-a81e-332d023fffc8/images',
                         {'Content-Type': 'multipart/form-data'},
                         files={'file': (image, open(f'media/temp/{image}', 'rb'))}).json()['image']['id'])

    # Записать существующие переменные
    state = event['state']['session']
    # Запросить id изображений уже хранящийхся в переменной и добавить к полученному новые id
    # Если такой строчки еще нет, создать
    state['image_ids'] = state.get(['image_ids'], []) + image_ids

    if len(images) == 1:

        answer = {
            'version': event['version'],
            'session': event['session'],
            'response': {

                'text': '',

                'end_session': 'false',

                'card': {
                    'type': 'BigImage',
                    'image_id': image_ids[0],
                    'title': text
                }

            },
            "session_state": state
        }

    else:

        answer = {
            'version': event['version'],
            'session': event['session'],
            'response': {

                'text': '',

                'end_session': 'false',

                'card': {
                    'header': {
                        'text': text,
                    },
                    'type': 'ItemsList',
                    'items': [{'image_id': i} for i in image_ids]
                }

            },
            "session_state": state
        }

    # for i in image_ids:
    #     session.delete(url=f'https://dialogs.yandex.net/api/v1/skills/6c8cbf72-0a69-4c8b-a81e-332d023fffc8/images/{i}')

    for i in images:
        os.remove(f'media/temp/{i}')

    return answer
