from wandaapp.models import Transaction
import datetime
import string, random
import numpy as np
from numpy.random import choice

def generate_data(request, n_registers):

    c_date = datetime.datetime.now() - datetime.timedelta(days=n_registers/10)

    for i in range(n_registers):

        user_id = get_id()
        user_gender = get_gender()
        companion_type, companion_gender = get_companion()
        sons_age = get_sons()
        travel_reason = get_reason(sons_age)
        origin, type_of_traveler = get_origin()
        days_of_travel = get_days()
        location = get_location()

        for d in range(days_of_travel):


            data = { 'date':c_date,
                     'category':get_category(),
                     'product':get_product(),
                     'subsector':get_sector(),
                     'price':get_price(),
                     'location':location
                     }


def get_id(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_gender():
    options = ['H', 'M', 'NA']
    p = [0.5, 0.1, 0.1, 0.3]
    return np.random.choice(options, 1, p=p)