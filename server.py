# creating a server for Peers to connect

import os
import threading
import pickle
import socket
import time


CONN_TEST_TIME = 1

#Check if connection closed
def is_socket_closed(sock: socket.socket) -> bool:
    
    try:
        try:
            obj = pickle.dumps('testing conn')
            sock.send(obj)
        except socket.error:
            return True
        return False

    except BlockingIOError:
        return False  
    except ConnectionResetError:
        return True  
    except Exception as e:
        return True
    return False


class Server:

    s: socket.socket
    connections: dict[(str, int), (socket.socket, (str, int))]
    accept_thread: threading.Thread
    broadcast_peers_thread: threading.Thread
    recv_msg_thread: threading.Thread

    server_ip = ''
    port = 1233
    connections = dict()

    def __init__(self):
        self.s = socket.socket()
        self.s.bind((self.server_ip, self.port))
        self.s.listen(10)
        print("Server is up and running")

    def __del__(self):
        self.s.close()

    #Acept connection and add ot list
    def accept_connections(self):
        
        while True:
            c, addr = self.s.accept()


            c.send(b'Send port')
            c.settimeout(2)
            peer_addr = pickle.loads(c.recv(512))
            self.connections[addr] = (c, peer_addr)
            print(f"Got connection from {addr, peer_addr}")
            self.recv_msg_thread = threading.Thread(target=self.recv_msg, args=(c, addr))
            self.recv_msg_thread.start()
            self.start_broadcast_peers_thread()

    #Reveive message from peer
    def recv_msg(self, c: socket.socket, addr: (str, int)):
        
        while True:
            c.settimeout(10000)
            try:
                msg = c.recv(512).decode()
                if msg == 'close':
                    print(addr)
                    self.connections.pop(addr)
                    self.start_broadcast_peers_thread()
                    break

                if msg == 'get_peers':
                    conn = pickle.dumps({
                        "type": "peers",
                        "peers": [x[1] for a, x in self.connections.items()]
                    })
                    c.send(conn)

            except Exception as e:
                print(f"got exception {e} while receiving from addr {addr}")
                break

    def periodic_conn_test(self):
        while True:
            closed_connections = []  # stores the keys for closed connections
            for addr, c in self.connections.items():
                if is_socket_closed(c[0]):
                    closed_connections.append(addr)

            n_closed = len(closed_connections)
            for addr in closed_connections:
                self.connections.pop(addr)

            if n_closed > 0:
                self.start_broadcast_peers_thread()

            time.sleep(CONN_TEST_TIME)

    def start_broadcast_peers_thread(self):
        
        self.broadcast_peers_thread = threading.Thread(target=self.broadcast_peers)
        self.broadcast_peers_thread.start()

    #Send detials from peer to other peers
    def broadcast_peers(self):
        
        conn = pickle.dumps({
            "type": "peers",
            "peers": [ x[1] for a, x in self.connections.items() ]
        })
        for addr in self.connections:
            self.connections[addr][0].send(conn)

    #Start the server
    def run(self):
    
        self.accept_thread = threading.Thread(target=self.accept_connections)
        self.accept_thread.start()
        self.periodic_conn_test_thread = threading.Thread(target=self.periodic_conn_test)
        self.periodic_conn_test_thread.start()


if __name__ == "__main__":
    try:
        server = Server()
        server.run()
        inp = input()
        if inp == 'c' or inp == 'close':
            os._exit(0)

    except KeyboardInterrupt:
        os._exit(0)
