import cppimport as cpp

somecode = cpp.imp('somecode') #automatically compiles code

b = 22


def sq(x):
    return somecode.square(x)


def myFunc(x, y):
    return x+y