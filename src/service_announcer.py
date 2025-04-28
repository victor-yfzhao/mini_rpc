import socket
import threading
import time

class ServiceAnnouncer:
    def __init__(self, service_name, service_port, broadcast_ip='255.255.255.255', broadcast_port=9999, interval=5):
        self.service_name = service_name
        self.service_port = service_port
        self.broadcast_ip = broadcast_ip
        self.broadcast_port = broadcast_port
        self.interval = interval
        self.running = False

    def _announce_loop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        message = f"SERVICE_ANNOUNCE:{self.service_name}:{self.service_port}".encode()

        while self.running:
            try:
                sock.sendto(message, (self.broadcast_ip, self.broadcast_port))
                print(f"[Announce] Sent: {message.decode()}")
                time.sleep(self.interval)
            except Exception as e:
                print(f"[Announce] Error: {e}")
                break

        sock.close()

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._announce_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()
