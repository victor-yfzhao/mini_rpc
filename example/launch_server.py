import time

from calculator import CalculatorServer

def launch_server():
    server = CalculatorServer("127.0.0.1", 50000)
    server.start()

    time.sleep(10)
    server.stop()


if __name__ == "__main__":
    launch_server()