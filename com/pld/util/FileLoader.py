import os


class FileLoader(object):

    @staticmethod
    def load_file(path):
        if not os.path.isfile(path):
            raise Exception(path + ' is not exist')
        file = open(path, 'r')
        return file.read()
