#-*- coding: UTF-8 -*-
import sys
import getopt
from diff.v2.Diff import Diff
from util.FileLoader import FileLoader


class SwaggerComparator(object):
    def __init__(self):
        pass


if __name__ == '__main__':

    # 第一个参数为脚本名称
    argvs = sys.argv[1:]
    if len(argvs) == 0:
        print('error command')
        exit(2)
    command = argvs[0]

    help_doc_path = '../../resources/doc/'

    if command == '--help':
        print FileLoader.load_file(help_doc_path + 'help.txt')
        exit(0)
    elif command == 'diff':
        argvs = argvs[1:]
        try:
            opts, args = getopt.getopt(argvs, "hn:o:")
        except getopt.GetoptError:
            print FileLoader.load_file(help_doc_path + 'help-diff.txt')
            exit(2)

        new_url = None
        orig_url = None
        directory = None
        file_name = None
        for opt, arg in opts:
            if opt == '-h':
                print FileLoader.load_file(help_doc_path + 'help-diff.txt')
                exit(0)
            elif opt == '-n':
                new_url = arg
            elif opt == '-o':
                orig_url = arg
            elif opt == '-d':
                directory = arg
            elif opt == '-f':
                file_name = arg
            diff = Diff(new_url, orig_url, directory, file_name)

        if new_url is None or orig_url is None:
            print FileLoader.load_file(help_doc_path + 'help-diff.txt')
            exit(0)
        diff = Diff(new_url, orig_url)
        diff.execute()
    else:
        print FileLoader.load_file(help_doc_path + 'help.txt')
        exit(0)




