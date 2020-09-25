from inspect import getgeneratorstate


# Пример 1
def subgen():
    x = 'Ready to accept message'
    message = yield x
    print('Subgen received: ', message)

# Объект генератора
g = subgen()

# Узнаем состояние генератора
print(getgeneratorstate(g))

# Инициализируем генератор
print(g.send(None))    # вернет значение переменной x

# Узнаем состояние генератора
print(getgeneratorstate(g))



##########
print('....................')
##########


# Helper decorator инициализирует генератор значением None
def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner

#Пример 2
@coroutine
def average():
    count = 0
    sum =0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done')
            break # exit from while
        else:
            count += 1
            sum += x
            average = round(sum/count, 2)

    return average


g = average()
# res = g.send(None) # None
res = g.send(5) # 5
res = g.send(10) # 7.5
res = g.send(35) # 16.67
print(res)

# Забрасываем исключение
try:
    g.throw(StopIteration)
except StopIteration as e:
    print('Average in finish: ', e.value)