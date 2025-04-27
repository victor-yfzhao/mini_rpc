class CalculatorStub:
    def __init__(self, host='localhost', port=5000):
        import socket
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def add(self, a, b):
        request = f'METHOD:add;PARAM1:{a};PARAM2:{b}'
        self.sock.sendall(request.encode())
        response = self.sock.recv(1024).decode()
        return self._parse_response(response)

    def subtract(self, a, b):
        request = f'METHOD:subtract;PARAM1:{a};PARAM2:{b}'
        self.sock.sendall(request.encode())
        response = self.sock.recv(1024).decode()
        return self._parse_response(response)

    def _parse_response(self, response):
        if response.startswith("RESULT:"):
            return int(response.split(":")[1])
        elif response.startswith("ERROR:"):
            raise Exception(response.split(":")[1])
        else:
            raise Exception("Invalid response format")

    def close(self):
        self.sock.close()