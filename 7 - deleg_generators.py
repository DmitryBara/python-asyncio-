from inspect import getgeneratorstate

# Helper decorator инициализирует генератор значением None
def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner

# custom Exception
class BlaBlaException(Exception):
    pass


# Подгенератор (читающий из строки)
@coroutine
def subgen():
    while True:
        try:
            message = yield # принимаем данные из делегатора и записываем влево (message)
        except BlaBlaException:
            print('Исключение обработано!')
        else:
            print('.....', message)


# Делегирующий (транслятор другого генератора)
@coroutine
def delegator(subg):
    while True:
        try:
            data = yield # Принимаем данные снаружи, кладем их в дату, отдаем в подгенератор
            subg.send(data)
        except BlaBlaException as e: # перехватываем исключение и бросаем его дальше
            subg.throw(e)



sg = subgen()
g = delegator(sg)

g.send('Hello')
g.send('World')
g.send('12345')

g.throw(BlaBlaException)



### Другой способ
# yield from - содержит в себе инициализацию подгенератора
print('################################')

# without @coroutine
def subgen():
    while True:
        try:
            message = yield # принимаем данные из делегатора и записываем влево (message)
        except StopIteration:
            print('Исключение обработано!')
            break
        else:
            print('.....', message)
    return 'Returned from subgen() Whoooah!'

@coroutine
def delegator(subg):
    # Эквивалентный код
    # while True:
    #     try:
    #         data = yield # Принимаем данные снаружи, кладем их в дату, отдаем в подгенератор
    #         subg.send(data)
    #     except BlaBlaException as e: # перехватываем исключение и бросаем его дальше
    #         subg.throw(e)
    result = yield from subg  # сохраняем результат return
    print(result)

sg = subgen()
g = delegator(sg)

g.send('1')
g.send('2')
g.send('3')

try:
    g.throw(StopIteration)
except:
    StopIteration

### Простой пример yield from
def a():
    yield from 'xyzabc'

simple = a()
print( next(simple) )
print( next(simple) )
print( next(simple) )
print( next(simple) )
