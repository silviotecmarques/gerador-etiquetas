from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# LISTA OFICIAL EM ORDEM ALFABÉTICA
DESTINOS = [
    "ABAETETUBA 1", "ABAETETUBA 2", "BARCARENA 1", "CAMETA 1", 
    "CAPANEMA 1", "CAPANEMA 2", "CAPITÃO POÇO 1", "CASTANHAL 1", 
    "CASTANHAL 2", "CASTANHAL 3", "CASTANHAL 4", "CASTANHAL 5", 
    "ITAITUBA 1", "ITAITUBA 2", "MÃE DO RIO", "QUATRO BOCAS", "SANTA ISABEL 1"
]

def desenhar_etiqueta(c, x, y, largura, altura, dados):
    c.setLineWidth(0.8)
    c.rect(x, y, largura, altura)
    
    margem = 5 * mm
    
    # --- BLOCO REMETENTE ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + margem, y + altura - 15, "REMETENTE:")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x + margem, y + altura - 35, dados['remetente'])

    # Divisória
    c.setDash(2, 2)
    c.line(x + 2*mm, y + altura/2 + 10*mm, x + largura - 2*mm, y + altura/2 + 10*mm)
    c.setDash()

    # --- BLOCO DESTINO ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + margem, y + altura/2 + 2*mm, "DESTINO:")
    c.setFont("Helvetica-Bold", 24) # Destino bem grande
    txt_dest = dados['destino']
    larg_txt = c.stringWidth(txt_dest, "Helvetica-Bold", 24)
    c.drawString(x + (largura - larg_txt)/2, y + altura/2 - 15*mm, txt_dest)

    # Linha Base
    c.line(x, y + 45, x + largura, y + 45)

    # --- NF E VOLUME ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + margem, y + 30, "NOTA FISCAL:")
    c.setFont("Helvetica", 14)
    c.drawString(x + margem, y + 12, dados['nf'])

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + largura/2 + 5*mm, y + 30, "VOLUME:")
    c.setFont("Helvetica-Bold", 20)
    c.drawString(x + largura/2 + 5*mm, y + 12, dados['vol_status'])

def gerar_pdf_etiquetas(nome_arquivo, dados_base, qtd_volumes):
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura_a4, altura_a4 = A4
    margem_folha = 10 * mm
    colunas, linhas = 2, 3
    largura_eti = (largura_a4 - (2 * margem_folha)) / colunas
    altura_eti = (altura_a4 - (2 * margem_folha)) / linhas
    
    for i in range(1, qtd_volumes + 1):
        idx = (i - 1) % 6
        if i > 1 and idx == 0: c.showPage()
        
        col = idx % colunas
        lin = idx // colunas
        x = margem_folha + (col * largura_eti)
        y = altura_a4 - margem_folha - ((lin + 1) * altura_eti)
        
        dados = {**dados_base, 'vol_status': f"{i} / {qtd_volumes}"}
        desenhar_etiqueta(c, x, y, largura_eti, altura_eti, dados)
    c.save()