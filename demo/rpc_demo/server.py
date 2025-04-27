import socket
import calculator_pb2

def handle_request(data):
    request = calculator_pb2.CalcRequest()
    request.ParseFromString(data)

    response = calculator_pb2.CalcResponse()

    try:
        if request.method == "add":
            response.result = sum(request.params)
        elif request.method == "subtract":
            response.result = request.params[0] - request.params[1]
        elif request.method == "multiply":
            result = 1
            for num in request.params:
                result *= num
            response.result = result
        elif request.method == "divide":
            if request.params[1] == 0:
                response.error = "Division by zero!"
            else:
                response.result = request.params[0] // request.params[1]
        else:
            response.error = "Unknown method."
    except Exception as e:
        response.error = str(e)

    return response.SerializeToString()

def start_server(host="127.0.0.1", port=50051):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server started at {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")


        length_bytes = client_socket.recv(4)
        if not length_bytes:
            continue
        message_length = int.from_bytes(length_bytes, byteorder='big')

        data = client_socket.recv(message_length)
        if not data:
            continue

        response_data = handle_request(data)


        client_socket.send(len(response_data).to_bytes(4, byteorder='big'))
        client_socket.send(response_data)

        client_socket.close()

if __name__ == "__main__":
    start_server()
