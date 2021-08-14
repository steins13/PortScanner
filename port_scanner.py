import socket
import nmap
import common_ports

def get_open_ports(target, port_range, verbose=None):
    #define scanner
    scanner = nmap.PortScanner()
    scanner.scan(target, str(port_range[0]) + "-" + str(port_range[1]))

    #variables
    openPorts = []
    services = []
    url = None
    ipAdd = None

    #determine open ports
    for host in scanner.all_hosts():
        ipAdd = host
        url = scanner[host].hostname()
        for proto in scanner[host].all_protocols():
            lport = scanner[host][proto].keys()
            for port in lport:
                if scanner[host][proto][port]['state'] == "open":
                    openPorts.append(port)

    #if IP or Hostname is invalid
    if len(openPorts) == 0:
        try:
            int(target[0])
        except:
            return "Error: Invalid hostname"
        return "Error: Invalid IP address"

    #if 3rd arg is true
    if verbose == True:
        #for services
        for port, serv in common_ports.ports_and_services.items():
            for openPort in openPorts:
                if port == openPort:
                    services.append(serv)
        
        #variables
        head = "Open ports for " + url + " (" + ipAdd + ")\nPORT     SERVICE\n"
        body = ""

        #for the head if url is empty
        if url == "":
            head = "Open ports for " + ipAdd + "\nPORT     SERVICE\n"

        #for the body
        index = 0
        while index < len(openPorts):
            port = openPorts[index]
            body = body + str(port)
            numOfSpaces = 9 - len(str(port))
            while numOfSpaces > 0:
                body = body + " "
                numOfSpaces = numOfSpaces - 1
            body = body + services[index] + "\n"
            index = index + 1
        return head + body.rstrip()
        
    return openPorts