# work with header
import requests
import json
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import random


def make_request(dep_city='bjs',
                 arr_city='can',
                 date='2020-04-04',
                 hasChild=False,
                 hasBaby=False,
                 classType='ALL', last_ref="https://flights.ctrip.com/"):
    '''
    函数用于根据参数对ctrip的api站点发送请求并返回routeList数据
    :param dep_city:始发城市
    :param arr_city:到达城市
    :param date:起飞日期
    :param hasChild:是否有儿童
    :param hasBaby:是否有婴儿
    :param classType:舱位类型
    :return: routeList 用于paser_route
    :return: next_referer 用于下一次的headers
    '''

    # 定义访问相关参数
    referer = 'https://flights.ctrip.com/'
    api_url = 'https://flights.ctrip.com/itinerary/api/12808/products'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36"
                      " (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        "Referer": referer,
        "Content-Type": "application/json",  # 声明文本类型为 json 格式
    }

    this_date = str(pd.to_datetime(date).date())

    next_referer = 'https://flights.ctrip.com/itinerary/oneway/'
    next_referer += dep_city + '-' + arr_city + '?' + 'date=' + this_date
    print("last ref", last_ref)
    print("new ref", next_referer)

    # 载入请求json并根据搜索条件更新数据
    re_json = json.load(open('./json/request.json', "r"))

    re_json['date'] = date
    re_json['hasChild'] = hasChild
    re_json['hasBaby'] = hasBaby
    re_json['airportParams'][0]['dcity'] = dep_city
    re_json['airportParams'][0]['acity'] = arr_city
    re_json['airportParams'][0]['date'] = date

    headers['Referer'] = last_ref

    # 利用访问数据对API站点进行访问，获取返回数据
    r = requests.post(api_url, data=json.dumps(re_json), headers=headers)
    respone_json = r.json()

    json_dir = './json/response.json'

    # 从返回结果数据中提取route出列表
    data = respone_json['data']
    routeList = data['routeList']

    return routeList, next_referer


def route_parser(routeList):
    """
    函数用于从route的集合中遍历每个舱位及其价格
    对于一个航班，最终返回母舱位中的最低价
    :param routeList:
    :return: pd.DataFrame 每一行是一个母舱位最低价
    """
    class_lines = []

    # 遍历所有route
    for i, route0 in enumerate(routeList):

        legs = route0['legs']
        print("方案%d/%d" % (i, len(routeList)))

        # 遍历所有leg
        for j, legs0 in enumerate(legs):
            print("  航节%d" % j)

            # 跳过非航班的leg
            if 'flightId' not in legs0:
                print("  这个leg不是飞机")
                continue

            # 航班信息
            flight = legs0['flight']
            flightNumber = flight['flightNumber']

            departureAirportInfo = flight['departureAirportInfo']
            arrivalAirportInfo = flight['arrivalAirportInfo']

            dep_airport = departureAirportInfo['airportTlc']
            arr_airport = arrivalAirportInfo['airportTlc']

            departureDate = flight['departureDate']
            arrivalDate = flight['arrivalDate']

            print("        航班%s %s-%s" % (flightNumber, dep_airport, arr_airport))
            print("        %s起飞 %s到达" % (departureDate[:-3], arrivalDate[:-3]))

            # 舱位信息
            cabins = legs0['cabins']

            min_price = {}
            min_cabinClass = {}

            # 遍历所有舱位信息 记录母舱位最低价格
            for k, cabins0 in enumerate(cabins):
                cabinClass = cabins0['cabinClass']
                priceClass = cabins0['priceClass']
                price = cabins0['price']['price']

                if cabinClass not in min_price:
                    min_price[cabinClass] = price
                    min_cabinClass[cabinClass] = priceClass
                else:
                    if min_price[cabinClass] > price:
                        min_price[cabinClass] = price
                        min_cabinClass[cabinClass] = priceClass

                # print("  %s舱价格(%s) %d元" % (cabinClass, priceClass, price))

            # 存储下所有的最低母舱位的价格信息
            for l, cls in enumerate(min_price.keys()):
                print("        %s舱(%s)最低价格 %d元" % (cls, min_cabinClass[cls], min_price[cls]))
                class_lines.append([flightNumber, dep_airport, arr_airport, departureDate[:-3], arrivalDate[:-3], cls,
                                    min_cabinClass[cls], min_price[cls]])

    keys = ['flight_no', 'dep', 'arr', 'dep_date', 'arr_date', 'cabin_class', 'price_class', 'price']
    class_df = pd.DataFrame(class_lines, columns=keys)

    return class_df


def draw_price_carrier(df, dep, arr, tw0=8, tw1=10):
    df = df.copy()

    title = 'lowest price in %s-%s [%d,%d)' % (dep, arr, tw0, tw1)

    df = df.loc[df['arr'] == arr]
    df = df.loc[df['dep'] == dep]

    df = df.loc[pd.to_datetime(df.dep_date).dt.hour < tw1]
    df = df.loc[pd.to_datetime(df.dep_date).dt.hour >= tw0]

    df['carrier'] = df['flight_no'].agg(lambda x: x[:2])
    df['dep_date'] = pd.to_datetime(df['dep_date']).dt.date
    y_class_df = df.loc[df['cabin_class'] == 'Y']
    min_df = y_class_df.groupby(['dep_date', 'carrier'])['price'].min()
    min_df = min_df.unstack()

    lg = df['carrier'].unique()
    print(lg)

    plt.figure(figsize=(8, 5))
    for cr in lg:
        plt.plot(min_df.index, min_df[cr], 'o:', markerfacecolor='white')

    plt.legend(labels=lg, loc='best')
    plt.title(title)

    plt.show()


def get_future_data(day_begin=1, day_end=30, dep_city='bjs', arr_city='can'):
    # 取未来1到30天起飞的日期
    f7_dates = [datetime.datetime.now().date() +
                datetime.timedelta(days=x) for x in range(day_begin, day_end + 1)]
    f7_dates = [str(d) for d in f7_dates]

    date_list = []

    ref = "https://flights.ctrip.com/"

    # 循环更新参数并进行请求 获得返回值
    for i, date in enumerate(f7_dates):
        print("crawling the %s  %d/%d" % (date, i, len(f7_dates)))
        # 输入参数进行请求
        r_list, new_ref = make_request(date=date, dep_city=dep_city, arr_city=arr_city, last_ref=ref)
        ref = new_ref

        # 对返回数据进行解析提取
        date_df = route_parser(routeList=r_list)
        # 将每个日期的DataFrame存入到list
        date_list.append(date_df)
        time.sleep(4.3333 + random.random() * 2)

    # 对多个日期数据进行连接
    future_df = pd.concat(date_list, axis=0)
    future_df['download_date'] = datetime.datetime.now()

    return future_df


if __name__ == '__main__':
    trip_o = 'can'
    trip_d = 'bjs'

    data_df = get_future_data(day_begin=7, day_end=13, dep_city=trip_o, arr_city=trip_d)

    # 存储数据
    data_df.to_csv(trip_o + trip_d + '_7to13days.csv', index=False)

    # 绘制票价图像
    draw_price_carrier(data_df, dep='CAN', arr='PEK', tw0=8, tw1=10)
