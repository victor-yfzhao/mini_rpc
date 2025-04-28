import socket
import threading
import time

class ServiceDiscovery:
    def __init__(self, listen_port=9999, timeout=15):
        self.listen_port = listen_port
        self.timeout = timeout
        self.services = {}  # { (ip, service_name): last_seen_time }
        self.running = False

    def _listen_loop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.listen_port))

        sock.settimeout(1)

        while self.running:
            try:
                data, addr = sock.recvfrom(1024)
                message = data.decode()
                if message.startswith("SERVICE_ANNOUNCE:"):
                    _, service_name, service_port = message.strip().split(":")
                    key = (addr[0], service_name)
                    self.services[key] = (int(service_port), time.time())
                    print(f"[Discovery] Found service: {key} on port {service_port}")
            except socket.timeout:
                pass
            except Exception as e:
                print(f"[Discovery] Error: {e}")
                break

            self._remove_expired_services()

        sock.close()

    def _remove_expired_services(self):
        now = time.time()
        expired = [key for key, (_, last_seen) in self.services.items() if now - last_seen > self.timeout]
        for key in expired:
            print(f"[Discovery] Service {key} expired")
            del self.services[key]

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()

    def get_services(self):
        return [(ip, service_name, port) for (ip, service_name), (port, _) in self.services.items()]
