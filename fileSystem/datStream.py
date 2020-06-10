import pickle
import os
import socket


class datStream:
    def dump(self, dire, serv_ip, port):
        s=socket.socket()
        s.connect((serv_ip, port))
        s.send(pickle.dumps(dire))
        s.close()

