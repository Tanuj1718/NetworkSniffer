# network_sniffer.py
from scapy.all import sniff, DNSQR, TCP, Raw, IP  # type: ignore
from scapy.layers.tls.handshake import TLSClientHello # type: ignore
import logging
from datetime import datetime

# Logging to file
logging.basicConfig(filename="visited_websites.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_to_file(info):
    logging.info(info)
    print(info)

def process_packet(packet):
    # --- DNS Detection ---
    if packet.haslayer(DNSQR):
        domain = packet[DNSQR].qname.decode(errors='ignore')
        log_to_file(f"[DNS] Queried Domain: {domain}")

    # --- HTTP Detection ---
    elif packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load

        try:
            if b"HTTP" in payload and b"Host:" in payload:
                lines = payload.split(b"\r\n")
                for line in lines:
                    if b"Host:" in line:
                        host = line.split(b"Host: ")[1].decode(errors='ignore')
                        log_to_file(f"[HTTP] Host: {host}")
                        break
        except Exception as e:
            print(f"[Error decoding HTTP] {e}")

    # --- HTTPS Detection via TLS SNI ---
    elif packet.haslayer(TLSClientHello):
        try:
            sni = packet[TLSClientHello].extensions[0].servernames[0].servername
            log_to_file(f"[HTTPS] TLS SNI: {sni}")
        except Exception as e:
            print(f"[Error decoding TLS] {e}")

if __name__ == "__main__":
    print("[*] Starting packet capture... Press Ctrl+C to stop.")
    sniff(prn=process_packet, store=False)
