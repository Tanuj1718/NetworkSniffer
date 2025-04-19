import json
import logging
import socketio
from scapy.all import sniff, DNSQR, TCP, Raw, ARP, IP
from scapy.layers.l2 import Ether
from scapy.layers.tls.handshake import TLSClientHello
from plyer import notification
import socket

sio = socketio.Client()

@sio.event
def connect():
    print("[SocketIO] Connected to Flask backend ✅")

@sio.event
def connect_error(data):
    print("[SocketIO] Connection failed ❌", data)

@sio.event
def disconnect():
    print("[SocketIO] Disconnected 🚫")

sio.connect("http://localhost:5050")

# Logging
logging.basicConfig(filename="filtered.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# 🔔 Notification
def notify(title, msg):
    notification.notify(title=title, message=msg, timeout=10)

# 🌐 Try hostname lookup
def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None

# 🎯 Main packet handler
def process_packet(packet):
    domain = None
    ip = None
    mac = None
    hostname = None

    # DNS packet
    if packet.haslayer(DNSQR):
        domain = packet[DNSQR].qname.decode(errors='ignore')
        ip = packet[IP].src if packet.haslayer("IP") else None
        mac = packet.src

    # HTTP Host header
    elif packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load
        if b"Host:" in payload:
            lines = payload.split(b"\r\n")
            for line in lines:
                if b"Host: " in line:
                    domain = line.split(b"Host: ")[1].decode(errors='ignore')
                    break
        ip = packet[IP].src if packet.haslayer("IP") else None
        mac = packet.src

    # TLS SNI
    elif packet.haslayer(TLSClientHello):
        try:
            domain = packet[TLSClientHello].extensions[0].servernames[0].servername
        except:
            pass
        ip = packet[IP].src if packet.haslayer("IP") else None
        mac = packet.src

    if domain and ip:
        hostname = get_hostname(ip)

        # 📤 Emit domain + device info
        print(f"[DEBUG] {ip} ({hostname or 'Unknown'}) visited {domain}")
        logging.info(f"[Detected] {ip} {domain}")
        notify("Detected Domain", domain)
        sio.emit("domain_detected", {
            "domain": domain,
            "device_ip": ip,
            "device_mac": mac,
            "device_name": hostname or "Encrypted"
        })

if __name__ == "__main__":
    print("[*] Sniffer started... Listening for traffic.")
    sniff(prn=process_packet, store=False)
