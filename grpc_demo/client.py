import grpc
import calculator_pb2
import calculator_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = calculator_pb2_grpc.CalculatorStub(channel)

    response = stub.Add(calculator_pb2.CalcRequest(a=5, b=3))
    print("Add result:", response.result)

    response = stub.Subtract(calculator_pb2.CalcRequest(a=10, b=4))
    print("Subtract result:", response.result)

if __name__ == '__main__':
    run()
