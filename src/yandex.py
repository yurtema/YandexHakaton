from requests import Session
from multiprocessing import Pool
from json import load, dump

session = Session()
session.headers.update({'Authorization': 'OAuth y0_AgAAAABFyZJlAAT7owAAAADfKD6vZDWCeWvtTCmOD6vqlbc6ZwlirQo'})


def send(image, files):
    if image in files:
        return files.get(image)
    image_id = session.post('https://dialogs.yandex.net/api/v1/skills/6c8cbf72-0a69-4c8b-a81e-332d023fffc8/images',
                            {'Content-Type': 'multipart/form-data'},
                            files={'file': (image, open(f'media/{image}', 'rb'))}).json()['image']['id']
    files[image] = image_id
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
    with open('src/files.json', 'w') as file:
        test = file.write('{}')

    with open('files.json', encoding='utf8', mode='r') as file:
        uploaded_files = load(file)

    image_ids = []
    if len(images) == 1:
        # записывая id всех изображений в список
        image_ids.append(send(images[0], uploaded_files))

    else:
        sequence = [(i, uploaded_files) for i in images]
        with Pool(len(images)) as p:
            image_ids += p.starmap(send, sequence)

    with open('files.json', encoding='utf8', mode='w') as file:
        dump(uploaded_files, file)

    # Записать существующие переменные
    state = event['state']['session']
    # Запросить id изображений уже хранящийхся в переменной и добавить к полученному новые id
    # Если такой строчки еще нет, создать
    if 'image_ids' in state:
        state['image_ids'] += image_ids
    else:
        state['image_ids'] = image_ids
    # Заменить нужные
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

    return answer
