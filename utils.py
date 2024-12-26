import random, time


def rand(n1, n2):
    return random.randint(n1,n2)


def sleep(n1, n2=0):
    if (n2 == 0) or (n1 > n2):
        time.sleep(n1)
    else:
        time.sleep(rand(n1,n2))

