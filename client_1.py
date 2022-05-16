import os
import tkinter
from datetime import datetime
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import filedialog


def recebe():
    """Lida com o recebimento de mensagens"""
    while True: # Loop infinito
        try:
            time = datetime.now() # Pega a hora atual
            getDatetime = time.strftime("%d/%m/%Y %H:%M:%S") # Formata a hora atual
            msg = client_socket.recv(1024).decode("utf8") # Recebe a mensagem
            msg_split = msg.split("@") # Separa a mensagem em partes
            window.title("Chat P2P " + remetente.get()) # Atualiza o título da janela
            
            if len(msg_split) > 1: # Se a mensagem tiver mais de uma parte
                destino = msg_split[1] # Pega o destinatário
                
                if destino == remetente.get(): # Se o destinatário for o remetente
                    
                    msg_list.insert(tkinter.END, "Remetente: " + msg_split[0]) # Insere a mensagem na lista
                    msg_list.insert(tkinter.END, "Mensagem: " + getDatetime
                                    + " " + msg_split[2]) # Insere a mensagem na lista
                    msg_list.insert(tkinter.END, " ") # Insere uma linha em branco na lista

            if len(msg_split) == 1: # Se a mensagem tiver apenas uma parte
                msg_list.insert(tkinter.END, msg) # Insere a mensagem na lista
                

        except OSError:  # Possivelmente o cliente saiu do chat.
            break # Sai do loop


def set_name():  # event is passed by binders.
    """Lida com o recebimento do nome do remetente."""
    msg = remetente.get() # Pega o nome do remetente
    client_socket.send(bytes(msg, "utf8"))


def send():
    """Lida com o envio de mensagens."""
    if destinatario.get() != "" and mensagem.get() != "":
        msg = "@" + destinatario.get() + "@" + mensagem.get()
        mensagem.set("")  # limpa o campo de mensagem
        client_socket.send(bytes(msg, "utf8")) # envia a mensagem


def send_file():
    """Envia arquivo"""
    file_path = filedialog.askopenfilename()
    file_name = file_path.split("/")[-1]
    file_size = str(os.path.getsize(file_path))
    msg = "@" + destinatario.get() + "@" + file_name + "@" + file_size
    client_socket.send(bytes(msg, "utf8"))
    with open(file_path, "rb") as f:
        bytes_read = f.read(1024)
        while bytes_read:
            client_socket.send(bytes_read)
            bytes_read = f.read(1024)
    client_socket.send(bytes("@", "utf8"))

def exit():
    """Encerrar a conexão"""
    msg = "quit" # Envia a mensagem de encerramento
    client_socket.send(bytes(msg, "utf8")) # Envia a mensagem de encerramento
    client_socket.close() # Fecha a conexão
    window.quit() # Fecha a janela


def fecha():
    """Essa funcão é chamada quando a janela é fechada"""
    mensagem.set("quit") # Envia a mensagem de encerramento
    send() # Envia a mensagem de encerramento


window = tkinter.Tk() # Cria a janela
window.configure(bg="#ffffff") # Configura a cor de fundo da janela
window.geometry("+450+10")  # tamanho e psocionamento

campo_conversa = tkinter.Frame(window) # Cria o frame
remetente = tkinter.StringVar()  # declarando o tipo do campo remetente
destinatario = tkinter.StringVar()  # declarando o tipo do campo destinatário
mensagem = tkinter.StringVar()  # declarando o tipo do campo mensagem
scrollbar = tkinter.Scrollbar(campo_conversa) # criando a barra de rolagem 
scrollbar2 = tkinter.Scrollbar(campo_conversa) # criando a barra de rolagem

l_remetente = tkinter.Label(
    window, 
    text="   Remetente:", 
    font="Ubuntu 14", 
    width=11, 
    height=2, 
    bg="#ffffff"
    ) # criando o label do remetente

l_destinatario = tkinter.Label(
    window, 
    text=" Destinatário:", 
    font="Ubuntu 14", 
    width=11, 
    height=2, 
    bg="#ffffff"
    ) # criando o label do destinatário

l_mensagem = tkinter.Label(
    window, 
    text="   Mensagem:",
    font="Ubuntu 14", 
    width=11, 
    height=2, 
    bg="#ffffff"
    ) # criando o label da mensagem

l_conversa = tkinter.Label(
    window, 
    text=" Conversa: ",
    font="Ubuntu 14", 
    height=2, 
    bg="#ffffff"
    ) # criando o label da conversa

