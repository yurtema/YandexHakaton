from src import yandex, phrases, image
from random import choice, randint
from os import listdir, remove
from threading import Thread


def start_generating_random():
    rgb_base = [randint(0, 255), randint(0, 255), randint(0, 255)]
    rgb_dec = [randint(0, 255), randint(0, 255), randint(0, 255)]

    # dirs = listdir('media')
    # dirs.remove('temp')
    dirs = ['spots']
    direct = choice(dirs)
    sample = f'{direct}/{str(randint(1, len(listdir(f"media/{direct}")) // 3))}'

    thread = Thread(target=image.recolor_hand, args=(sample, rgb_base, rgb_dec))
    thread.start()

    if len(listdir('media/temp')) >= 100:
        for i in range(70):
            remove('media/temp/' + choice(listdir('media/temp')))

    return f'{sample[-1]}_{rgb_base}_{rgb_dec}.png'


def overlaps(user, target):
    return [1 for i in user.replace(',', ' ').replace('.', ' ').replace('?', ' ').split() if i in target] != []


def is_rgb(value):
    value = value.split(' ')
    if len(value) != 3:
        return False
    try:
        value = list(map(int, value))
    except ValueError:
        return False
    if not ((0 <= value[0] <= 255) and (0 <= value[1] <= 255) and (0 <= value[2] <= 255)):
        return False
    return [value[0], value[1], value[2]]


