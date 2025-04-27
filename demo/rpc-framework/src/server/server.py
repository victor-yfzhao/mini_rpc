import socket
import json
from calculator_service import CalculatorService

class RPCServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.calculator_service = CalculatorService()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print(f'Server listening on {self.host}:{self.port}')

        while True:
            client_socket, addr = server_socket.accept()
            print(f'Connection from {addr}')
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        request_data = client_socket.recv(1024).decode()
        print(f'Received request: {request_data}')
        
        response_data = self.process_request(request_data)
        client_socket.send(response_data.encode())
        client_socket.close()

    def process_request(self, request_data):
        try:
            request = json.loads(request_data)
            method = request.get('method')
            params = request.get('params', [])

            if method == 'add':
                result = self.calculator_service.add(*params)
            elif method == 'subtract':
                result = self.calculator_service.subtract(*params)
            else:
                return json.dumps({"error": "Method not found"})

            return json.dumps({"result": result})
        except Exception as e:
            return json.dumps({"error": str(e)})

if __name__ == '__main__':
    server = RPCServer()
    server.start()