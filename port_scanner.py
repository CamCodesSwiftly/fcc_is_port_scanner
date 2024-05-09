import socket
import threading
import errno

from common_ports import ports_and_services


def test_single_port(target, port, verbose = False):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    print(f"Scanning port {port} on IP: {target}")
    result = s.connect_ex((target, port))
    if result == 0:
        s.close()
        return f"Port {port} is open"
    elif result == errno.ECONNREFUSED:
        s.close()
        return f"Port {port} connection was refused. Port is closed."
    else:
        s.close()
        return f"The connection to Port {port} failed with error code: {result}"
    # return(open_ports)


def get_open_ports(target, port_range, verbose):
    # check if address is correct
    invalid_address = is_invalid_address(target)
    if invalid_address == False:
        return invalid_address
    


    print(f"Scanning port range: {port_range} on IP: {target}")

    # scan for ports
    open_ports = []
    for port in range(port_range[0], port_range[1] + 1):
        if port in ports_and_services:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)  # Set a timeout for the connection attempt
            result = s.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            s.close()

    # handle verbose
    if verbose:
        # handle hostname
        verbose_open_ports = ""
        if not target[0].isdigit():
            ipAddress = socket.gethostbyname(target)
            verbose_open_ports = f"Open ports for {target} ({ipAddress})\nPORT     SERVICE\n"
        else: 
            hostname = socket.gethostbyaddr(target)
            verbose_open_ports = f"Open ports for {hostname[0]} ({target})\nPORT     SERVICE\n"
        for index, port in enumerate(open_ports):
            whitespaces = 6 if len(str(port)) == 3 else 7
            if index != len(open_ports) - 1:
                port_string = f"{port}{" "*whitespaces}{ports_and_services[port]}\n" 
            else:
                port_string = f"{port}{" "*whitespaces}{ports_and_services[port]}"

            verbose_open_ports += port_string
        return verbose_open_ports

    return open_ports

def is_invalid_address(address):
    invalid = None
    try:
        socket.gethostbyaddr(address)
        invalid = False
    except socket.herror:
        invalid = True
    except socket.gaierror:
        invalid = True

    if invalid == True:
        if address[0].isdigit():
            return "Error: Invalid IP address"
        return "Error: Invalid hostname"

    return False  
         
