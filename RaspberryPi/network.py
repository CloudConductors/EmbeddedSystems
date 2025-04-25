import socket

def ping_aws():
    """
    Pings AWS to check if it is reachable.

    Returns:
        bool: True if AWS is reachable, False otherwise.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect(("dynamodb.us-east-1.amazonaws.com", 443))
            return True
    except socket.error:
        return False
    except socket.timeout:
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False