import psycopg2
import requests
import json




def create_table():
    try:
        connection = psycopg2.connect(
            host='',
            user='',
            password='',
            database='',
            port=1234
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            characters = '''CREATE TABLE characters (
                            id int primary key,
                            name varchar(80),
                            status varchar(40),
                            species varchar(100),
                            type varchar(40),
                            gender varchar(40),
                            origin_name varchar(80),
                            origin_url varchar(80),
                            location_name varchar(80),
                            location_url varchar(100),
                            image varchar(100),
                            episode jsonb,
                            url varchar(100),
                            created varchar(80)
                            )'''
            locations = '''CREATE TABLE locations (
                            id int primary key,
                            name varchar(80),
                            type varchar(40),
                            dimension varchar(40),
                            residents jsonb,
                            url varchar(100),
                            created varchar(80)
                            )'''
            episodes = '''CREATE TABLE episodes (
                            id int primary key,
                            name varchar(80),
                            air_date varchar(40),
                            episode varchar(40),
                            characters jsonb,
                            url varchar(100),
                            created varchar(80)
                            )'''
            cursor.execute(characters)
            cursor.execute(locations)
            cursor.execute(episodes)
            print("[INFO] Tables were succefully created")
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def add_data(name_table, link):
    connection = psycopg2.connect(
        host='',
        user='',
        password='',
        database='',
        port=1234
    )
    connection.autocommit = True
    try:
        info = requests.get(link)
        json_data = info.json()
        pages = json_data['info']['pages']
        for iter in range(pages):
            page_info = requests.get(link + "?page={}".format(iter + 1))
            json_data = page_info.json()
            for i in range(len(json_data['results'])):
                data = []
                for tem in json_data['results'][i]:
                    if name_table == 'characters':
                        if tem == 'origin' or tem == 'location':
                            data.append(json_data['results'][i][tem]['name'])
                            data.append(json_data['results'][i][tem]['url'])
                        elif tem == 'episode':
                            data.append(json.dumps(json_data['results'][i][tem]))
                        else:
                            data.append(json_data['results'][i][tem])
                    elif name_table == 'locations':
                        if tem == 'residents':
                            data.append(json.dumps(json_data['results'][i][tem]))
                        else:
                            data.append(json_data['results'][i][tem])
                    elif name_table == 'episodes':
                        if tem == 'characters':
                            data.append(json.dumps(json_data['results'][i][tem]))
                        else:
                            data.append(json_data['results'][i][tem])
                for j in range(len(data)):
                    if type(data[j]) == str and "'" in data[j]:
                        l = data[j].find("'")
                        data[j] = data[j][:l] + "`" + data[j][l + 1:]
                with connection.cursor() as cursor:
                    try:
                        cursor.execute(
                            'INSERT INTO {} values {}'.format(name_table, tuple(data))
                        )
                    except Exception as _ex:
                        print("[INFO] Error while working with {} in PostgreSQL".format(name_table), _ex)
        print("[INFO] Add info to {} was succefully".format(name_table))
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)

    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

def update_data(name_table, link):
    connection = psycopg2.connect(
        host='',
        user='',
        password='',
        database='',
        port=1234
    )
    connection.autocommit = True
    try:
        info = requests.get(link)
        json_data = info.json()
        pages = json_data['info']['pages']
        for iter in range(pages):
            page_info = requests.get(link + "?page={}".format(iter + 1))
            json_data = page_info.json()
            for i in range(len(json_data['results'])):
                data = []
                for tem in json_data['results'][i]:
                    if name_table == 'characters':
                        if tem == 'origin' or tem == 'location':
                            data.append(json_data['results'][i][tem]['name'])
                            data.append(json_data['results'][i][tem]['url'])
                        else:
                            data.append(json_data['results'][i][tem])
                    elif name_table == 'locations':
                        data.append(json_data['results'][i][tem])
                    elif name_table == 'episodes':
                        data.append(json_data['results'][i][tem])
                for j in range(len(data)):
                    if type(data[j]) == str and "'" in data[j]:
                        l = data[j].find("'")
                        data[j] = data[j][:l] + "`" + data[j][l + 1:]
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            'select * from {} where id = {}'.format(name_table, data[0])
                        )
                        checker = cursor.fetchone()
                        for g in range(len(data)):
                            if data[g] != checker[g]:
                                cursor.execute(
                                    'delete from {} where id = {}'.format(name_table, data[0])
                                )
                                if name_table == 'character':
                                    data[11] = json.dumps(data[11])
                                elif name_table == 'locations':
                                    data[4] = json.dumps(data[4])
                                elif name_table == 'episodes':
                                    data[4] = json.dumps(data[4])
                                cursor.execute(
                                    'INSERT INTO {} values {}'.format(name_table, tuple(data))
                                )
                                break
                except Exception as _ex:
                    print("[INFO] Error while working with {} in PostgreSQL".format(name_table), _ex)
        print("[INFO] Update {} was succefully".format(name_table))
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)

    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

if __name__ == '__main__':
    create_table()
    #For characters
    add_data('characters', 'https://rickandmortyapi.com/api/character')
    update_data('characters', 'https://rickandmortyapi.com/api/character')
    #For locations
    add_data('locations', 'https://rickandmortyapi.com/api/location')
    update_data('locations', 'https://rickandmortyapi.com/api/location')
    #For characters
    add_data('episodes', 'https://rickandmortyapi.com/api/episode')
    update_data('episodes', 'https://rickandmortyapi.com/api/episode')








