import os

def open_file(path):
    path = os.path.realpath(path)
    return open(path)
