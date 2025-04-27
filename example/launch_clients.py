from calculator import CalculatorClient


def launch_clients():
    client = CalculatorClient('127.0.0.1', 50000)

    client.test()


if __name__ == '__main__':
    launch_clients()