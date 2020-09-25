from time import time

def gen_filename():
    while True:
        pattern = 'file-{}.jpeg'
        t = int(time()*1000)
        yield pattern.format(str(t))
        print('Code block After Yield')

g = gen_filename()
print( next(g) )
print( next(g) )
print( next(g) )


'''Событийный цикл Round Robin'''
def gen1(s):
    for i in s:
        yield i

def gen2(n):
    for i in range(n):
        yield i

g1 = gen1('abcd')
g2 = gen2(4)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)

    try:
        _ = next(task)
        print(_)
        tasks.append(task)
    except StopIteration:
        pass
