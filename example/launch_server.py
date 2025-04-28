import time
from example.calculator.calculator_server import CalculatorServer

def launch_server():

    server = CalculatorServer(host="0.0.0.0", port=50000, service_name="calculator-service")
    server.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping server...")
        server.stop()

if __name__ == "__main__":
    launch_server()