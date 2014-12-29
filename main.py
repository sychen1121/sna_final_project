import common_function as common
from sys import argv

if __name__ == '__main__':
    file_path = argv[1]
    checkin_info = common.create_checkin_info(file_path)

