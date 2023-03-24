from src.yandex import send_image


def handler(event, context):
    return send_image(event=event, images=['base.png'], text='тест', state=10)



# Authorization: OAuth y0_AgAAAABFyZJlAAT7owAAAADfKD6vZDWCeWvtTCmOD6vqlbc6ZwlirQo

