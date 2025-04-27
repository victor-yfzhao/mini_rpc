from example.calculator.calculator_stub import CalculatorStub


class CalculatorClient:
    def __init__(self):
        self.calculatorStub = CalculatorStub()


    def service(self):
        response = None
        request = self.calculatorStub.service()