def handler(event):
    # Начало
    if event['state']['session'] == {}:
        return yandex.send_text(event, choice(phrases.greeting), {'state': 'начнем?'})

    user_text = event['request']['original_utterance'].lower()
    state = event['state']['session']['state']
    if len(listdir()) <= 5:
        start_generating_random()
    elif len(listdir()) <= 20 and randint(1, 2) == 1:
        start_generating_random()
    elif len(listdir()) <= 50 and randint(1, 4) == 1:
        start_generating_random()
    elif len(listdir()) <= 70 and randint(1, 5) == 1:
        start_generating_random()

    # Начинать или нет?
    # да - запустить генерацию изображения со случайными параметрами
    # нет - закончить навык
    if state == 'начнем?':
        if overlaps(user_text, phrases.yes):
            return yandex.send_text(event, choice(phrases.start_skill),
                                    {'state': 'случайный?'})

        if overlaps(user_text, phrases.no):
            return yandex.end_session(event, choice(phrases.end_session))

        if user_text == 'сбрось':
            with open('src/files.json', 'w', encoding='utf8') as file:
                file.write('{}')
            return yandex.send_text(event, 'да')

        if user_text in ['что ты умеешь', 'что ты умеешь?']:
            return yandex.send_text(event, 'Я умею создавать дизайны маникюра по твоему выбору или '
                                           'генерировать случайные. Начнем?')

        if overlaps(user_text, phrases.help_phrases):
            return yandex.send_text(event, 'Начинаем работу навыка? \n да - начать \n нет - не начинать')

        return yandex.send_text(event, choice(phrases.what))

    # Случайный или нет?
    # рандом - прислать случайное изображение из папки temp
    # конкретный - спросить про цвет
    if state == 'случайный?':
        if overlaps(user_text, phrases.user_random):
            return yandex.send_image(event, choice(phrases.random), ['temp/' + choice(listdir('media/temp')), ],
                                     {'state': 'еще случайный?'})

        if overlaps(user_text, phrases.specific_choise):
            return yandex.send_text(event, choice(phrases.what_color) + '\nВарианты:\n' + 'случайный\n' + '\n'.join(
                phrases.colors.keys()), {'state': 'цвет?'})

        if overlaps(user_text, phrases.help_phrases):
            return yandex.send_text(event, 'Прислать случайно сгенерированный дизайн? \n'
                                           'рандом/случайный - прислать случайный \n'
                                           'конкретный/определенный - начать собирать свой дизайн')

        return yandex.send_text(event, choice(phrases.what))

    # Отправлять ли еще одно случайное изображение или закончить?
    # да - отправить случайное изображение из папки temp и спросить снова
    # нет - закончить навык
    if state == 'еще случайный?':
        if overlaps(user_text, phrases.yes):
            return yandex.send_image(event, choice(phrases.random), ['temp/' + choice(listdir('media/temp'))],
                                     {'state': 'еще случайный?'})

        if overlaps(user_text, phrases.no):
            return yandex.end_session(event, choice(phrases.end_session))

        if overlaps(user_text, phrases.help_phrases):
            return yandex.send_text(event, 'Еще один случайный? \n'
                                           'да - прислать новый случайный \n '
                                           'нет - закончить навык')

        return yandex.send_text(event, choice(phrases.what))

    # Какой цвет?
    # рандом - выбрать случайный цвет
    # цвет - записать выбранный
    if state == 'цвет?':
        dirs = listdir('media')
        dirs.remove('temp')
        if overlaps(user_text, phrases.user_random):
            rgb_base = (randint(0, 255), randint(0, 255), randint(0, 255))
            return yandex.send_text(event,
                                    choice(phrases.what_theme) + '\nВарианты:\n' + 'случайный\n' + '\n'.join(dirs),
                                    {'state': 'тема дек?', 'base_color': rgb_base})

        if overlaps(user_text, phrases.colors):
            return yandex.send_text(event,
                                    choice(phrases.what_theme) + '\nВарианты:\n' + 'случайный\n' + '\n'.join(dirs),
                                    {'state': 'тема дек?', 'base_color': phrases.colors[user_text]})

        if overlaps(user_text, phrases.help_phrases):
            return yandex.send_text(event, 'Выберите основной цвет (цвет ногтя) \n'
                                           'код цвета в формате rgb (например 65 212 34) - выбрать цвет \n'
                                           'название цвета - выбрать цвет \n '
                                           'рандом/случайный - взять случайный цвет')

        if is_rgb(user_text):
            return yandex.send_text(event,
                                    choice(phrases.what_theme) + '\nВарианты:\n' + 'случайный\n' + '\n'.join(dirs),
                                    {'state': 'тема дек?', 'base_color': is_rgb(user_text)})

        return yandex.send_text(event, choice(phrases.error_color) + '\nВарианты:\n' + 'случайный\n' + '\n'.join(
            phrases.colors.keys()))

    # Из какой папки брать декор?
    # рандом - выбрать случайную тему
    # тема - записать выбранную
    if state == 'тема дек?':

        dirs = listdir('media')
        dirs.remove('temp')
        random_theme = choice(dirs)

        if overlaps(user_text, phrases.user_random):
            return yandex.send_text(event, choice(phrases.what_design), {'state': 'дизайн?',
                                                                         'dec_theme': random_theme})

        if overlaps(user_text, dirs):
            return yandex.send_text(event, choice(phrases.what_design), {'state': 'дизайн?',
                                                                         'dec_theme': user_text})

        if overlaps(user_text, phrases.help_phrases):
            return yandex.send_text(event, 'Выберите тему для дизайна \n'
                                           'тема - выбрать тему \n '
                                           'рандом/случайный - взять случайную тему')

        return yandex.send_text(event, choice(phrases.error_theme) + '\nВарианты:\n' + 'случайный\n' + '\n'.join(dirs))

    # Все ниже писалось после полуночи

    # Какой дизайн?
    # номер дизайна - записать дизайн
    # каталог - начать показывать возможные варианты
    if state == 'дизайн?':
        theme = event['state']['session']['dec_theme']

        available = {i[0] for i in listdir('media/' + theme)}

        if overlaps(user_text, available):
            return yandex.send_text(event, choice(phrases.what_design_color) + '\nВарианты:\n' + 'случайный\n' +
                                    '\n'.join(phrases.colors.keys()), {'state': 'цвет дизайна?', 'design': user_text})

        if overlaps(user_text, phrases.user_random):
            return yandex.send_text(event, choice(phrases.what_design_color) + '\nВарианты:\n' + 'случайный\n' +
                                    '\n'.join(phrases.colors.keys()),
                                    {'state': 'цвет дизайна?', 'design': choice(list(available))})

        if overlaps(user_text, phrases.available):
            images = [f'{theme}/{i}_hand.png' for i in available]
            if len(images) > 10:
                return yandex.send_image(event, 'страница 1/' + str(len(images) // 10), images, {'state': 'каталог',
                                                                                                 'page': 1})
            return yandex.send_image(event, choice(phrases.catalog), images)

        if overlaps(user_text, phrases.help_phrases):
            return yandex.send_text(event, 'Выберите дизайн \n'
                                           'порядковый номер дизайна - выбрать дизайн \n '
                                           'рандом/случайный - взять случайную тему')

        return yandex.send_text(event, choice(phrases.what))

    if state == 'цвет дизайна?':
        theme = event['state']['session']['dec_theme']
        design = event['state']['session']['design']
        base_color = event['state']['session']['base_color']

        if overlaps(user_text, phrases.user_random):
            dec_color = [randint(0, 255), randint(0, 255), randint(0, 255)]
            file = f'{theme}/{design}'
            thread = Thread(target=image.recolor_hand, args=(file, base_color, dec_color))
            thread.start()
            try:
                dec_color = [i for i in phrases.colors if phrases.colors[i] == dec_color][0]
            except IndexError:
                pass
            try:
                base_color = [i for i in phrases.colors if phrases.colors[i] == base_color][0]
            except IndexError:
                pass
            return yandex.send_text(event,
                                    f'Замечательно:\n тема: {theme} \nдизайн: {design} \nосновной цвет: {base_color} '
                                    f'\nдоп цвет: {dec_color} \nВсе так?',
                                    {'state': 'все так?', 'file': f'{design}_{base_color}_{dec_color}.png'})

        if overlaps(user_text, phrases.colors):
            dec_color = phrases.colors[user_text]
            file = f'{theme}/{design}'
            thread = Thread(target=image.recolor_hand, args=(file, base_color, dec_color))
            thread.start()
            try:
                dec_color = [i for i in phrases.colors if phrases.colors[i] == dec_color][0]
            except IndexError:
                pass
            try:
                base_color = [i for i in phrases.colors if phrases.colors[i] == base_color][0]
            except IndexError:
                pass
            return yandex.send_text(event,
                                    f'Замечательно:\n тема: {theme} \nдизайн: {design} \nосновной цвет: {base_color} '
                                    f'\nдоп цвет: {dec_color} \nВсе так?',
                                    {'state': 'все так?', 'file': f'{design}_{base_color}_{dec_color}.png'})

        if overlaps(user_text, phrases.help_phrases):
            return yandex.send_text(event, 'Выберите цвет дизайна \n'
                                           'название цвета - выбрать цвет \n '
                                           'код цвета в формате rgb (например 65 212 34) - выбрать цвет \n'
                                           'рандом/случайный - взять случайный цвет \n')

        if is_rgb(user_text):
            dec_color = is_rgb(user_text)
            file = f'{theme}/{design}'
            thread = Thread(target=image.recolor_hand, args=(file, base_color, dec_color))
            thread.start()
            try:
                dec_color = [i for i in phrases.colors if phrases.colors[i] == dec_color][0]
            except IndexError:
                pass
            try:
                base_color = [i for i in phrases.colors if phrases.colors[i] == base_color][0]
            except IndexError:
                pass
            return yandex.send_text(event,
                                    f'Замечательно:\n тема: {theme} \nдизайн: {design} \nосновной цвет: {base_color} '
                                    f'\nдоп цвет: {dec_color} \nВсе так?',
                                    {'state': 'все так?', 'file': f'{design}_{base_color}_{dec_color}.png'})

        return yandex.send_text(event, choice(phrases.error_color) + '\nВарианты:\n' + 'случайный\n' + '\n'.join(
            phrases.colors.keys()))

    if state == 'все так?':

        if overlaps(user_text, phrases.yes):
            if event['state']['session']['file'] in listdir('media/temp'):
                return yandex.send_image(event, 'Все готово:', ['temp/' + event['state']['session']['file'], ])
            else:
                return yandex.send_text(event, 'Простите, изображение ещё не сгенерированно. Попробовать еще раз?',
                                        {'state': 'ждите генерации'})

        if overlaps(user_text, phrases.no):
            return yandex.send_text(event,
                                    'Тогда давайте еще раз попробуем. Какой хотите главный цвет?' + '\nВарианты:\n' +
                                    'случайный\n' + '\n'.join(phrases.colors.keys()), {'state': 'цвет?'})

        if overlaps(user_text, phrases.help_phrases):
            return yandex.send_text(event, 'Все ли правильно? \n'
                                           'да - утвердить параметры изображения и прислать его \n '
                                           'нет - начать выбирать заново')

        return yandex.send_text(event, choice(phrases.what))

    if state == 'ждите генерации':
        if overlaps(user_text, phrases.yes):
            if event['state']['session']['file'] in listdir('media/temp'):
                return yandex.send_image(event, 'Все готово:', ['temp/' + event['state']['session']['file'], ])
            else:
                return yandex.send_text(event, 'Простите, изображение ещё не сгенерированно. Попробовать еще раз?')

        if overlaps(user_text, phrases.no):
            return yandex.send_text(event,
                                    'Тогда давайте еще раз попробуем. Какой хотите главный цвет?' + '\nВарианты:\n' +
                                    'случайный\n' + '\n'.join(phrases.colors.keys()), {'state': 'цвет?'})

        if overlaps(user_text, phrases.help_phrases):
            return yandex.send_text(event, 'Изображению нужно время для генерации, простите пожалуйста. Может '
                                           'понадобиться несколько секунд, максимум - 10 секунд \n'
                                           'да - попробовать прислать то же изображение \n '
                                           'нет - начать выбирать заново')

        return yandex.send_text(event, choice(phrases.what))

    else:
        return 'Ничерта не сработало, пишите админу. Для админа: \n' + str(event)
