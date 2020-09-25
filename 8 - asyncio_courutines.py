"""Экземпляры класса task (действия которые должны выполянтся асинхронно) - контейнеры для корутин
Future - это класс-заглушка, ведь функция должна что то возвращать.
Асинхронная функция тут же отдает результат Future. И контроль выполнения отдается нам обратно.
В джаваскрипте эта сущность называется Promise

Event Loop:
    coroutine > Task (Future)"""


import asyncio
from time import time


# Декоратор делает из функции - генераторную функцию
@asyncio.coroutine
def print_nums():
    num = -1
    while True:
        print(num)
        num += 1
        yield from asyncio.sleep(1)


@asyncio.coroutine
def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print("{} seconds have passed".format(count))
        count +=1
        yield from asyncio.sleep(1)


# Здесь опишем событийный цикл
# Своеобразный диспетчер
@asyncio.coroutine
def main():
    # Задачи первого рода. Корутину оборачиваем в экземпляр класса task
    task1 = asyncio.ensure_future(print_nums())
    # Задачи второго рода
    task2 = asyncio.ensure_future(print_time())

    # Ставим задачи в очередь. Дожидаемся результата с помощью метода gather
    yield from asyncio.gather(task1, task2)

if __name__ == '__main__':
    loop = asyncio.get_event_loop() # create event loop
    # loop.run_until_complete(main()) # main - это корутина
    loop.close () # когда закончит работу





''' New version of this'''
print ('**************************')
# Python 3.5 создает корутины с помощью синтаксиса async/await
# 3.6 - задачи создают с помощью create_task
# 3.7 - запускаем с помощью asyncio.run()

async def main_new():
    task1 = asyncio.create_task(print_nums())
    task2 = asyncio.create_task(print_time())
    await asyncio.gather(task1, task2)

asyncio.run(main_new())