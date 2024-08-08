import socket
import sys
import threading
from datetime import datetime

common_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    88: "Kerberos",
    137: "NetBIOS",
    139: "SMB",
    143: "IMAP",
    161: "SNMP",
    162: "SNMP",
    194: "IRC",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB"
}

if len(sys.argv) < 2:
    print(f"Usage: PortScanner.py <host/IP>")
    sys.exit(1)

host = sys.argv[1]

try:
    hostIP = socket.gethostbyname(host)
except socket.gaierror:
    print(f"Hostname could not be resolved: {host}")
    sys.exit(1)

socket.setdefaulttimeout(0.1)

print("-" * 35)
print(f"| Scanning host at {hostIP}  |")
print("-" * 35)

t1 = datetime.now()

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((hostIP, port))
        if result == 0:
            if port in common_ports:
                print(f"Port {port}({common_ports[port]}): Open")
            else:
                print(f"Port {port}: Open")
        s.close()

    except socket.error as e:
        print(f"Socket error: {e}")

threads = []

try:
    for port in range(1, 65536):
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    t2 = datetime.now()
    total_time = t2 - t1

    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()
    print("-"*36)
    print(f"| Scan Completed in {total_time} |")
    print("-"*36)

except KeyboardInterrupt:
    sys.exit(1)

except socket.error as e:
    print(f"Socket error: {e}")
    sys.exit(1)
