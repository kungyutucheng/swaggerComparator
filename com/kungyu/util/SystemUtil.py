# -*- coding: UTF-8 -*-
import sys
import getpass
import platform
import os
from com.kungyu.enums.OsType import OsType

reload(sys)
sys.setdefaultencoding('utf8')



class SystemUtil(object):

    @staticmethod
    def get_system_os_type():
        os_type = platform.platform().lower()
        if os_type.startswith('darwin'):
            return OsType.MAC
        elif os_type.startswith('linux') or os_type.startswith('unix'):
            return OsType.LINUX
        else:
            return OsType.WINDOWS

    @staticmethod
    def get_sys_user_path(parent_dir):
        user_name = getpass.getuser()
        if parent_dir is None:
            parent_dir = ''
        os_type = SystemUtil.get_system_os_type()
        if os_type == OsType.MAC:
            return os.sep + 'Users' + os.sep + user_name + os.sep + parent_dir + os.sep
        elif os_type == OsType.LINUX:
            return os.sep + 'usr' + os.sep + 'local' + os.sep + user_name + os.sep + parent_dir + os.sep
        elif os_type == OsType.WINDOWS:
            return 'C:' + os.sep + os.sep + 'Users' + os.sep + user_name + os.sep + parent_dir + os.sep
