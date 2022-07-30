import os
import datetime
import random

def my_shuffle(word):
    letters = list(word)
    random.shuffle(letters)
    res_word = ''
    for i in letters:
        res_word += i
    return res_word



if __name__ == '__main__':
    if os.path.exists('squanch') == False:
        os.mkdir('squanch')
    path = os.getcwd() + '\squanch\{}_squanch.txt'.format(str(datetime.date.today()))
    try:
        my_file = open(path, mode='w+')
        my_file.write("let`s {}".format(my_shuffle('squanch')))
    except OSError:
        print('Failed creating the file')
    finally:
        my_file.close()