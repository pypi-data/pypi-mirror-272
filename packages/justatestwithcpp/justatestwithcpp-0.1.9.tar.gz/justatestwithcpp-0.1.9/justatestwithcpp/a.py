import cppimport as cpp
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the absolute path to the C++ source file
cpp_file_path = os.path.join(current_dir, 'somecode.cpp')
# Importing the somecode object from the specified C++ file
somecode = cpp.imp(cpp_file_path, relative=False)

b = 22


def sq(x):
    return somecode.square(x)


def myFunc(x, y):
    return x+y