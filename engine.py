from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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
    cor_azul = hex_to_rgb("#156082")
    cor_branco = (1, 1, 1)
    cor_preto = (0, 0, 0)

    c.setLineWidth(1.5)
    c.setStrokeColorRGB(*cor_preto)
    c.rect(x, y, largura, altura)
    
    x_meio = x + (largura / 2)
    y_topo = y + altura
    h_barra = 10 * mm 

    # 1. CABEÇALHO (Logo Total: 70mm x 28mm)
    y_div_sup = y_topo - 28 * mm
    info_loja = CONFIG_LOJAS.get(dados['remetente'], {"logo": "maxi.png"}) 
    img_path = resource_path(info_loja["logo"])
    if os.path.exists(img_path):
        c.drawImage(img_path, x, y_div_sup, width=largura/2, height=28*mm, preserveAspectRatio=True, anchor='c')

    # Título REMETENTE: Esquerda da linha central
    c.setFillColorRGB(*cor_azul)
    c.rect(x_meio, y_topo - h_barra, largura/2, h_barra, fill=1)
    c.setFillColorRGB(*cor_branco)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(x_meio + 2*mm, y_topo - 7.5*mm, "REMETENTE:")
    
    # Resultado REMETENTE: Fonte 20 Centralizado
    c.setFillColorRGB(*cor_preto)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(x_meio + (largura/4 - c.stringWidth(dados['remetente'], "Helvetica-Bold", 20)/2), y_div_sup + 7*mm, dados['remetente'])

    # 2. RODAPÉ (NF E VOLUME)
    y_rodape_base = y + 22 * mm 
    c.setFillColorRGB(*cor_azul)
    c.rect(x, y_rodape_base - h_barra, largura/2, h_barra, fill=1)
    c.rect(x_meio, y_rodape_base - h_barra, largura/2, h_barra, fill=1)
    
    c.setFillColorRGB(*cor_branco)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(x + 2*mm, y_rodape_base - 7.5*mm, "NOTA FISCAL:")
    c.drawString(x_meio + 2*mm, y_rodape_base - 7.5*mm, "VOLUME:")
    
    # Resultados NF e Volume: Fonte 26 e abaixados para 2.5mm
    c.setFillColorRGB(*cor_preto)
    c.setFont("Helvetica-Bold", 26)
    y_texto_rodape = y + 2.5 * mm
    c.drawString(x + (largura/4 - c.stringWidth(dados['nf'], "Helvetica-Bold", 26)/2), y_texto_rodape, dados['nf'])
    c.drawString(x_meio + (largura/4 - c.stringWidth(dados['vol_status'], "Helvetica-Bold", 26)/2), y_texto_rodape, dados['vol_status'])

    # 3. BLOCO CENTRAL (DESTINO)
    c.setFillColorRGB(*cor_azul)
    c.rect(x, y_div_sup - h_barra, largura, h_barra, fill=1)
    c.setFillColorRGB(*cor_branco)
    c.setFont("Helvetica-Bold", 15)
    txt_dest = "DESTINO:"
    c.drawString(x + (largura/2 - c.stringWidth(txt_dest, "Helvetica-Bold", 15)/2), y_div_sup - 7.5*mm, txt_dest)

    y_cor_inicio = y_rodape_base
    h_cor = (y_div_sup - h_barra) - y_cor_inicio
    cor_loja = CONFIG_LOJAS.get(dados['destino'], {"cor": "#ffffff"})["cor"]
    c.setFillColorRGB(*hex_to_rgb(cor_loja))
    c.rect(x, y_cor_inicio, largura, h_cor, fill=1)
    
    c.setFillColorRGB(*cor_preto)
    c.setFont("Helvetica-Bold", 45)
    c.drawString(x + (largura/2 - c.stringWidth(dados['destino'], "Helvetica-Bold", 45)/2), y_cor_inicio + (h_cor/2) - 6*mm, dados['destino'])

    c.setLineWidth(1)
    c.line(x_meio, y, x_meio, y_rodape_base)

def gerar_pdf_etiquetas(nome_arquivo, dados_base, qtd_volumes):
    try:
        qtd_volumes = int(qtd_volumes)
        c = canvas.Canvas(nome_arquivo, pagesize=A4)
        largura_a4, altura_a4 = A4
        m_x, m_y, esp = 35*mm, 15*mm, 10*mm
        l_eti = largura_a4 - (2 * m_x)
        a_eti = (altura_a4 - (2 * m_y) - (2 * esp)) / 3
        for i in range(1, qtd_volumes + 1):
            idx = (i-1) % 3
            if i > 1 and idx == 0: c.showPage()
            py = (altura_a4 - m_y) - ((idx + 1) * a_eti) - (idx * esp)
            desenhar_etiqueta(c, m_x, py, l_eti, a_eti, {**dados_base, 'vol_status': f"{i} / {qtd_volumes}"})
        c.save()
        return True
    except Exception:
        return False