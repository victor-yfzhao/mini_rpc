import socket
import calculator_pb2


def send_request(method, params):
    # 创建请求对象
    request = calculator_pb2.CalcRequest()
    request.method = method
    request.params.extend(params)

    # 创建套接字连接到服务器
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 50052))


    client.send(request.SerializeToString())


    response_data = client.recv(1024)
    client.close()


    response = calculator_pb2.CalcResponse()
    response.ParseFromString(response_data)

    if response.error:
        return {"error": response.error}
    return {"result": response.result}


def test_rpc():
    result = send_request("add", [5, 3])
    print(f"Add result: {result}")

    result = send_request("subtract", [10, 4])
    print(f"Subtract result: {result}")

    result = send_request("multiply", [6, 7])
    print(f"Multiply result: {result}")

    result = send_request("divide", [10, 2])
    print(f"Divide result: {result}")

    result = send_request("divide", [10, 0])
    print(f"Divide error: {result.get('error')}")

if __name__ == "__main__":
    test_rpc()
