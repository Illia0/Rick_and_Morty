import psycopg2
import argparse

def get_characters(value = 10):
    try:
        connection = psycopg2.connect(
            host='',
            user='',
            password='',
            database='',
            port=1234
        )
        connection.autocommit = True
        result_data = []
        with connection.cursor() as cursor:
            cursor.execute('select count(id) from episodes')
            num_episodes = cursor.fetchone()
            perc_episode = num_episodes[0] * value / 100
            cursor.execute('select name, episode from characters')
            data = []
            iter = ''
            while iter != None:
                data.append(cursor.fetchone())
                iter = data[-1]
            for i in range(len(data) - 1):
                num_in = len(data[i][1])
                if num_in > perc_episode:
                    result_data.append((data[i][0], num_in))
            result_data.sort(key=lambda x: x[1], reverse=True)
            for i in range(len(result_data)):
                if i == 10:
                    break
                print(result_data[i])
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

def get_episodes(value = 1):
    try:
        connection = psycopg2.connect(
            host='',
            user='',
            password='',
            database='',
            port=1234
        )
        connection.autocommit = True
        result_data = []
        with connection.cursor() as cursor:
            cursor.execute('select episode from characters where id = {}'.format(value))
            episodes = cursor.fetchone()
            for i in episodes[0]:
                id = ''
                while i[-1] != '/':
                    id = i[-1] + id
                    i = i[:-1]
                cursor.execute('select name from episodes where id = {}'.format(id))
                result_data.append(cursor.fetchone())
            result_data.sort()
            for j in range(len(result_data)):
                if j == 10:
                    break
                print(result_data[j][0])
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-value', type=int, help="Input int value from 0 to 100")
    parser.add_argument('-type', type=str, help="Input int value")
    args = parser.parse_args()
    if args.type == 'characters':
        get_characters(args.value)
    elif args.type == 'episodes':
        get_episodes(args.value)
    else:
        print('Incorrect input')


#py ram_top.py -value=15 -type=characters
#py ram_top.py -value=3 -type=episodes
