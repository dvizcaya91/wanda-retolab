from wandaapp.models import Transaction
import datetime
import string, random
import numpy as np

def generate_data(request, n_registers):

    c_date = datetime.datetime.now() - datetime.timedelta(days=n_registers/10)

    for i in range(n_registers):

        user_id = get_id()
        user_gender = get_option(['H', 'M', 'NA'], [0.5, 0.35, 0.15])
        companion_type = get_option(['Pareja', 'Familia', 'Amigos', 'Solo'], [0.4, 0.15, 0.15, 0.3])
        companion_gender = get_option(['H', 'M', 'NA'], [0.35, 0.5, 0.15])
        sons_age = get_option([0,1,2,3,4,5,6,7], [0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        travel_reason = get_option(['Trabajo', 'Turismo', 'Otro', 'Educación'], [0.3, 0.4, 0.2, 0.1])

        type_of_traveler = get_option(['Nacional', 'Internacional'], [0.7, 0.3])
        if type_of_traveler == 'Nacional':
            origin = get_option(['Bogota', 'Medellin', 'Cali', 'Barranquilla'], [0.4, 0.3, 0.2, 0.1])
        else:
            origin = get_option(['USA', 'Asia', 'Europa'], [0.5, 0.3, 0.2])


        days_of_travel = int(get_option([1, 5, 10, 30], [0.1, 0.3, 0.4, 0.2]))
        location = get_option(['Casanare', 'Meta', 'Arauca', 'Barranquilla'], [0.4, 0.3, 0.2, 0.1])

        for d in range(days_of_travel):

            category = get_option(['Naturaleza', 'Aventura', 'Reuniones'], [0.5, 0.3, 0.2])
            if category == 'Reuniones':
                product = get_option(['Evento', 'Congreso', 'Reunion'], [0.3, 0.3, 0.4])
            else:
                product = get_option(['Paseo ecológico', 'Cascadas', 'Avistsamiento de aves'], [0.3, 0.1, 0.6])

            data = { 'date':(c_date+datetime.timedelta(days=d)).strftime('%Y-%m-%d'),
                     'category':category,
                     'product':product,
                     'subsector':get_option(['Hotel', 'Operador', 'Agencia'], [0.1, 0.6, 0.3]),
                     'price':np.random.randint(50000, 300000),
                     'location':location,
                     'user_id':user_id,
                     'user_gender':user_gender,
                     'companion_type':companion_type,
                     'companion_gender':companion_gender,
                     'sons_age':sons_age,
                     'travel_reason':travel_reason,
                     'type_of_traveler':type_of_traveler,
                     'origin':origin
                     }

            tran = Transaction(**data)
            tran.save()

        if i%1 == 0:
            c_date += datetime.timedelta(days=1)


def get_id(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_option(options, p):
    return np.random.choice(options, 1, p=p)[0]

if __name__ == '__main__':
    generate_data('a', 3)