from example.calculator.calculator_client import CalculatorClient

def launch_clients():
    client = CalculatorClient('calculator-service')

    client.test()

if __name__ == '__main__':
    launch_clients()
