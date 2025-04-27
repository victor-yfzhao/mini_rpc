import json
import socket
from src.client_stub.calculator_stub import CalculatorStub

class Client:
    def __init__(self, host='localhost', port=5000):
        self.stub = CalculatorStub(host, port)

    def run(self):
        while True:
            operation = input("Enter operation (add/subtract) or 'exit' to quit: ")
            if operation == 'exit':
                break
            try:
                a = int(input("Enter first number: "))
                b = int(input("Enter second number: "))
                if operation == 'add':
                    result = self.stub.add(a, b)
                elif operation == 'subtract':
                    result = self.stub.subtract(a, b)
                else:
                    print("Invalid operation. Please try again.")
                    continue
                print(f"Result: {result}")
            except ValueError:
                print("Invalid input. Please enter integers.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    client = Client()
    client.run()