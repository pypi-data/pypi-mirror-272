def root(number1):
    for i in range(int(number1)):
        if i * i > number1 and i * i * i > number1:
            break
        elif i * i == number1:
            root = i
            return i
        elif i * i > number1:
            return None
def cube_root(number1):
    for i in range(int(number1)):
        if i * i * i > number1 and i * i * i > number1:
            break
        elif i * i * i == number1:
            root = i
            return i
        elif i * i * i > number1:
            return None
def swap(x, y):
    x = x + y
    y = x - y
    x = x - y
    return x, y
