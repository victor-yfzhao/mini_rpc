import socket
import calculator_pb2

#计算器
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return {"error": "Division by zero"}
        return a / b


# 处理客户端请求
def handle_client_connection(client_socket):

    data = client_socket.recv(1024)


    request = calculator_pb2.CalcRequest()
    request.ParseFromString(data)

    method = request.method
    params = request.params

    calculator = Calculator()

    if method == "add":
        result = calculator.add(*params)
    elif method == "subtract":
        result = calculator.subtract(*params)
    elif method == "multiply":
        result = calculator.multiply(*params)
    elif method == "divide":
        result = calculator.divide(*params)
    else:
        result = {"error": "Unknown method"}


    response = calculator_pb2.CalcResponse()

    if isinstance(result, dict) and "error" in result:
        response.error = result["error"]
    else:
        response.result = result

    client_socket.send(response.SerializeToString())
    client_socket.close()



def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 50052))
    server.listen(5)
    print("Server started on port 50052...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr} has been established!")
        handle_client_connection(client_socket)


if __name__ == "__main__":
    start_server()
