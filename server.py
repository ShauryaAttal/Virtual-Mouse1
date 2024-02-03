import socket
from threading import Thread
from pynput.mouse import Button, Controller
from screeninfo import get_monitors

# import autopy


SERVER = None
PORT = 8000
IP_ADDRESS = input("Enter your computer IP ADDR : ").strip()
screen_width = None
screen_height = None


mouse = Controller()


def getDeviceSize():
    global screen_height, screen_width

    for m in get_monitors():
        screen_width = int(str(m).split(",")[2].strip().split("width=")[1])
        screen_height = int(str(m).split(",")[3].strip().split("height=")[1])
        print(m)
        print(screen_width)


def recvMsg(client_socket):
    global mouse
    while True:
        try:
            msg = client_socket.recv(4096).decode()
            print("msg: ", msg)
            if msg:
                new_msg = eval(msg)
                if new_msg["data"] == "left_click":
                    mouse.press(Button.left)
                    mouse.release(Button.left)
                if new_msg["data"] == "right_click":
                    mouse.press(Button.right)
                    mouse.release(Button.right)
                else:
                    xpos = new_msg["data"][0] * screen_width
                    ypos = new_msg["data"][1] * screen_height
                    mouse.position = (int(xpos), int(ypos))
                    print(xpos, ypos)
                print("New_msg: ", new_msg)
        except Exception as e:
            pass


def acceptConnections():
    global SERVER

    while True:
        client_socket, addr = SERVER.accept()

        print(f"Connection established with {client_socket} : {addr}")
        thread = Thread(target=recvMsg, args=(client_socket,))
        thread.start()


# 192.168.86.53


def setup():
    print("\n\t\t\t\t\t*** Welcome To Remote Mouse ***\n")

    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")

    acceptConnections()


setup()
