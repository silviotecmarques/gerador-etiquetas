import ctypes
import sys
import os

# --- RESOLUÇÃO DE CAMINHO PARA RECURSOS NO EXE ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- FIXAR ÍCONE NA BARRA DE TAREFAS ---
if sys.platform == "win32":
    try:
        # ID único para o Windows não confundir com o Python
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Farmacia.Expedicao.Maxi.V3')
    except: pass

import tkinter as tk
from tkinter import messagebox, ttk
from engine import gerar_pdf_etiquetas, DESTINOS

COR_P = "#156082"  # Azul Petróleo
COR_F = "#f4f7f9"  # Fundo suave
COR_T = "#2c3e50"
ARQ_C = "config_origem.txt"

def carregar_origem():
    if os.path.exists(ARQ_C):
        with open(ARQ_C, "r") as f:
            un = f.read().strip()
            if un in DESTINOS: return un
    return DESTINOS[0]

def acao():
    rem, dest, nf, vol_raw = var_rem.get(), var_dest.get(), entry_nf.get(), entry_vol.get()
    if vol_raw == 'QUANTIDADE DE CAIXAS' or not nf:
        messagebox.showwarning("Aviso", "Por favor, preencha a NF e a Quantidade!")
        return
    try:
        vols = int(vol_raw)
        # Salva a origem como padrão
        with open(ARQ_C, "w") as f: f.write(rem)
        
        gerar_pdf_etiquetas("etiquetas_saida.pdf", {'remetente': rem, 'destino': dest, 'nf': nf}, vols)
        
        if sys.platform == "win32": os.startfile("etiquetas_saida.pdf")
        else: os.system(f"xdg-open etiquetas_saida.pdf")
    except: 
        messagebox.showerror("Erro", "Quantidade de volumes inválida.")

root = tk.Tk()
root.title("Expedição - Maxi/Ultra Popular")
root.geometry("450x580")
root.configure(bg=COR_F)

# Desativa Maximizar
root.resizable(False, False)

# Ícone do Programa
path_ico = resource_path("logo.ico")
if os.path.exists(path_ico): 
    root.iconbitmap(path_ico)

# Cabeçalho Azul
header = tk.Frame(root, bg=COR_P, height=70)
header.pack(fill='x')
header.pack_propagate(False)
tk.Label(header, text="GERADOR DE ETIQUETAS", bg=COR_P, fg="white", font=("Segoe UI", 14, "bold")).pack(expand=True)

main = tk.Frame(root, bg=COR_F, padx=30, pady=20)
main.pack(fill='both', expand=True)

# Interface
tk.Label(main, text="ORIGEM (REMETENTE):", bg=COR_F, font=("Segoe UI", 9, "bold")).pack(fill='x', pady=(10,0))
var_rem = tk.StringVar(value=carregar_origem())
ttk.Combobox(main, textvariable=var_rem, values=DESTINOS, state="readonly", font=("Segoe UI", 11)).pack(fill='x', pady=5)

tk.Label(main, text="DESTINO:", bg=COR_F, font=("Segoe UI", 9, "bold")).pack(fill='x', pady=(10,0))
var_dest = tk.StringVar(value=DESTINOS[0])
ttk.Combobox(main, textvariable=var_dest, values=DESTINOS, state="readonly", font=("Segoe UI", 11)).pack(fill='x', pady=5)

tk.Label(main, text="NOTA FISCAL:", bg=COR_F, font=("Segoe UI", 9, "bold")).pack(fill='x', pady=(10,0))
entry_nf = tk.Entry(main, font=("Segoe UI", 12), bd=1, relief="solid")
entry_nf.pack(fill='x', ipady=5, pady=5)

tk.Label(main, text="VOLUMES:", bg=COR_F, font=("Segoe UI", 9, "bold")).pack(fill='x', pady=(10,0))
entry_vol = tk.Entry(main, font=("Segoe UI", 12), bd=1, relief="solid", fg="#95a5a6")
entry_vol.insert(0, 'QUANTIDADE DE CAIXAS')

# Placeholder Inteligente
entry_vol.bind('<FocusIn>', lambda e: (entry_vol.delete(0, 'end'), entry_vol.config(fg=COR_T)) if entry_vol.get()=='QUANTIDADE DE CAIXAS' else None)
entry_vol.bind('<FocusOut>', lambda e: (entry_vol.insert(0, 'QUANTIDADE DE CAIXAS'), entry_vol.config(fg="#95a5a6")) if entry_vol.get()=='' else None)

entry_vol.pack(fill='x', ipady=5, pady=5)

tk.Button(main, text="GERAR E CONFERIR PDF", bg=COR_P, fg="white", font=("Segoe UI", 12, "bold"), 
          relief="flat", command=acao, height=2, cursor="hand2").pack(fill='x', pady=25)

root.mainloop()