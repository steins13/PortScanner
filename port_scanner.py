import socket
import common_ports

def get_open_ports(target, port_range, verbose=None):

    #variables
    openPorts = []
    services = []
    url = ""
    ipAdd = ""
    start = port_range[0]
    end = port_range[1]

    #loop port_range
    while start <= end:
        #make socket and connect
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            mySocket.settimeout(2.0)
            #if close
            if mySocket.connect_ex((target, start)):
                start = start + 1
                continue
            #if open
            else:
                openPorts.append(start)
                start = start + 1
                mySocket.close()
        except:
            #if error
            try:
                int(target[0])
            except:
                return "Error: Invalid hostname"
            return "Error: Invalid IP address"

    #get url and ipAdd
    try:
        host = socket.gethostbyaddr(target)
        url = host[0]
        ipAdd = host[2][0]
    except:
        ipAdd = socket.gethostbyname(target)

    #if 3rd arg is true
    if verbose == True:
        #for services
        for port, serv in common_ports.ports_and_services.items():
            for openPort in openPorts:
                if port == openPort:
                    services.append(serv)
        
        #variables
        head = ""
        body = ""

        #for the head if url is empty
        if url == "":
            head = "Open ports for " + ipAdd + "\nPORT     SERVICE\n"
        else:
            head = "Open ports for " + url + " (" + ipAdd + ")\nPORT     SERVICE\n"

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