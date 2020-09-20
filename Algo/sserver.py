import socket
import server_run
import datetime
import time
import MetaTrader5 as mt5

class socketserver:
    def __init__(self, address = '', port = 7000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.sock.bind((self.address, self.port))
        self.cummdata = ''
        
    def recvmsg(self):
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()
        print('connected to', self.addr)
        self.cummdata = ''

        while True:
            data = self.conn.recv(10000)
            self.cummdata+=data.decode("utf-8")
            if not data:
                break 
            self.conn.send(bytes(cal(), "utf-8"))
            #print(self.cummdata)
            
    def __del__(self):
        self.sock.close()
        
def cal():
    cday = datetime.date.today()
    r = server_run.execute_logic(mt5.TIMEFRAME_H1, cday)

    return str(r)
    
def main_socket():
    serv = socketserver('127.0.0.1', 7000)
    while True:  
        msg = serv.recvmsg()









'''
def stop_socket_connection():
    print("socket connection stopped !!!")


def run_socket():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind(('127.0.0.1', 7000))
    serv.listen(1)

    while True:
        conn, addr = serv.accept()
        print('client connected to :', addr)
        conn.close()


run_socket()
'''