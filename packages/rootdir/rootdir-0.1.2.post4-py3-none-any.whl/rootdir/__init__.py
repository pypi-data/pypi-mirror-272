import os

class FailToFindRootException(Exception):
    pass


def rootdir():
    current_directory = os.path.dirname(__file__)

    while True:
        if os.path.exists(os.path.join(current_directory, '__root__.py')):
            return current_directory

        if current_directory == "/" or current_directory == os.path.dirname(current_directory):
            raise FailToFindRootException("There is no _root__.py, " + current_directory)

        current_directory = os.path.dirname(current_directory)
