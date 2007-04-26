def get_ip():
    """
    return the ip address as a string    
    """

    import socket
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip = '127.0.0.1'
    return ip
