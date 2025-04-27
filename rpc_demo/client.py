import socket
import calculator_pb2

def send_request(method, params):
    request = calculator_pb2.CalcRequest()
    request.method = method
    request.params.extend(params)

    data = request.SerializeToString()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 50051))

    client.send(len(data).to_bytes(4, byteorder='big'))
    client.send(data)

    length_bytes = client.recv(4)
    if not length_bytes:
        return None
    message_length = int.from_bytes(length_bytes, byteorder='big')
    response_data = client.recv(message_length)

    response = calculator_pb2.CalcResponse()
    response.ParseFromString(response_data)

    client.close()

    return response

def test_rpc():
    methods = [
        ("add", [5, 3]),
        ("subtract", [10, 4]),
        ("multiply", [6, 7]),
        ("divide", [20, 5]),
        ("divide", [10, 0])
    ]

    for method, params in methods:
        resp = send_request(method, params)
        if resp.error:
            print(f"{method} Error: {resp.error}")
        else:
            print(f"{method} Result: {resp.result}")

if __name__ == "__main__":
    test_rpc()
