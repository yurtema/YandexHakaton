import requests


def end_session(event, text):
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {

            'text': text,

            'end_session': 'true'

        }
    }


def send_text(event, text, state, ids):
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {

            'text': text,

            'end_session': 'false'

        },
        "session_state": {
            'state': state,
            'image_ids': ids
        }
    }


def send_image(event, text, images: list, state, ids):
    session = requests.Session()
    session.headers.update({'Authorization': 'OAuth y0_AgAAAABFyZJlAAT7owAAAADfKD6vZDWCeWvtTCmOD6vqlbc6ZwlirQo'})
    image_ids = []
    for image in images:
        image_ids.append(
            session.post('https://dialogs.yandex.net/api/v1/skills/6c8cbf72-0a69-4c8b-a81e-332d023fffc8/images',
                         {'Content-Type': 'multipart/form-data'},
                         files={'file': (image, open(f'media/{image}', 'rb'))}).json()['image']['id'])

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
            "session_state": {
                'state': state,
                'image_ids': ids
            }
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
            "session_state": {
                'state': state,
                'image_ids': ids
            }
        }

    for i in image_ids:
        session.delete(url=f'https://dialogs.yandex.net/api/v1/skills/6c8cbf72-0a69-4c8b-a81e-332d023fffc8/images/{i}')

    return answer
