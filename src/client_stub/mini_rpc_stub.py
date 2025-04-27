import struct
import socket
from abc import ABC, abstractmethod

from src.template import template_message_pb2


def recv_all(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            return None
        data += more
    return data


class MiniRpcStub(ABC):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send_and_receive(self, message_obj):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, self.port))

            data = message_obj.SerializeToString()
            msglen = struct.pack('>I', len(data))
            sock.sendall(msglen + data)

            length_bytes = recv_all(sock, 4)
            if not length_bytes:
                raise ConnectionError("Failed to receive length prefix")

            message_length = struct.unpack('>I', length_bytes)[0]
            data = recv_all(sock, message_length)
            if not data:
                raise ConnectionError("Failed to receive full response")

            response = template_message_pb2.MiniRpcResponse()
            response.ParseFromString(data)
            return response

    def call(self, method, args):
        request = template_message_pb2.MiniRpcRequest()
        request.method = method
        request.args.Pack(args)

        response = self.send_and_receive(request)
        if response.status == -1:
            raise Exception(response.info)
        return response.data
