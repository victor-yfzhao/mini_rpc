import time

from example.calculator.calculator_stub import CalculatorStub
#

class CalculatorClient:
    def __init__(self, service_name, listen_port=9999):
        self.calculatorStub = CalculatorStub(service_name, listen_port)

    def test(self):
        self.calculatorStub.add(1, 2)
        self.calculatorStub.substract(3, 4)
        self.calculatorStub.multiply(5, 6)
        self.calculatorStub.divide(15, 5)
        self.calculatorStub.divide(15, 0)


