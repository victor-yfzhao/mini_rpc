import socket
import struct
import threading
from abc import ABC, abstractmethod

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
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.socket_listener = socket.socket()
        self.socket_listener.bind((ip, port))

        self.methods = {}

        self.status = False

    def regiter_method(self, method_name, method):
        self.methods[method_name] = method

    @abstractmethod
    def call_method(self, method_name, args):
        raise NotImplementedError

    def handle_request(self, raw_request):
        request = template_message_pb2.MiniRpcRequest()
        request.ParseFromString(raw_request)
        print(request)

        method = request.method
        args = request.args

        response = template_message_pb2.MiniRpcResponse()

        try:
            result = self.call_method(method, args)
            response.status = 1
            response.info = "success"
            response.data.Pack(result)
        except Exception as e:
            response.status = -1
            response.info = str(e)
        finally:
            print(response)
            return response

    def _serve(self):
        self.socket_listener.listen()
        print(f"Server listening on {self.ip}:{self.port}")

        while self.status:
            try:
                conn, address = self.socket_listener.accept()
            except OSError:
                # Socket已经被关闭，退出循环
                break

            try:
                raw_msg_len = recv_all(conn, 4)
                if not raw_msg_len:
                    conn.close()
                    continue

                msg_len = struct.unpack(">I", raw_msg_len)[0]
                data = recv_all(conn, msg_len)
                if not data:
                    conn.close()
                    continue

                response = self.handle_request(data)

                send_msg(conn, response)
            except Exception as e:
                print(f"Error handling request: {e}")
            finally:
                conn.close()

        print("Server loop exited.")

    def start(self):
        if self.status:
            print("Server already started")
            return

        self.status = True
        self._server_thread = threading.Thread(target=self._serve, daemon=True)
        self._server_thread.start()
        print("Server started.")

    def stop(self):
        if not self.status:
            print("Server already stopped")
            return

        self.status = False
        self.socket_listener.close()
        if self._server_thread:
            self._server_thread.join()
        print("Server stopped.")
