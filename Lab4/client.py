import socket
import time


class Client:
    def __init__(self, host='0.0.0.0', port=49513, skip=3):
        self.host = host
        self.port = port
        self.skip = skip

    def run_client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        expected_sequence_number = 0
        i = 0

        try:
            while True:
                frame = client_socket.recv(1024).decode('utf-8')
                if not frame:
                    break

                sequence_number, data = frame.split(":", 1)
                sequence_number = int(sequence_number)

                print(f"Received frame with sequence number {sequence_number}: {data.strip()}")

                if sequence_number == expected_sequence_number:
                    if i != self.skip:
                        print(f"Sending ACK for sequence number {sequence_number}")
                        client_socket.send(str(sequence_number).encode('utf-8'))
                        expected_sequence_number = 1 - expected_sequence_number
                    else:
                        print(f"Skipping ACK for sequence number {sequence_number}")
                else:
                    print(f"Unexpected sequence number. Resending ACK for {1 - expected_sequence_number}")
                    client_socket.send(str(1 - expected_sequence_number).encode('utf-8'))

                i += 1

        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()


if __name__ == "__main__":
    client = Client()
    client.run_client()
