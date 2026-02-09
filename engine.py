from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
import os

# --- CONFIGURAÇÃO DAS LOJAS (Cores e Logos) ---
CONFIG_LOJAS = {
    "ABAETETUBA 01":  {"cor": "#ff9966", "logo": "maxi.png"},
    "ABAETETUBA 02":  {"cor": "#00b050", "logo": "maxi.png"},
    "BARCARENA":      {"cor": "#7030a0", "logo": "maxi.png"},
    "CAMETA":         {"cor": "#ffc000", "logo": "maxi.png"},
    "CAPANEMA 01":    {"cor": "#a6c9ec", "logo": "maxi.png"},
    "CAPANEMA 02":    {"cor": "#0ae1a8", "logo": "maxi.png"},
    "CAPITÃO POÇO":   {"cor": "#ffff00", "logo": "maxi.png"},
    "CASTANHAL 01":   {"cor": "#f7c7ac", "logo": "maxi.png"},
    "CASTANHAL 02":   {"cor": "#0070c0", "logo": "maxi.png"},
    "CASTANHAL 03":   {"cor": "#990033", "logo": "ultra.png"},
    "CASTANHAL 04":   {"cor": "#993366", "logo": "maxi.png"},
    "CASTANHAL 05":   {"cor": "#00ffff", "logo": "maxi.png"},
    "ITAITUBA 01":    {"cor": "#fbe2d5", "logo": "maxi.png"},
    "ITAITUBA 02":    {"cor": "#196b24", "logo": "maxi.png"},
    "MÃE DO RIO":     {"cor": "#ff0000", "logo": "maxi.png"},
    "QUATRO BOCAS":   {"cor": "#d86dcd", "logo": "maxi.png"},
    "SANTA ISABEL":   {"cor": "#92d050", "logo": "maxi.png"},
}

DESTINOS = sorted(list(CONFIG_LOJAS.keys()))

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16)/255.0 for i in (0, 2, 4))

def desenhar_etiqueta(c, x, y, largura, altura, dados):
    cor_azul_petroleo = hex_to_rgb("#156082")
    cor_branco = (1, 1, 1)
    cor_preto = (0, 0, 0)

    # Borda
    c.setLineWidth(1)
    c.setStrokeColorRGB(*cor_preto)
    c.rect(x, y, largura, altura)
    
    x_meio = x + (largura / 2)
    y_topo = y + altura
    y_centro = y + (altura / 2)
    y_box_dest = y_centro + 4 * mm
    y_limite_inferior_topo = y_box_dest + 7 * mm

    # 1. LOGO
    info_loja = CONFIG_LOJAS.get(dados['remetente'], {"logo": "maxi.png"}) 
    arquivo_logo = info_loja["logo"]
    if os.path.exists(arquivo_logo):
        c.drawImage(arquivo_logo, x, y_limite_inferior_topo, width=largura/2, height=y_topo - y_limite_inferior_topo, preserveAspectRatio=True, anchor='c')
    else:
        c.rect(x, y_limite_inferior_topo, largura/2, y_topo - y_limite_inferior_topo, stroke=1)

    # 2. REMETENTE
    c.setFillColorRGB(*cor_azul_petroleo) 
    c.rect(x_meio, y_topo - 7*mm, largura/2, 7*mm, fill=1, stroke=1)
    c.setFillColorRGB(*cor_branco)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x_meio + 2*mm, y_topo - 5*mm, "REMETENTE:")
    
    c.setFillColorRGB(*cor_preto)
    c.setFont("Helvetica-Bold", 12) 
    c.drawString(x_meio + (largura/2 - c.stringWidth(dados['remetente'], "Helvetica-Bold", 12))/2, y_limite_inferior_topo + (y_topo - 7*mm - y_limite_inferior_topo)/2 - 1.5*mm, dados['remetente'])

    # 3. DESTINO
    c.setFillColorRGB(*cor_azul_petroleo) 
    c.rect(x, y_box_dest, largura, 7*mm, fill=1, stroke=1)
    c.setFillColorRGB(*cor_branco)
    c.setFont("Helvetica-Bold", 11) 
    c.drawString(x + (largura - c.stringWidth("DESTINO:", "Helvetica-Bold", 11))/2, y_box_dest + 2*mm, "DESTINO:")

    # Fundo Colorido do Destino
    y_inf_dest = y + 20*mm
    info_dest = CONFIG_LOJAS.get(dados['destino'], {"cor": "#ffffff"})
    c.setFillColorRGB(*hex_to_rgb(info_dest["cor"]))
    c.rect(x, y_inf_dest, largura, y_box_dest - y_inf_dest, fill=1, stroke=1)

    c.setFillColorRGB(*cor_preto)
    c.setFont("Helvetica-Bold", 25) 
    c.drawString(x + (largura - c.stringWidth(dados['destino'], "Helvetica-Bold", 25))/2, y_inf_dest + (y_box_dest - y_inf_dest)/2 - 3.5*mm, dados['destino'])

    # 4. RODAPÉ
    y_footer = y_inf_dest - 7*mm
    c.setFillColorRGB(*cor_azul_petroleo)
    c.rect(x, y_footer, largura/2, 7*mm, fill=1, stroke=1)
    c.rect(x_meio, y_footer, largura/2, 7*mm, fill=1, stroke=1)
    
    c.setFillColorRGB(*cor_branco)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 2*mm, y_footer + 2*mm, "NOTA FISCAL:")
    c.drawString(x_meio + 2*mm, y_footer + 2*mm, "VOLUME:")
    
    c.setFillColorRGB(*cor_preto)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + (largura/4 - c.stringWidth(dados['nf'], "Helvetica-Bold", 12)/2), y + 6*mm, dados['nf'])
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x_meio + (largura/4 - c.stringWidth(dados['vol_status'], "Helvetica-Bold", 16)/2), y + 5*mm, dados['vol_status'])
    c.line(x_meio, y, x_meio, y_footer)

def gerar_pdf_etiquetas(nome_arquivo, dados_base, qtd_volumes):
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura_a4, altura_a4 = A4
    m_x, m_y, esp = 10*mm, 10*mm, 15*mm
    larg_e = (largura_a4 - 2*m_x - esp)/2
    alt_e = (altura_a4 - 2*m_y - 2*esp)/3
    
    for i in range(1, qtd_volumes + 1):
        idx = (i - 1) % 6
        if i > 1 and idx == 0: c.showPage()
        col, lin = idx % 2, idx // 2
        px = m_x + (col * (larg_e + esp))
        py = (altura_a4 - m_y) - ((lin + 1) * alt_e) - (lin * esp)
        dados = {**dados_base, 'vol_status': f"{i} / {qtd_volumes}"}
        desenhar_etiqueta(c, px, py, larg_e, alt_e, dados)
    c.save()