msg_list = tkinter.Listbox(
    window, 
    height=11, 
    width=38, 
    font="Ubuntu 12 bold", 
    fg="#483659", 
    border=2,
    yscrollcommand=scrollbar.set
    ) # criando a lista de mensagens

e_remetente = tkinter.Entry(
    window, 
    font="Ubuntu 12 bold", 
    fg="#483659", 
    textvariable=remetente
    ) # criando o campo do remetente

e_remetente.bind("<Return>", ) # evento do enter
e_destinatario = tkinter.Entry(
    window, 
    font="Ubuntu 12 bold", 
    fg="#483659", 
    textvariable=destinatario
    ) # criando o campo do destinatário

e_destinatario.bind("<Return>", ) # evento do enter
e_mensagem = tkinter.Entry(
    window, 
    font="Ubuntu 12 bold", 
    fg="#483659", 
    width=65, 
    textvariable=mensagem
    ) # criando o campo da mensagem

e_mensagem.bind("<Return>", ) # evento do enter
window.protocol("WM_DELETE_WINDOW", fecha) # evento de fechar a janela

b_enviar_remetente = tkinter.Button(
    window, 
    text="    Enviar    ", 
    font="Ubuntu 14 bold", 
    height=1, 
    border=3,
    relief="groove", 
    fg="#483659", 
    command=set_name
    )  # criando o botão de enviar o remetente

b_enviar = tkinter.Button(
    window, 
    text="Enviar Mensagem", 
    font="Ubuntu 14 bold", 
    height=1, 
    border=3,
    relief="groove", 
    fg="#483659", 
    command=send
    ) # criando o botão de enviar a mensagem

b_sair = tkinter.Button(
    window, 
    text="Exit", 
    font="Ubuntu 14 bold", 
    fg="red", 
    border=3, 
    relief='groove',
    command=exit
    ) # criando o botão de encerrar a conexão

b_enviar_arquivo = tkinter.Button(
    window,
    text="Enviar Arquivo",
    font="Ubuntu 14 bold",
    height=1,
    border=3,
    relief="groove",
    fg="#483659",
    command=send_file
    ) # criando o botão de enviar arquivo

b_limpar_conversa = tkinter.Button(
    window,
    text="Limpar Conversa",
    font="Ubuntu 14 bold",
    height=1,
    border=3,
    relief="groove",
    fg="#483659",
    command=msg_list.delete(0, tkinter.END)
    ) # criando o botão de limpar a conversa

scrollbar.grid() # posiciona a barra de rolagem
msg_list.grid(row=2, column=3) # posiciona a lista de mensagens
campo_conversa.grid(column=3) # posiciona o frame

l_remetente.grid(row=1, column=1, sticky="n") # posiciona o label do remetente
l_destinatario.grid(row=2, column=1) # posiciona o label do destinatário 
l_mensagem.grid(row=4, column=1) # posiciona o label da mensagem
l_conversa.grid(row=1, column=3) # posiciona o label da conversa
 
e_remetente.grid(row=1, column=2) # posiciona o campo do remetente
e_destinatario.grid(row=2, column=2) # posiciona o campo do destinatário
e_mensagem.grid(row=4, column=2, columnspan=6) # posiciona o campo da mensagem

b_enviar.grid(row=5, column=2, sticky="n") # posiciona o botão de enviar a mensagem
b_enviar_remetente.grid(row=2, column=2, sticky="n") # posiciona o botão de enviar o remetente
b_sair.grid(row=5, column=3) # posiciona o botão de encerrar a conexão
b_enviar_arquivo.grid(row=5, column=1) # posiciona o botão de enviar arquivo
b_limpar_conversa.grid(row=5, column=4) # posiciona o botão de limpar a conversa

HOST = "localhost" # endereço do servidor
PORT = 50000 # porta do servidor
if not PORT: PORT = 50000 # porta do servidor
else: PORT = int(PORT) # porta do servidor

ADDR = (HOST, PORT) # endereço do servidor

client_socket = socket(AF_INET, SOCK_STREAM) # criando o socket
client_socket.connect(ADDR) # conectando ao servidor

receive_thread = Thread(target=recebe) # criando a thread de recebimento
receive_thread.start() # iniciando a thread de recebimento
"""início da execucão da interface"""
window.mainloop() # loop da interface
