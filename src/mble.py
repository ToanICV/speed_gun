import socket
import struct
import base64


class BLE:
    def __init__(self, macAddr: str, channel: int):
        self.socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) 
        self.socket.bind((macAddr, channel))
        self.socket.listen()
        self.client, self.addr = self.socket.accept()

    def send(self, data):
        # Prefix each message with a 4-byte length (network byte order)
        data = struct.pack('>I', len(data)) + data
        self.socket.send(data)

    def send_img(self,img_path: str):
        try:
            with open(img_path, "rb") as image_file:
                image_data = image_file.read()
            encoded_image = base64.b64encode(image_data).decode("utf-8")
            self.send(encoded_image.encode('utf-8'))
        except Exception as e:
            print(f"Error sending image: {e}")