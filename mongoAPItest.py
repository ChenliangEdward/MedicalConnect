import requests
import json
import time
from datetime import datetime

option = 0  # 1 for insert, 0 for find, -1 for delete


def insert_message(f, t, m):
    timestamp = int(time.time())
    # dt = datetime.fromtimestamp(timestamp)
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'CU8wXM1sLJLA40qxvvhVr4IaldsJY7xtZBnnJN0d6zV9cSuStUmGLSXvSGnbozSO',
    }
    json_data = {
        'dataSource': 'Cluster0',
        'database': 'test',
        'collection': 'test',
        'document': {
            'from': f,
            'to': t,
            'Message': m,
            'Datetime': str(timestamp)
        },
    }
    response = requests.post(
        'https://data.mongodb-api.com/app/data-nfawj/endpoint/data/beta/action/insertOne', headers=headers,
        json=json_data)


def find_message(f, t):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'CU8wXM1sLJLA40qxvvhVr4IaldsJY7xtZBnnJN0d6zV9cSuStUmGLSXvSGnbozSO',
    }

    json_data = {
        'dataSource': 'Cluster0',
        'database': 'test',
        'collection': 'test',
        'filter': {
            'from': f,
            'to': t
        },
    }
    response = requests.post(
        'https://data.mongodb-api.com/app/data-nfawj/endpoint/data/beta/action/find',
        headers=headers,
        json=json_data)
    my_json = response.content.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    # print(s)
    return data


def get_conversation(f, t):
    ft = find_message(f, t)
    tf = find_message(t, f)
    l1 = ft['documents']
    l2 = tf['documents']
    l = l1 + l2
    for i in l:
        i['Datetime'] = int(i['Datetime'])
    l = sorted(l, key=lambda x: x['Datetime'], reverse=False)
    return l


# insert
if option == 1:
    f = 'Edward'
    t = 'Dr.A B'
    m = 'Hello Dr.A B, I am Edward'

    # f = 'Dr.A B'
    # t = 'Edward'
    # m = 'Hello I am A'
    insert_message(f, t, m)

    print('insert finished')

# find
if option == 0:
    l = get_conversation('Edward', 'Dr.A B')
    # print(l)
    s = ""
    for i in l:
        dt = datetime.fromtimestamp(i['Datetime'])
        print(dt.strftime('%b %d %Y %I:%M%p'))
        print(i["from"] + ": " + i["Message"] + "\n")
        s = s + i["from"] + ": " + i["Message"] + "\n"
    j = json.dumps(s)
    print(j)
