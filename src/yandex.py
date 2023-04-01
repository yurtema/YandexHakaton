from requests import Session
from multiprocessing import Pool
from json import load, dump
from os import listdir

session = Session()
session.headers.update({'Authorization': 'OAuth y0_AgAAAABFyZJlAAT7owAAAADfKD6vZDWCeWvtTCmOD6vqlbc6ZwlirQo'})


def send(image, files):
    if image in files:
        return files.get(image)
    image_id = session.post('https://dialogs.yandex.net/api/v1/skills/6c8cbf72-0a69-4c8b-a81e-332d023fffc8/images',
                            {'Content-Type': 'multipart/form-data'},
                            files={'file': (image, open(f'media/{image}', 'rb'))}).json()['image']['id']
    return image_id


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


def send_image(event, text, images: list, state_change: dict = ()):
    """ Отправить изображение """

    if 'files.json' not in listdir('src'):
        with open('src/files.json', encoding='utf8', mode='w') as file:
            dump('{}', file)

    with open('src/files.json', encoding='utf8', mode='r') as file:
        uploaded_files = dict(load(file))

    print('что просиходит')
    image_ids = []

    if len(images) == 1:
        # записывая id всех изображений в список
        image_ids.append(send(images[0], uploaded_files))

    else:
        sequence = [(i, uploaded_files) for i in images]
        with Pool(len(images)) as p:
            image_ids = p.starmap(send, sequence)

    # for i in range(len(images)):
        # uploaded_files[images[i]] = image_ids[i]

    with open('src/files.json', encoding='utf8', mode='w') as file:
        dump(uploaded_files, file)

    state = event['state']['session']
    for i in state_change:
        state[i] = state_change[i]

    if len(images) == 1:

        answer = {
            'version': event['version'],
            'session': event['session'],
            'response': {

                'text': '',

                'end_session': 'false',

                'card': {
                    'type': 'BigImage',
                    'title': text,
                    'image_id': image_ids[0]
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

    return answer
