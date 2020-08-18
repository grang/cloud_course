# coding=utf-8
import os
import socket
import threading
import time

def get_machine_no():
    return 0



class IdGenerator(object):
    _inc = 0
    _inc_lock = threading.Lock()
    _machine_no = get_machine_no()

    @staticmethod
    def gen():
        new_id = (int(time.time()) & 0xffffffff) << 32
        new_id |= (IdGenerator._machine_no & 0xff) << 24
        new_id |= (os.getpid() & 0xff) << 16
        IdGenerator._inc_lock.acquire()
        new_id |= IdGenerator._inc
        IdGenerator._inc = (IdGenerator._inc + 1) & 0xffff
        IdGenerator._inc_lock.release()

        return str(new_id)


def gen_db_id():
    return IdGenerator.gen()  

if __name__ == '__main__':
    for i in range(0, 10):
        print(IdGenerator.gen())
        
        