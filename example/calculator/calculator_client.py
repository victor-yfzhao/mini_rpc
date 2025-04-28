from example.calculator.calculator_stub import CalculatorStub
from src.service_discovery import ServiceDiscovery
import time

class CalculatorClient:
    def __init__(self, service_name, service_port=9999):
        self.service_name = service_name
        self.discovery = ServiceDiscovery(listen_port=service_port)
        self.discovery.start()

        ip, port = self.find_service(service_name)
        self.calculatorStub = CalculatorStub(ip, port)

    def find_service(self, service_name):
        timeout = 5
        start_time = time.time()
        while time.time() - start_time < timeout:
            services = self.discovery.get_services()
            for ip, svc_name, svc_port in services:
                if svc_name == service_name:
                    print(f"[Client] Found service {svc_name} at {ip}:{svc_port}")
                    return ip, svc_port
            time.sleep(1)
        raise Exception(f"Service '{service_name}' not found.")

    def test(self):
        self.calculatorStub.add(1, 2)
        self.calculatorStub.substract(3, 4)
        self.calculatorStub.multiply(5, 6)
        self.calculatorStub.divide(15, 5)

        self.calculatorStub.divide(15, 0)

