import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utils.monitor import get_system_status
from utils.maintenance import limpar_cache, encerrar_pesados, verificar_firewall

# --- Variáveis globais ---
pet_health = 100
frame_index = 0

# --- Janela principal ---
root = tk.Tk()
root.title("🐾 Monitori - Seu Pet do Sistema")
root.geometry("420x560")
root.resizable(False, False)
root.configure(bg="#E7ECF2")

# --- Tema moderno ttk ---
style = ttk.Style()
style.theme_use("clam")
style.configure("TProgressbar", troughcolor="#DDE3EA", background="#6EC1E4", thickness=14, borderwidth=0)
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

# --- Função para carregar frames ---
def carregar_frames(prefixo):
    frames = []
    for i in range(1, 4):
        img = Image.open(f"assets/{prefixo}_{i}.png").resize((180, 180))
        frames.append(ImageTk.PhotoImage(img))
    return frames

frames_happy = carregar_frames("happy")
frames_neutral = carregar_frames("neutral")
frames_sad = carregar_frames("sad")

# --- Frame principal (card) ---
frame_main = tk.Frame(root, bg="white", bd=0, relief="solid", highlightthickness=1, highlightbackground="#C9D1D9")
frame_main.pack(pady=20, padx=20, fill="both", expand=True)

# --- Pet ---
lbl_pet = tk.Label(frame_main, image=frames_happy[0], bg="white")
lbl_pet.pack(pady=15)

# --- Saúde ---
barra_saude = ttk.Progressbar(frame_main, length=220, mode="determinate", maximum=100)
barra_saude.pack(pady=6)
barra_saude["value"] = pet_health

lbl_msg = tk.Label(frame_main, text="", bg="white", wraplength=300, font=("Segoe UI", 9))
lbl_msg.pack(pady=8)

# --- Dados do sistema ---
dados_frame = tk.Frame(frame_main, bg="white")
dados_frame.pack(pady=10)

lbl_cpu = tk.Label(dados_frame, text="CPU: --%", bg="white", font=("Consolas", 10))
lbl_ram = tk.Label(dados_frame, text="RAM: --%", bg="white", font=("Consolas", 10))
lbl_disk = tk.Label(dados_frame, text="Disco: --%", bg="white", font=("Consolas", 10))
lbl_cpu.pack()
lbl_ram.pack()
lbl_disk.pack()

# --- Funções ---
def atualizar_pet():
    global frame_index
    if pet_health > 70:
        frames = frames_happy
    elif pet_health > 40:
        frames = frames_neutral
    else:
        frames = frames_sad

    lbl_pet.config(image=frames[frame_index])
    lbl_pet.image = frames[frame_index]
    frame_index = (frame_index + 1) % len(frames)
    root.after(300, atualizar_pet)

def atualizar_dados():
    global pet_health
    cpu, ram, disk = get_system_status()
    lbl_cpu.config(text=f"CPU: {cpu}%")
    lbl_ram.config(text=f"RAM: {ram}%")
    lbl_disk.config(text=f"Disco: {disk}%")

    if cpu > 85 or ram > 90 or disk > 90:
        pet_health = max(0, pet_health - 5)
    else:
        pet_health = min(100, pet_health + 1)

    barra_saude["value"] = pet_health
    root.after(3000, atualizar_dados)

def executar_tarefa(func):
    global pet_health
    msg = func()
    lbl_msg.config(text=msg)
    pet_health = min(100, pet_health + 10)

# --- Botões ---
frame_botoes = tk.Frame(root, bg="#E7ECF2")
frame_botoes.pack(pady=10)

def criar_botao(texto, func):
    return tk.Button(
        frame_botoes, 
        text=texto, 
        command=lambda: executar_tarefa(func),
        bg="#6EC1E4", fg="white",
        activebackground="#5AA8CA",
        relief="flat", font=("Segoe UI", 10, "bold"),
        width=18, height=1, bd=0,
        highlightthickness=0, cursor="hand2"
    )

criar_botao("🧹 Limpar Cache", limpar_cache).pack(pady=5)
criar_botao("⚙️ Encerrar Pesados", encerrar_pesados).pack(pady=5)
criar_botao("🛡️ Verificar Firewall", verificar_firewall).pack(pady=5)

# --- Loop principal ---
atualizar_pet()
atualizar_dados()
root.mainloop()
