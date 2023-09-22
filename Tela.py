from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import time
import controle
from tkinter import simpledialog, messagebox

frame = {}
def selecionar_arquivo(event):
    controle.web = filedialog.askopenfilename()
    if controle.web:
        print("Arquivo selecionado")
        label_document.config(bg='white', borderwidth=3, highlightbackground='green', highlightthickness=3)
    else:
        print("Arquivo nao selecionado")
        label_document.config(bg='white', borderwidth=3, highlightbackground='red', highlightthickness=3)
      

def update_count():
    global tempo_restante
    tempo_restante = tempo_restante - 1
    if tempo_restante < 0:
        tempo_restante = 0
        label_timer.config(borderwidth=3, highlightbackground='red', highlightthickness=3)
    else:
        label_timer.config(borderwidth=3, highlightbackground='blue', highlightthickness=3)

    timer_text.config(text=f"{tempo_restante}")
    root.after(1100, update_count)  # Atualiza a cada segundo (1000 ms)

def start_count():
    global tempo_restante
    tempo_restante = 600
    update_count()

def entregar_balao(nome, frame):

    global pendentes_frame
    for element in pendentes_frame.winfo_children():
        element.destroy()
    global coletados_frame
    for element in coletados_frame.winfo_children():
        element.destroy()
    
    
    for i in range(controle.Numero_questoes):
        if controle.pendentes[nome][i] == True:
            controle.concluidos[nome][i] = True
            controle.pendentes[nome][i] = False
            break
         
    update_screen()
    baloes(nome, frame)
    

def baloes(nome, frame):

    
    for i in range(controle.Numero_questoes):
        if controle.pendentes[nome][i] == True:
            x = Frame(pendentes_frame, width=20, height=20, bg=controle.cores[i])
            x.pack(side='left', padx=10, pady=10)
          

    for i in range(controle.Numero_questoes):
        if controle.concluidos[nome][i] == True:
            x = Frame(coletados_frame, width=20, height=20, bg=controle.cores[i])
            x.pack(side='left', padx=10, pady=10)

    

def info(frame):
    global window 
    window = Tk()
    window.geometry("400x450")
    window.title("Janela do competidor")
    name_label = Label(window, text=frame.nome, font=("Arial, 16"))
    name_label.pack(side='top', pady=10)

    pendentes_label = Label(window, text="Balões Pendentes", font=("Arial, 16"))
    pendentes_label.pack(side='top', pady=10)

    global pendentes_frame
    pendentes_frame = Frame(window, borderwidth=2, highlightthickness=2, highlightbackground='black', relief=RAISED)
    pendentes_frame.pack(side='top')

    coletados_label = Label(window, text="Balões Coletados",  font=("Arial, 16"))
    coletados_label.pack(side='top', pady=10)

    global coletados_frame
    coletados_frame = Frame(window, borderwidth=2, highlightthickness=2, highlightbackground='black', relief=RAISED)
    coletados_frame.pack(side='top')

    baloes(frame.nome,frame)

   
    btn = Button(window, width=15, height=3, text="Entregar balão", command=lambda : entregar_balao(frame.nome, frame)) 
    btn.pack(side='bottom', pady=20)
    window.mainloop()

def board():
    index = 0
    for i in range(controle.Tamanho_matriz):
        for j in range(controle.Tamanho_matriz):
            if index == controle.Numero_alunos:
                break
            nome = controle.Nome_alunos[controle.Tamanho_matriz*i + j]
            frame[nome] = Frame(master = content, relief=RAISED, borderwidth=3, width=200, height=200, highlightthickness=2)
            frame[nome].grid(row = i, column = j, padx = 10, pady = 10)
            frame[nome].pack_propagate(0)
            frame[nome].nome = nome
            name_label = Label(master=frame[nome], text=nome, font=("Arial, 10"))
            name_label.pack(pady=10)
            identificacao = Label(master=frame[nome], text="Numero de identificacao")
            identificacao.pack(pady=10)
            check_button = Button(master=frame[nome], text="Check", width=10, height=2, command=lambda f=frame[nome]: info(f)) 
            check_button.pack(pady=10, side='bottom')
            index+=1


def update_screen():
    for nome in controle.Nome_alunos:
        balao = False
        for i in range(controle.Numero_questoes):
            if controle.pendentes[nome][i] == True:
                balao = True
        if balao == True:
            frame[nome].config(highlightbackground='red', highlightthickness= 4)
        else:
            frame[nome].config(highlightbackground='black', highlightthickness = 2)


def update_score(event):
    import Update as up
    if controle.zerar == True:
        up.start()
        board()
        controle.zerar = False
    else:
        up.update()
        update_screen()
        up.delete()
    
    start_count()
    
def close_window():
    senha = simpledialog.askstring("Senha", "Digite a senha:", show='*')
    if senha == 'inatel2023':
        root.destroy()
    else:
        messagebox.showerror("Erro", "Senha incorreta. Fechamento cancelado.")

root = Tk()

root.geometry("700x700")
root.title("Gerenciador")

side_bar = Frame(root, width=100, bg='white',  relief=RAISED, borderwidth=2,highlightthickness=3, highlightbackground='black')
side_bar.pack(side='left', fill='y')

icon_document = 'C:\\Users\\Cliente\\Documents\\novo_gerenciador\\Document.png'
icon_document = Image.open(icon_document)
icon_document = icon_document.resize((80, 80))
icon_document = ImageTk.PhotoImage(icon_document)


label_document = Label(side_bar, image=icon_document, bg='white', relief=RAISED, borderwidth=3, highlightthickness=3)
label_document.grid(row=0, column=0, pady=100)
label_document.bind('<Button-1>', selecionar_arquivo)

icon_timer = 'C:\\Users\\Cliente\\Documents\\novo_gerenciador\\ampulheta.png'
icon_timer = Image.open(icon_timer)
icon_timer = icon_timer.resize((70,70))
icon_timer = ImageTk.PhotoImage(icon_timer)

label_timer = Label(side_bar, image=icon_timer, bg='white',relief=RAISED, borderwidth=3, highlightthickness=3)
label_timer.grid(row=1, column=0)

tempo_restante = 0
timer_text = Label(side_bar, text=f"{tempo_restante}")
timer_text.grid(row=2, column=0)


icon_update = 'C:\\Users\\Cliente\\Documents\\novo_gerenciador\\atualizar.png'
icon_update = Image.open(icon_update)
icon_update = icon_update.resize((70,70))
icon_update = ImageTk.PhotoImage(icon_update)

label_update = Label(side_bar, image=icon_update, bg='white',relief=RAISED, borderwidth=3, highlightthickness=3)
label_update.grid(row=3, column = 0, pady=130)
label_update.bind('<Button-1>', update_score)


content = Frame(root)
content.pack(side='top', fill='both', padx=10, pady=10)

zerar = True

#root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()
