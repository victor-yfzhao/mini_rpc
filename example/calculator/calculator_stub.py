from src.client_stub import MiniRpcStub
from example.calculator.messages import calculator_messages_pb2

class CalculatorStub(MiniRpcStub):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    def send_calculation_request(self, method, operand1, operand2):
        request = calculator_messages_pb2.CalculatorRequest()
        request.operand1 = operand1
        request.operand2 = operand2

        try:
            response = self.call(method, request)
            result = calculator_messages_pb2.CalculatorResponse()
            response.Unpack(result)
            return result.result
        except Exception as e:
            raise e

    def add(self, operand1, operand2):
        try:
            result = self.send_calculation_request("+", operand1, operand2)
            print(f"{operand1} + {operand2} = {result}")
        except Exception as e:
            print(e)

    def substract(self, operand1, operand2):
        try:
            result = self.send_calculation_request("-", operand1, operand2)
            print(f"{operand1} - {operand2} = {result}")
        except Exception as e:
            print(e)

    def multiply(self, operand1, operand2):
        try:
            result = self.send_calculation_request("*", operand1, operand2)
            print(f"{operand1} * {operand2} = {result}")
        except Exception as e:
            print(e)

    def divide(self, operand1, operand2):
        try:
            result = self.send_calculation_request("/", operand1, operand2)
            print(f"{operand1} / {operand2} = {result}")
        except Exception as e:
            print(e)
