import customtkinter as ctk
import os
from engine import gerar_pdf_etiquetas, DESTINOS

class AppEtiquetas(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerador de Etiquetas V1.0")
        self.geometry("450x600")
        self.resizable(False, False)

        # Título
        self.label_titulo = ctk.CTkLabel(self, text="GERADOR DE ETIQUETAS", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)

        # --- REMETENTE (Agora com Menu) ---
        self.label_rem = ctk.CTkLabel(self, text="Selecione o Remetente:")
        self.label_rem.pack(pady=(10, 0))
        self.combo_remetente = ctk.CTkComboBox(self, values=DESTINOS, width=300)
        self.combo_remetente.pack(pady=5)

        # --- DESTINO ---
        self.label_dest = ctk.CTkLabel(self, text="Selecione o Destino:")
        self.label_dest.pack(pady=(10, 0))
        self.combo_destino = ctk.CTkComboBox(self, values=DESTINOS, width=300)
        self.combo_destino.pack(pady=5)

        # Nota Fiscal
        self.label_nf = ctk.CTkLabel(self, text="Número da Nota Fiscal:")
        self.label_nf.pack(pady=(10, 0))
        self.entry_nf = ctk.CTkEntry(self, width=300, placeholder_text="Ex: 000.123")
        self.entry_nf.pack(pady=5)

        # Volumes
        self.label_vol = ctk.CTkLabel(self, text="Quantidade de Volumes:")
        self.label_vol.pack(pady=(10, 0))
        self.entry_vol = ctk.CTkEntry(self, width=300, placeholder_text="Ex: 5")
        self.entry_vol.pack(pady=5)

        # Botão Gerar
        self.btn_gerar = ctk.CTkButton(self, text="GERAR PDF AGORA", command=self.executar_geracao, height=45, font=("Arial", 14, "bold"))
        self.btn_gerar.pack(pady=30)

        # Status
        self.label_status = ctk.CTkLabel(self, text="", text_color="yellow")
        self.label_status.pack()

    def executar_geracao(self):
        try:
            # Garante que a pasta existe
            if not os.path.exists("pdf_saida"):
                os.makedirs("pdf_saida")

            remetente = self.combo_remetente.get()
            destino = self.combo_destino.get()
            nf = self.entry_nf.get()
            
            if not self.entry_vol.get():
                raise ValueError("Digite a quantidade de volumes")
                
            vols = int(self.entry_vol.get())

            # Nome do arquivo: Etiquetas_DE_LojaA_PARA_LojaB.pdf
            nome_limpo_rem = remetente.replace(' ', '_')
            nome_limpo_dest = destino.replace(' ', '_')
            caminho = f"pdf_saida/Etiquetas_{nome_limpo_rem}_PARA_{nome_limpo_dest}_NF_{nf}.pdf"
            
            dados = {
                'remetente': remetente,
                'destino': destino,
                'nf': nf
            }
            
            gerar_pdf_etiquetas(caminho, dados, vols)

            self.label_status.configure(text=f"Sucesso! Salvo na pasta pdf_saida", text_color="green")
            
        except ValueError as e:
            self.label_status.configure(text=f"Erro: {str(e)}", text_color="red")
        except Exception as e:
            self.label_status.configure(text=f"Erro inesperado", text_color="red")

if __name__ == "__main__":
    app = AppEtiquetas()
    app.mainloop()