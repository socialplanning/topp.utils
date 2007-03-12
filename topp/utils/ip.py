def get_ip():
    """
    return the ip address as a string    
    """

    import socket
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip
