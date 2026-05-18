import pygame
import sys
import os
from escpos.printer import Usb

# ==========================================
# CONFIGURACIÓN DE IMPRESIÓN
# ==========================================

# 1. Impresora Térmica Epson TM-T88V (Directo por USB)
def imprimir_epson_termica():
    try:
        p = Usb(0x04b8, 0x0202, profile="TM-T88V")
        p.set(align="center", text_type="B", width=2, height=2)
        p.text("¡Bienvenido a xxxxx!\n\n")
        p.set(align="center", text_type="NORMAL", width=1, height=1)
        p.text("Muchas gracias por su compra.\n")
        p.text("-" * 42 + "\n\n\n")
        p.cut()
        print("Ticket impreso en Epson TM-T88V.")
    except Exception as e:
        print(f"Error en Epson Térmica: {e}")

# 2. Impresora Normal (Utiliza la impresora predeterminada del sistema operativo)
def imprimir_impresora_normal():
    try:
        # Creamos un archivo de texto temporal con el mensaje
        nombre_archivo = "ticket_temporal.txt"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("¡Bienvenido a xxxxx!\n\n")
            f.write("Muchas gracias por su compra.\n")
        
        # Comando nativo de Windows para mandar a la impresora predeterminada de forma silenciosa
        if sys.platform == "win32":
            os.startfile(nombre_archivo, "print")
            print("Enviado a la cola de la impresora predeterminada de Windows.")
        else:
            # Comando genérico para Linux / macOS (si aplica)
            os.system(f"lp {nombre_archivo}")
            print("Enviado a la cola de impresión (Linux/Mac).")
            
    except Exception as e:
        print(f"Error en Impresora Normal: {e}")

# ==========================================
# CONFIGURACIÓN DE LA INTERFAZ (PYGAME)
# ==========================================
pygame.init()

# Resolución monitor de 15"
ANCHO, ALTO = 1024, 768
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sistema de Tickets - Multimpresión")

# Fuentes
fuente_titulo = pygame.font.SysFont("Arial", 50, bold=True)
fuente_boton = pygame.font.SysFont("Arial", 20, bold=True)

# Cargar Fondo Estirado (Sin Logo)
try:
    img_fondo = pygame.image.load("caja.png")
    img_fondo = pygame.transform.scale(img_fondo, (ANCHO, ALTO))
except pygame.error as e:
    print(f"Error al cargar caja.png: {e}")
    sys.exit()

# Dimensiones y posiciones de los botones (Columna a la derecha)
ancho_btn, alto_btn = 260, 70
pos_x_botones = ANCHO - ancho_btn - 80  # Margen desde la derecha

# Botón 1: Epson Térmica (Arriba)
btn_epson_rect = pygame.Rect(pos_x_botones, (ALTO // 2) - 80, ancho_btn, alto_btn)

# Botón 2: Impresora Normal (Abajo)
btn_normal_rect = pygame.Rect(pos_x_botones, (ALTO // 2) + 20, ancho_btn, alto_btn)

# Colores y Textos
COLOR_BTN_EPSON = (0, 150, 255)
COLOR_BTN_NORMAL = (46, 204, 113)
COLOR_HOVER = (44, 62, 80)
COLOR_TEXTO = (255, 255, 255)

texto_titulo = fuente_titulo.render("SISTEMA DE GESTIÓN", True, (255, 255, 255))
txt_btn_epson = fuente_boton.render("IMPRIMIR EPSON", True, COLOR_TEXTO)
txt_btn_normal = fuente_boton.render("IMPRIMIR NORMAL", True, COLOR_TEXTO)

# ==========================================
# BUCLE PRINCIPAL
# ==========================================
reloj = pygame.time.Clock()

while True:
    mouse_pos = pygame.mouse.get_pos()
    
    # Efectos Hover individuales
    color_actual_epson = COLOR_HOVER if btn_epson_rect.collidepoint(mouse_pos) else COLOR_BTN_EPSON
    color_actual_normal = COLOR_HOVER if btn_normal_rect.collidepoint(mouse_pos) else COLOR_BTN_NORMAL

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            # Limpieza del archivo temporal si existe al salir
            if os.path.exists("ticket_temporal.txt"):
                os.remove("ticket_temporal.txt")
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Clic izquierdo
                # Acción Botón Epson
                if btn_epson_rect.collidepoint(mouse_pos):
                    imprimir_epson_termica()
                
                # Acción Botón Normal
                if btn_normal_rect.collidepoint(mouse_pos):
                    imprimir_impresora_normal()

    # --- RENDERIZADO ---
    # 1. Fondo estirado completo
    pantalla.blit(img_fondo, (0, 0))
    
    # 2. Título Superior Centrado
    x_titulo = (ANCHO // 2) - (texto_titulo.get_width() // 2)
    pantalla.blit(texto_titulo, (x_titulo, 50))
    
    # 3. Dibujar Botón Epson Térmica
    pygame.draw.rect(pantalla, color_actual_epson, btn_epson_rect, border_radius=10)
    x_txt_epson = btn_epson_rect.x + (ancho_btn // 2) - (txt_btn_epson.get_width() // 2)
    y_txt_epson = btn_epson_rect.y + (alto_btn // 2) - (txt_btn_epson.get_height() // 2)
    pantalla.blit(txt_btn_epson, (x_txt_epson, y_txt_epson))
    
    # 4. Dibujar Botón Impresora Normal
    pygame.draw.rect(pantalla, color_actual_normal, btn_normal_rect, border_radius=10)
    x_txt_normal = btn_normal_rect.x + (ancho_btn // 2) - (txt_btn_normal.get_width() // 2)
    y_txt_normal = btn_normal_rect.y + (alto_btn // 2) - (txt_btn_normal.get_height() // 2)
    pantalla.blit(txt_btn_normal, (x_txt_normal, y_txt_normal))

    pygame.display.flip()
    reloj.tick(60)
