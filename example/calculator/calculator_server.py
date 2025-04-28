# from Tools.i18n.makelocalealias import parse_glibc_supported
from src.service_announcer import ServiceAnnouncer
from src import MiniRpcServer
from example.calculator.messages import calculator_messages_pb2

class CalculatorServer(MiniRpcServer):
    def __init__(self, host, port, service_name="calculator-service"):
        # 初始化父类
        super().__init__(host, port, service_name=service_name)

        self.regiter_method("+", self.add)
        self.regiter_method("-", self.substract)
        self.regiter_method("*", self.multiply)
        self.regiter_method("/", self.divide)
        self.service_name = service_name
    def start(self):
        super().start()
        print("[CalculatorServer] Server started.")

    def stop(self):
        super().stop()
        print("[CalculatorServer] Server stopped.")

    def call_method(self, method_name, args):
        method = self.methods.get(method_name)
        if not method:
            raise NotImplementedError(f"Method {method_name} not found")

        request = calculator_messages_pb2.CalculatorRequest()
        try:
            args.Unpack(request)
        except Exception as e:
            print(e)
            raise e

        operand1 = request.operand1
        operand2 = request.operand2

        if operand1 is None or operand2 is None:
            raise NotImplementedError(f"Operand {operand1} or {operand2} not found")

        result = method(operand1, operand2)

        response = calculator_messages_pb2.CalculatorResponse()
        response.result = result
        return response

    def add(self, operand1, operand2):
        return operand1 + operand2

    def substract(self, operand1, operand2):
        return operand1 - operand2

    def multiply(self, operand1, operand2):
        return operand1 * operand2

    def divide(self, operand1, operand2):
        if operand2 == 0:
            raise ZeroDivisionError("Division by zero")

        return operand1 / operand2

