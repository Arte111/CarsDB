import re
import shelve
from pywebio.input import input_group, input, select, NUMBER, TEXT
from pywebio.output import put_buttons, put_text, put_table, clear, use_scope, set_scope

FILENAME = 'cars_oop/cars'  # file with database


class Car(object):
    def __init__(self, mark, model, color, power, drive_unit, transmission, cost, max_speed):
        self.mark = mark
        self.model = model
        self.color = color
        self.power = power
        self.drive_unit = drive_unit
        self.transmission = transmission
        self.cost = cost
        self.max_speed = max_speed


class Regular(object):  # for check on correct
    def state_number(num):
        if not(re.fullmatch(r'\b[а-я]\d{3}[а-я]{2}\d{2,3}\b', num)):
            return 'Not state number'

    def anti_obscene(text):
        obscene = ['говно', 'залупа', 'пенис', 'хер', 'давалка', 'хуй', 'блядина',
                   'головка', 'шлюха', 'жопа', 'член', 'еблан', 'петух', 'мудила',
                   'рукоблуд', 'ссанина', 'очко', 'блядун', 'вагина',
                   'сука', 'ебланище', 'влагалище', 'пердун', 'дрочила',
                   'пидр', 'пизда', 'туз', 'малафья', 'гомик', 'мудила', 'пилотка', 'манда',
                   'анус', 'вагина', 'путана', 'педрила', 'шалава', 'хуила', 'мошонка', 'елда']
        if set(obscene) & set(text.lower().split()):
            return 'Не материтесь, сударь. Давайте на французском'


def main():
    def add():
        clear('scope2')
        data = input_group('Info about auto', [
            input('state number', type=TEXT, name='state_number', validate=Regular.state_number),
            input('mark', type=TEXT, name='mark', validate=Regular.anti_obscene),
            input('model', type=TEXT, name='model', validate=Regular.anti_obscene),
            input('color', type=TEXT, name='color', validate=Regular.anti_obscene),
            input('power', type=NUMBER, name='power'),
            select('drive unit', options=["AWD", "4WD", "RWD", "FWD"], name='drive_unit'),
            select('transmission', options=["Manual", "Automatic", "CVT transmissions", "Hybrid"], name='transmission'),
            input('cost, $', type=NUMBER, name='cost'),
            input('max speed, km/h', type=NUMBER, name='max_speed')
        ])

        with shelve.open(FILENAME) as car:
            car[data['state_number']] = Car(data['mark'], data['model'], data['color'], data['power'],
                                            data['drive_unit'], data['transmission'], data['cost'], data['max_speed'])

        put_text("Auto was added", scope='scope2')

    def show():
        clear('scope2')
        state_number = input('Enter state number', validate=Regular.state_number)

        with shelve.open(FILENAME) as car:
            data = car[state_number].__dict__

        with use_scope('scope2'):
            put_table([[state_number, data['mark'], data['model'], data['color'], data['power'],
                        data['drive_unit'], data['transmission'], data['cost'], data['max_speed']]],
                      header=['state number', 'mark', 'model', 'color',
                              'power', 'drive_unit', 'gearbox', 'cost, $', 'max speed, km/h'])

    def show_all():
        clear('scope2')
        with shelve.open(FILENAME) as car:
            keys = list(car.keys())
            info = []
            for state_number in keys:
                data = car[state_number].__dict__
                info.append([state_number, data['mark'], data['model'], data['color'], data['power'],
                             data['drive_unit'], data['transmission'], data['cost'], data['max_speed']])
        with use_scope("scope2"):
            put_table(info, header=['state number', 'mark', 'model', 'color', 'power',
                                    'drive_unit', 'gearbox', 'cost, $', 'max speed, km/h'])

    def edit():
        clear('scope2')
        state_number = input('Enter state number', validate=Regular.state_number)

        with shelve.open(FILENAME) as car:
            data = car[state_number].__dict__

        data = input_group('Info about auto', [
            input('mark', type=TEXT, name='mark', value=f'{data["mark"]}', validate=Regular.anti_obscene),
            input('model', type=TEXT, name='model', value=f'{data["model"]}', validate=Regular.anti_obscene),
            input('color', type=TEXT, name='color', value=f'{data["color"]}', validate=Regular.anti_obscene),
            input('power', type=NUMBER, name='power', value=f'{data["power"]}'),
            select('drive unit', options=["AWD", "4WD", "RWD", "FWD"], value=f'{data["drive_unit"]}',
                   name='drive_unit'),
            select('transmission', options=["Manual", "Automatic", "CVT transmissions", "Hybrid"],
                   value=f'{data["transmission"]}', name='gearbox'),
            input('cost, $', type=NUMBER, name='cost', value=f'{data["cost"]}'),
            input('max speed, km/h', type=NUMBER, name='max_speed', value=f'{data["max_speed"]}')
        ])

        with shelve.open(FILENAME) as car:  # save in file
            car[state_number] = Car(data['mark'], data['model'], data['color'], data['power'],
                                    data['drive_unit'], data['transmission'], data['cost'], data['max_speed'])

        put_text("Auto was edited", scope='scope2')

    def delete():
        clear('scope2')
        state_number = input('Enter state number to delete auto', validate=Regular.state_number)

        try:
            shelve.open(FILENAME).pop(state_number)
            put_text("auto was deleted", scope='scope2')
        except: put_text("auto wasn't found", scope='scope2')


    '''Buttons'''
    set_scope('scope1', 'ROOT')
    set_scope('scope2', 'ROOT')
    put_buttons(["Add auto", "Show info", "Show all", "Edit auto", "Delete auto"],
                onclick=[add, show, show_all, edit, delete], scope='scope1')


if __name__ == '__main__':
    from pywebio import start_server
    start_server(main)
