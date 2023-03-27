from requests import Session
from multiprocessing import Pool


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


def post_image(image):
    session = Session()
    session.headers.update({'Authorization': 'OAuth y0_AgAAAABFyZJlAAT7owAAAADfKD6vZDWCeWvtTCmOD6vqlbc6ZwlirQo'})
    return session.post('https://dialogs.yandex.net/api/v1/skills/6c8cbf72-0a69-4c8b-a81e-332d023fffc8/images',
                        {'Content-Type': 'multipart/form-data'},
                        files={'file': (image, open(f'media/{image}', 'rb'))}).json()['image']['id']


def send_image(event, text, images: list, state_change: dict = ()):
    """ Отправить изображение """

    image_ids = []
    if len(images) == 1:
        # записывая id всех изображений в список
        image_ids.append(post_image(images[0]))

    else:
        with Pool(len(images)) as p:
            image_ids += p.map(post_image, images)

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
