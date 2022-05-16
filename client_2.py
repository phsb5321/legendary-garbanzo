import os
import tkinter
from datetime import datetime
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import filedialog


def recebe():
    while True:
        try:
            time = datetime.now()
            getDatetime = time.strftime("%d/%m/%Y %H:%M:%S")
            msg = client_socket.recv(1024).decode("utf8")
            msg_split = msg.split("@")
            window.title("Chat P2P " + remetente.get())

            if msg_split[0] == "file":
                receive_file()

            if len(msg_split) > 1:
                destino = msg_split[1]

                if destino == remetente.get():
                    msg_list.insert(tkinter.END, "Remetente: " + msg_split[0])
                    msg_list.insert(tkinter.END, "Mensagem: " + getDatetime + " " + msg_split[2])
                    msg_list.insert(tkinter.END, " ")

            if len(msg_split) == 1:
                msg_list.insert(tkinter.END, msg)


        except OSError:
            break


def set_name():
    msg = remetente.get()
    client_socket.send(bytes(msg, "utf8"))


def send():
    if destinatario.get() != "" and mensagem.get() != "":
        msg = "@" + destinatario.get() + "@" + mensagem.get()
        mensagem.set("")
        client_socket.send(bytes(msg, "utf8"))


def send_file():
    file_path = filedialog.askopenfilename()
    file_name = file_path.split("/")[-1]
    file_size = str(os.path.getsize(file_path))
    msg = "file @" + destinatario.get() + "@" + file_name + "@" + file_size
    client_socket.send(bytes(msg, "utf8"))
    with open(file_path, "rb") as f:
        bytes_read = f.read(1024)
        while bytes_read:
            client_socket.send(bytes_read)
            bytes_read = f.read(1024)
    client_socket.send(bytes("@", "utf8"))


def receive_file():
    file_name = filedialog.asksaveasfile()
    file_size = client_socket.recv(1024).decode("utf8")
    file_size = int(file_size)
    with open(f'./files/{file_name}', "wb") as f:
        while file_size > 0:
            bytes_read = client_socket.recv(1024)
            if not bytes_read: break
            break
        f.write(bytes_read)
        file_size -= len(bytes_read)
    client_socket.send(bytes("@", "utf8"))


def exit():
    msg = "quit"
    client_socket.send(bytes(msg, "utf8"))
    client_socket.close()
    window.quit()


def fecha():
    mensagem.set("quit")
    send()


def delete_chat():
    msg_list.delete(0, tkinter.END)


window = tkinter.Tk()
window.configure(bg="#ffffff")
window.geometry("+450+10")

campo_conversa = tkinter.Frame(window)
remetente = tkinter.StringVar()
destinatario = tkinter.StringVar()
mensagem = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(campo_conversa)
scrollbar2 = tkinter.Scrollbar(campo_conversa)

l_remetente = tkinter.Label(
    window,
    text="   Remetente:",
    font="Ubuntu 14",
    width=11,
    height=2,
    bg="#ffffff"
)

l_destinatario = tkinter.Label(
    window,
    text=" Destinatário:",
    font="Ubuntu 14",
    width=11,
    height=2,
    bg="#ffffff"
)

l_mensagem = tkinter.Label(
    window,
    text="   Mensagem:",
    font="Ubuntu 14",
    width=11,
    height=2,
    bg="#ffffff"
)

l_conversa = tkinter.Label(
    window,
    text=" Conversa: ",
    font="Ubuntu 14",
    height=2,
    bg="#ffffff"
)

msg_list = tkinter.Listbox(
    window,
    height=11,
    width=38,
    font="Ubuntu 12 bold",
    fg="#483659",
    border=2,
    yscrollcommand=scrollbar.set
)

e_remetente = tkinter.Entry(
    window,
    font="Ubuntu 12 bold",
    fg="#483659",
    textvariable=remetente
)
e_remetente.bind("<Return>", set_name)

e_destinatario = tkinter.Entry(
    window,
    font="Ubuntu 12 bold",
    fg="#483659",
    textvariable=destinatario
)

e_mensagem = tkinter.Entry(
    window,
    font="Ubuntu 12 bold",
    fg="#483659",
    width=65,
    textvariable=mensagem
)
e_mensagem.bind("<Return>", send)

window.protocol("WM_DELETE_WINDOW", fecha)

b_enviar_remetente = tkinter.Button(
    window,
    text="    Enviar    ",
    font="Ubuntu 14 bold",
    height=1,
    border=3,
    relief="groove",
    fg="#483659",
    command=set_name
)

b_enviar = tkinter.Button(
    window,
    text="Enviar Mensagem",
    font="Ubuntu 14 bold",
    height=1,
    border=3,
    relief="groove",
    fg="#483659",
    command=send
)

b_sair = tkinter.Button(
    window,
    text="Exit",
    font="Ubuntu 14 bold",
    fg="red",
    border=3,
    relief='groove',
    command=exit
)

b_enviar_arquivo = tkinter.Button(
    window,
    text="Enviar Arquivo",
    font="Ubuntu 14 bold",
    height=1,
    border=3,
    relief="groove",
    fg="#483659",
    command=send_file
)

b_limpar_conversa = tkinter.Button(
    window,
    text="Limpar Conversa",
    font="Ubuntu 14 bold",
    height=1,
    border=3,
    relief="groove",
    fg="#483659",
    command=delete_chat
)

scrollbar.grid()
msg_list.grid(row=2, column=3)
campo_conversa.grid(column=3)

l_remetente.grid(row=1, column=1, sticky="n")
l_destinatario.grid(row=2, column=1)
l_mensagem.grid(row=4, column=1)
l_conversa.grid(row=1, column=3)

e_remetente.grid(row=1, column=2)
e_destinatario.grid(row=2, column=2)
e_mensagem.grid(row=4, column=2, columnspan=6)

b_enviar.grid(row=5, column=2, sticky="n")
b_enviar_remetente.grid(row=2, column=2, sticky="n")
b_sair.grid(row=5, column=3)
b_enviar_arquivo.grid(row=5, column=1)
b_limpar_conversa.grid(row=5, column=4)

HOST = "localhost"
PORT = 3000
if not PORT:
    PORT = 3000
else:
    PORT = int(PORT)

ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=recebe)
receive_thread.start()

window.mainloop()
