import struct
import socket
import time
from abc import ABC, abstractmethod
from src.service_discovery import ServiceDiscovery
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
    def __init__(self, service_name, listen_port):
        self.service_name = service_name
        self.timeout = 10
        self.discovery = ServiceDiscovery(listen_port)
        self.discovery.start()

        self.ip = "-1.-1.-1.-1"
        self.port = -1
        try:
            self.ip, self.port = self.find_service()
        except Exception as e:
            print(e)

    def find_service(self):
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            services = self.discovery.get_services()
            for ip, svc_name, svc_port in services:
                if svc_name == self.service_name:
                    print(f"[Info][Stub] Found service {svc_name} at {ip}:{svc_port}")
                    return ip, svc_port
            time.sleep(1)
        raise Exception(f"[Error][Stub] Service '{self.service_name}' not found.")

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
        if self.ip == "-1.-1.-1.-1":
            print(f"[Error][Stub] Service {self.service_name} not found, trying to connect...")
            self.ip, self.port = self.find_service()
            if self.ip == "-1.-1.-1.-1":
                raise Exception(f"[Error][Stub] Failed to call {method}: Illegal ip address")
        request = template_message_pb2.MiniRpcRequest()
        request.method = method
        request.args.Pack(args)

        response = self.send_and_receive(request)
        if response.status == -1:
            raise Exception(response.info)
        return response.data
