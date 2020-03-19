import pandas as pd
import datetime
import numpy as np
import os


def fakeing(length):
    data_key = ['city', 'company', 'date', 'price']

    df = pd.DataFrame(columns=data_key)

    citys = ['CAN', 'PEK', 'CTU', 'WUH']
    companies = ['AB', 'BB', 'XX', 'YZ']
    dates = [datetime.datetime.today().date() + datetime.timedelta(days=d) for d in range(30)]

    city_list = np.random.choice(citys, length)
    com_list = np.random.choice(companies, length)
    date_list = np.random.choice(dates, length)
    price_list = np.random.randint(300, 600, length)

    df['city'] = city_list
    df['company'] = com_list
    df['date'] = date_list
    df['price'] = price_list
    df = df.sort_values(['date', 'city', 'company']).reset_index(drop=True)

    return df


def one_fake(length=1000):
    path = './fake_data/'
    if not os.path.exists(path):
        os.makedirs(path)

    df = fakeing(length)
    df.to_csv(path + 'fake_data.csv', index=False)


def many_fake(length=100, nums=20):
    path = './fake_data/'
    if not os.path.exists(path):
        os.makedirs(path)

    for i in range(nums):
        df = fakeing(length)
        df.to_csv(path + 'fake_data_%d.csv' % i, index=False)
