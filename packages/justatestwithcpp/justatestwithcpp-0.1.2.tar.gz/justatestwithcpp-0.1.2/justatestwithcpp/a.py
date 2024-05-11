import cppimport as cpp

somecode = cpp.imp('somecode') #automatically compiles code

def sq(x):
    return somecode.square(x)
