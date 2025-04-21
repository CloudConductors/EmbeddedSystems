import socket

def ping_aws():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.settimeout(1)
            s.connect(("dynamodb.us-east-1.amazonaws.com", 80))
            return True
    except socket.error:
        return False
    except socket.timeout:
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False