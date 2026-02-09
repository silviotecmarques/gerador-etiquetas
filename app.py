import tkinter as tk
from tkinter import messagebox, ttk
from engine import gerar_pdf_etiquetas, DESTINOS
import os
import sys

# Cores e Configurações
COR_PRIMARIA = "#156082"
COR_FUNDO = "#f4f7f9"
COR_TEXTO = "#2c3e50"
COR_BRANCO = "#ffffff"
COR_SUBTIL = "#95a5a6"
ARQUIVO_CONFIG = "config_origem.txt"

def carregar_origem_padrao():
    if os.path.exists(ARQUIVO_CONFIG):
        with open(ARQUIVO_CONFIG, "r") as f:
            un = f.read().strip()
            if un in DESTINOS: return un
    return DESTINOS[0]

def abrir_vizualizador(caminho):
    if sys.platform == "win32": os.startfile(caminho)
    else: os.system(f"xdg-open {caminho}")

def on_click(event):
    if entry_vol.get() == 'QUANTIDADE DE CAIXAS':
        entry_vol.delete(0, "end")
        entry_vol.config(fg=COR_TEXTO)

def on_out(event):
    if entry_vol.get() == '':
        entry_vol.insert(0, 'QUANTIDADE DE CAIXAS')
        entry_vol.config(fg=COR_SUBTIL)

def acao():
    rem, dest, nf, vol_raw = var_rem.get(), var_dest.get(), entry_nf.get(), entry_vol.get()
    if vol_raw == 'QUANTIDADE DE CAIXAS' or not vol_raw or not nf:
        messagebox.showwarning("Aviso", "Preencha a NF e a Quantidade corretamente.")
        return
    try:
        vols = int(vol_raw)
        with open(ARQUIVO_CONFIG, "w") as f: f.write(rem)
        gerar_pdf_etiquetas("etiquetas_saida.pdf", {'remetente': rem, 'destino': dest, 'nf': nf}, vols)
        abrir_vizualizador("etiquetas_saida.pdf")
    except: messagebox.showerror("Erro", "Quantidade inválida.")

# --- Janela Principal ---
root = tk.Tk()
root.title("Expedição - Maxi/Ultra Popular")
root.geometry("450x580")
root.configure(bg=COR_FUNDO)

# Bloquear Maximizar
root.resizable(False, False)

# Ícone (Remover a pena)
if os.path.exists("logo.ico"):
    root.iconbitmap("logo.ico")

header = tk.Frame(root, bg=COR_PRIMARIA, height=70)
header.pack(fill='x')
header.pack_propagate(False)
tk.Label(header, text="GERADOR DE ETIQUETAS", bg=COR_PRIMARIA, fg=COR_BRANCO, font=("Segoe UI", 14, "bold")).pack(expand=True)

main = tk.Frame(root, bg=COR_FUNDO, padx=30, pady=20)
main.pack(fill='both', expand=True)

# Interface
tk.Label(main, text="ORIGEM (REMETENTE):", bg=COR_FUNDO, font=("Segoe UI", 9, "bold")).pack(fill='x', pady=(10,0))
var_rem = tk.StringVar(value=carregar_origem_padrao())
ttk.Combobox(main, textvariable=var_rem, values=DESTINOS, state="readonly", font=("Segoe UI", 11)).pack(fill='x', pady=5)

tk.Label(main, text="DESTINO:", bg=COR_FUNDO, font=("Segoe UI", 9, "bold")).pack(fill='x', pady=(10,0))
var_dest = tk.StringVar(value=DESTINOS[0])
ttk.Combobox(main, textvariable=var_dest, values=DESTINOS, state="readonly", font=("Segoe UI", 11)).pack(fill='x', pady=5)

tk.Label(main, text="NOTA FISCAL:", bg=COR_FUNDO, font=("Segoe UI", 9, "bold")).pack(fill='x', pady=(10,0))
entry_nf = tk.Entry(main, font=("Segoe UI", 12), bd=1, relief="solid")
entry_nf.pack(fill='x', ipady=5, pady=5)

tk.Label(main, text="VOLUMES:", bg=COR_FUNDO, font=("Segoe UI", 9, "bold")).pack(fill='x', pady=(10,0))
entry_vol = tk.Entry(main, font=("Segoe UI", 12), bd=1, relief="solid", fg=COR_SUBTIL)
entry_vol.insert(0, 'QUANTIDADE DE CAIXAS')
entry_vol.bind('<FocusIn>', on_click)
entry_vol.bind('<FocusOut>', on_out)
entry_vol.pack(fill='x', ipady=5, pady=5)

tk.Button(main, text="GERAR E CONFERIR PDF", bg=COR_PRIMARIA, fg=COR_BRANCO, 
          font=("Segoe UI", 12, "bold"), relief="flat", command=acao, height=2, cursor="hand2").pack(fill='x', pady=25)

root.mainloop()