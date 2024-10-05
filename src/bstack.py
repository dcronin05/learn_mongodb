from lib import *


def retrieve(id_num):
    result = api.get_pages_read({"id": id_num})
    print(result)

def insert(id_num, name, text):
    pass