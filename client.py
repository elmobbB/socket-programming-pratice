import socket
import struct,os
import time

IP_ADDRESS = "132.196.0.1"  # Replace with the actual IP address of the server
PORT = 16011  # Replace with the actual port number of the server
BUFFER_SIZE = 4096


def send_command(sock, command):
    # Send the command to the server

    sock.sendall(bytes(command, encoding="utf-8"))
    response = sock.recv(BUFFER_SIZE).decode("utf-8")
    return response


def post_string(sock):
    # Send the "POST_STRING" command to the server

    print("=== POST_STRING ===")
    sock.sendall(bytes("POST_STRING", encoding="utf-8"))

    while True:
        # Prompt the user to enter a line of text

        client_message = input("Enter a line of text (or '&' to finish): ")
        if client_message == '&':
            # If the user enters '&', send it to the server and break the loop
            sock.sendall(bytes(client_message, encoding="utf-8"))
            break
        # Send the line of text to the server
        sock.sendall(bytes(client_message, encoding="utf-8"))
    
    # Receive and decode the response from the server
    response = sock.recv(BUFFER_SIZE).decode("utf-8")
    print("Server response:", response)


def post_file(sock):
    print("=== POST_FILE ===")
    while True:
        # Prompt the user to enter the file path

        file_path = input("Enter the file path: ")
        
        # If the file does not exist, display an error message and prompt for the file path again

        if not os.path.isfile(file_path):
            print("Error: File does not exist. Please try again.")
        else:
            break
    # Extract the file name and size
    file_name = file_path.split("/")[-1]
    file_size = os.path.getsize(file_path)

    # If the file size exceeds the buffer size, display an error message and recursively call post_file

    if file_size > BUFFER_SIZE:
        print("Error: File size exceeds buffer size. Please try with a smaller file.")
        post_file(sock)
        return
    
    # Send the "POST_FILE" command to the server

    sock.sendall(bytes("POST_FILE", encoding="utf-8"))

    # Pack the file name and size into a struct and send it to the server

    file_info = struct.pack('128sl', bytes(file_name, encoding="utf-8"), file_size)
    sock.sendall(file_info)

    # Send the contents of the file to the server in chunks
    with open(file_path, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            sock.sendall(data)
    # Receive a response from the server
    response = sock.recv(1024)
    print("Server response:", response.decode("utf-8"))


def get_messages(sock):
    # Send the "GET" command to the server

    sock.sendall(bytes("GET", encoding="utf-8"))
    while True:
        # Receive and decode the response from the server
        response = sock.recv(BUFFER_SIZE).decode("utf-8")
        print(response)
        if response == 'server: &':
            break
        print(response)
    

def exit_program(sock):
    # Send the "EXIT" command to the server

    print("=== EXIT ===")
    sock.sendall(bytes("EXIT", encoding="utf-8"))

    # Receive and decode the response from the server

    response = sock.recv(1024)
    print("Server response:", response.decode("utf-8"))

def main():
    while True:
        server_ip = input("Enter the server IP address: ")
        server_port = input("Enter the server port number: ")

        try:
            server_port = int(server_port)
        except ValueError:
            print("Error: Invalid port number. Please enter a valid integer value.")
            continue

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server_ip, server_port)

        try:
            sock.connect(server_address)
            print("Connection successful.")
            break
        except ConnectionRefusedError:
            print("Error: Connection refused. Please check the server IP and port.")
        except socket.gaierror:
            print("Error: Invalid IP address. Please enter a valid IP address.")
        except OSError as e:
            print(f"Error: {e.strerror}. Please check the server IP and port.")

    # Rest of the code remains the same
    while True:
        print("\nAvailable commands:")
        print("1. POST_STRING")
        print("2. POST_FILE")
        print("3. GET")
        print("4. EXIT")

        command = input("Enter a command (1-4): ")

        if command == "1":
            post_string(sock)
        elif command == "2":    
            post_file(sock)
        elif command == "3":
            get_messages(sock)
        elif command == "4":
            exit_program(sock)
            break
        else:
            print("Invalid command. Please try again.")

    sock.close()

if __name__ == "__main__":
    main()