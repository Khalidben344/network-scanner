import socket
import subprocess
import platform
import threading
import ipaddress

# Ping function
def ping_host(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    result = subprocess.run(command, stdout=subprocess.DEVNULL)
    return result.returncode == 0

# Port scanner function
def scan_ports(host, start_port, end_port):
    open_ports = []
    print(f"\n🔍 Scanning ports {start_port} to {end_port} on {host}...")
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"✅ Port {port} is open")
            open_ports.append(port)
        sock.close()
    if not open_ports:
        print("❌ No open ports found.")
    else:
        print(f"\nOpen ports on {host}: {open_ports}")

# Scan a single host (ping + port scan)
def scan_host(host, start_port=1, end_port=1024):
    print(f"\n🌐 Scanning host: {host}")
    alive = ping_host(host)
    if alive:
        print(f"✅ Host {host} is alive.")
        scan_ports(host, start_port, end_port)
    else:
        print(f"❌ Host {host} is not reachable.")

# Scan a subnet (ping sweep)
def scan_subnet(subnet):
    print(f"\n🌍 Scanning subnet: {subnet}")
    try:
        net = ipaddress.ip_network(subnet, strict=False)
    except ValueError:
        print("❌ Invalid subnet.")
        return

    alive_hosts = []

    def ping_and_record(ip):
        if ping_host(str(ip)):
            print(f"✅ Host {ip} is alive.")
            alive_hosts.append(str(ip))

    threads = []
    for ip in net.hosts():
        t = threading.Thread(target=ping_and_record, args=(ip,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if not alive_hosts:
        print("❌ No alive hosts found in subnet.")
    else:
        print(f"\nAlive hosts in {subnet}:")
        for host in alive_hosts:
            print(f"- {host}")

def main():
    print("""
==============================
🔥 Advanced Network Scanner 🔥
==============================

Options:
1. Ping a single host
2. Port scan a single host
3. Ping sweep a subnet
4. Port scan a single host with custom port range
5. Exit
""")
    while True:
        choice = input("Choose an option (1-5): ")
        if choice == "1":
            host = input("Enter host IP or domain: ")
            alive = ping_host(host)
            if alive:
                print(f"✅ Host {host} is alive.")
            else:
                print(f"❌ Host {host} is not reachable.")
        elif choice == "2":
            host = input("Enter host IP or domain: ")
            scan_ports(host, 1, 1024)
        elif choice == "3":
            subnet = input("Enter subnet (e.g. 192.168.1.0/24): ")
            scan_subnet(subnet)
        elif choice == "4":
            host = input("Enter host IP or domain: ")
            start_port = int(input("Enter start port: "))
            end_port = int(input("Enter end port: "))
            scan_ports(host, start_port, end_port)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    main()
