import tkinter as tk
from tkinter import ttk, messagebox
import engine
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def executar_geracao():
    dados = {
        'remetente': combo_remetente.get(),
        'destino': combo_destino.get(),
        'nf': entry_nf.get()
    }
    qtd = entry_volumes.get()
    
    if not dados['nf'] or not qtd:
        messagebox.showwarning("Atenção", "Preencha a NF e a Quantidade!")
        return

    sucesso = engine.gerar_pdf_etiquetas("etiquetas_geradas.pdf", dados, qtd)
    
    if sucesso:
        messagebox.showinfo("Sucesso", "PDF Gerado com sucesso!")
        os.startfile("etiquetas_geradas.pdf")
    else:
        messagebox.showerror("Erro", "Falha ao gerar o PDF. Verifique os dados.")

root = tk.Tk()
root.title("Gerador de Etiquetas - Grupo Silvio")
root.geometry("400x450")

# --- CORREÇÃO DO ÍCONE NA BARRA DE TAREFAS ---
icon_path = resource_path("icone.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(main_frame, text="Remetente:").pack(pady=5)
combo_remetente = ttk.Combobox(main_frame, values=engine.DESTINOS, state="readonly")
combo_remetente.current(0)
combo_remetente.pack(fill=tk.X)

ttk.Label(main_frame, text="Destino:").pack(pady=5)
combo_destino = ttk.Combobox(main_frame, values=engine.DESTINOS, state="readonly")
combo_destino.current(1)
combo_destino.pack(fill=tk.X)

ttk.Label(main_frame, text="Nota Fiscal:").pack(pady=5)
entry_nf = ttk.Entry(main_frame)
entry_nf.pack(fill=tk.X)

ttk.Label(main_frame, text="Quantidade de Volumes:").pack(pady=5)
entry_volumes = ttk.Entry(main_frame)
entry_volumes.pack(fill=tk.X)

btn_gerar = ttk.Button(main_frame, text="GERAR ETIQUETAS", command=executar_geracao)
btn_gerar.pack(pady=30, fill=tk.X)

root.mainloop()