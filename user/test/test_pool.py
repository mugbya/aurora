# coding = utf-8
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import json
import asyncio


NUMBERS = range(10)


def login(number):

    url = 'http://localhost:8000/test_login/'
    payload = {'username': chr(ord('a') + number)}
    r = requests.post(url, data=json.dumps(payload))
    return r.text


def test_by_futures():
    '''
    使用 concurrent.futures 测试并发
    :return:
    '''
    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        for num, result in zip(NUMBERS, executor.map(login, NUMBERS)):
            print('login({}) = {}'.format(chr(ord('a') + num), result))
    print('Use requests+ThreadPoolExecutor cost: {}'.format(time.time() - start))


async def run_scraper_tasks(executor):
    loop = asyncio.get_event_loop()
    blocking_tasks = []
    for num in NUMBERS:
        task = loop.run_in_executor(executor, login, num)
        task.__num = num
        blocking_tasks.append(task)
    completed, pending = await asyncio.wait(blocking_tasks)
    results = {t.__num: t.result() for t in completed}
    for num, result in sorted(results.items(), key=lambda x: x[0]):
        print('login({}) = {}'.format(chr(ord('a') + num), result))


def test_by_asyncio():
    '''

    :return:
    '''
    start = time.time()
    executor = ThreadPoolExecutor(10)
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run_scraper_tasks(executor))
    print('Use asyncio+requests+ThreadPoolExecutor cost: {}'.format(time.time() - start))

if __name__ == "__main__":
    test_by_asyncio()
    test_by_futures()


