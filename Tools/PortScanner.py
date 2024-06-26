import socket
import sys

common_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    88: "Kerberos",
    135: "RPC",
    137: "NetBIOS",
    139: "SMB",
    143: "IMAP",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB"
}

if len(sys.argv) < 2:
    print(f"Usage: PortScanner.py <host/IP>")
    sys.exit(1)

host = sys.argv[1]
scan_type = sys.argv[2]

if sys.argv[2] == "-quick":
    port_limit = 1000
elif sys.argv[2] == "-full":
    port_limit = 65535

try:
    hostIP = socket.gethostbyname(host)
except socket.gaierror:
    print(f"Hostname could not be resolved: {host}")
    sys.exit(1)

socket.setdefaulttimeout(0.1)

print("-" * 60)
print(f"Scanning host at {hostIP}")
print("-" * 60)

try:
    for port in range(1, port_limit):
        sys.stdout.write(f"\rScanning port {port}/{port_limit}")
        sys.stdout.flush()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((hostIP, port))
        if result == 0:
            if port in common_ports:
                print(f"\r{' ' * 60}\rPort {port}({common_ports[port]}): Open")
            else:
                print(f"\r{' ' * 60}\rPort {port}: Open")
        s.close()

    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()
    print("\nScan Completed")

except KeyboardInterrupt:
    sys.exit(1)

except socket.error as e:
    print(f"Socket error: {e}")
    sys.exit(1)
