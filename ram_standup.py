import requests
import random
from jokeapi import Jokes
import asyncio
import time


def get_members(link, members_num = 8):
    info = requests.get(link)
    info_json = info.json()
    character_num = info_json['info']['count']
    members = []
    for i in range(members_num):
        member_id = random.randint(1, character_num)
        if member_id not in members:
            members.append(member_id)
        else:
            i -= 1
    info_members = requests.get(link + '/' + str(members))
    members_json = info_members.json()
    for i in range(len(members)):
        members[i] = members_json[i]['name']
    return members[0], members[1:]


async def print_joke(name):
    j = await Jokes()
    joke = await j.get_joke()
    if joke["type"] == "single":
        print(name + ': - ' + joke["joke"])
    else:
        print(name + ': - ' + joke["setup"])
        time.sleep(2)
        print(name + ': - ' + joke["delivery"])


if __name__ == '__main__':
    master, members = get_members("https://rickandmortyapi.com/api/character")
    print(master + ': - Standup begins. Greet participants : {}'.format(', '.join(members)))
    input()
    for member in members:
        print(master + ': - {} enters the stage'.format(member))
        time.sleep(2)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(print_joke(member))
        input()
    print(master + ': - Thanks to all comedians.', "Now let's vote for the best!")
    time.sleep(3)
    result = random.randint(0, len(members)-1)
    print(master + ': - Winner ... ' + members[result] + '.', 'Thank you viewers for coming.')
    input()


