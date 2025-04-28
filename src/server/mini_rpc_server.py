import socket
import struct
import threading
from abc import ABC, abstractmethod
from src.service_announcer import ServiceAnnouncer
from src.template import template_message_pb2


def recv_all(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def send_msg(sock, message_obj):
    data = message_obj.SerializeToString()
    msglen = struct.pack('>I', len(data))
    sock.sendall(msglen + data)


class MiniRpcServer(ABC):
    def __init__(self, ip, port, service_name=None):
        self.ip = ip
        self.port = port

        self.socket_listener = socket.socket()
        self.socket_listener.bind((ip, port))

        self.methods = {}

        self.status = False

        if service_name:
            self.announcer = ServiceAnnouncer(service_name=service_name, service_port=port, broadcast_port=9999)
        else:
            self.announcer = None
    def regiter_method(self, method_name, method):
        self.methods[method_name] = method

    @abstractmethod
    def call_method(self, method_name, args):
        raise NotImplementedError

    def handle_request(self, conn, addr):
        print(f"[Info][Server] Starting new thread to haddle request from {addr}")
        response = template_message_pb2.MiniRpcResponse()

        try:
            raw_msg_len = recv_all(conn, 4)
            if not raw_msg_len:
                raise Exception(f"Unknown request from {addr}: Invalid length")

            msg_len = struct.unpack(">I", raw_msg_len)[0]
            data = recv_all(conn, msg_len)
            if not data:
                raise Exception(f"Unknown request from {addr}: Invalid data")

            request = template_message_pb2.MiniRpcRequest()
            request.ParseFromString(data)

            method = request.method
            args = request.args

            result = self.call_method(method, args)

            response.status = 1
            response.info = "success"
            response.data.Pack(result)
        except Exception as e:
            response.status = -1
            response.info = str(e)
        finally:
            send_msg(conn, response)
            conn.close()


    def _serve(self):
        self.socket_listener.listen()
        print(f"Server listening on {self.ip}:{self.port}")

        while self.status:
            try:
                conn, addr = self.socket_listener.accept()
                client_thread = threading.Thread(target=self.handle_request, args=(conn, addr))
                client_thread.start()
            except Exception as e:
                print(f"[Error][Server] {e}")

        print("Server loop exited.")

    def start(self):
        if self.status:
            print("Server already started")
            return

        self.status = True
        self._server_thread = threading.Thread(target=self._serve, daemon=True)
        self._server_thread.start()
        if self.announcer:
            self.announcer.start()
            print(f"[{self.service_name}] Announcer started.")
        print("[Info][Server] Server started.")

    def stop(self):
        if not self.status:
            print("[Info][Server] Server already stopped")
            return

        self.status = False
        self.socket_listener.close()
        if self._server_thread:
            self._server_thread.join()
        if self.announcer:
            self.announcer.stop()
            print(f"[{self.service_name}] Announcer stopped.")
        print("[Info][Server] Server stopped.")
