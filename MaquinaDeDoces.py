import pygame
import sys
import os
import subprocess

# Inicializa o Pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (211, 211, 211)
BLUE = (0, 0, 255)
HOVER_COLOR = (100, 100, 255)

# Tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Máquina de Doces")

# Fonte
font = pygame.font.SysFont(None, 32)
large_font = pygame.font.SysFont(None, 48)

# Preços dos doces
precos = {"A": 6, "B": 7, "C": 8}
saldo = 0
mensagem = ""
doce_img = None

# Carrega imagens dos doces (blocos coloridos)
doce_imgs = {
    "A": pygame.Surface((60, 60)),
    "B": pygame.Surface((60, 60)),
    "C": pygame.Surface((60, 60))
}
doce_imgs["A"].fill((255, 0, 0))  # Vermelho
doce_imgs["B"].fill((0, 255, 0))  # Verde
doce_imgs["C"].fill((0, 0, 255))  # Azul

# Botões
botao_1 = pygame.Rect(50, 100, 100, 50)
botao_2 = pygame.Rect(50, 170, 100, 50)
botao_5 = pygame.Rect(50, 240, 100, 50)
botao_a = pygame.Rect(200, 100, 100, 50)
botao_b = pygame.Rect(200, 170, 100, 50)
botao_c = pygame.Rect(200, 240, 100, 50)

def desenhar_texto(texto, x, y, cor=BLACK):
    img = font.render(texto, True, cor)
    screen.blit(img, (x, y))

def desenhar_tela():
    screen.fill(WHITE)

    # Título
    titulo = large_font.render("Máquina de Doces", True, BLACK)
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 20))

    # Botões de inserir dinheiro
    pygame.draw.rect(screen, LIGHT_BLUE, botao_1)
    pygame.draw.rect(screen, LIGHT_BLUE, botao_2)
    pygame.draw.rect(screen, LIGHT_BLUE, botao_5)
    desenhar_texto("R$1", botao_1.x + 30, botao_1.y + 10)
    desenhar_texto("R$2", botao_2.x + 30, botao_2.y + 10)
    desenhar_texto("R$5", botao_5.x + 30, botao_5.y + 10)

    # Botões de doces
    pygame.draw.rect(screen, GRAY, botao_a)
    pygame.draw.rect(screen, GRAY, botao_b)
    pygame.draw.rect(screen, GRAY, botao_c)
    desenhar_texto("Doce A", botao_a.x + 10, botao_a.y + 10)
    desenhar_texto("Doce B", botao_b.x + 10, botao_b.y + 10)
    desenhar_texto("Doce C", botao_c.x + 10, botao_c.y + 10)

    # Saldo
    desenhar_texto(f"Saldo: R${saldo},00", 400, 100)

    # Mensagem
    desenhar_texto(mensagem, 400, 150, RED if "Erro" in mensagem else BLACK)

    # Doce entregue
    if doce_img:
        desenhar_texto("Doce Entregue:", 400, 250)
        screen.blit(doce_img, (400, 280))

    # Desenhar botão de voltar
    desenhar_botao_voltar()

    pygame.display.flip()

# Adicionando o botão de voltar ao menu
def desenhar_botao_voltar():
    mouse_pos = pygame.mouse.get_pos()
    botao_voltar = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 60, 200, 40)

    if botao_voltar.collidepoint(mouse_pos):
        pygame.draw.rect(screen, HOVER_COLOR, botao_voltar, border_radius=10)
    else:
        pygame.draw.rect(screen, BLUE, botao_voltar, border_radius=10)

    texto_voltar = font.render("Voltar ao Menu", True, WHITE)
    screen.blit(texto_voltar, (botao_voltar.centerx - texto_voltar.get_width() // 2, botao_voltar.centery - texto_voltar.get_height() // 2))

    return botao_voltar

# Loop principal
rodando = True
clock = pygame.time.Clock()

while rodando:
    botao_voltar = desenhar_botao_voltar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            doce_img = None
            if botao_1.collidepoint(event.pos):
                saldo += 1
                mensagem = "R$1 inserido."
            elif botao_2.collidepoint(event.pos):
                saldo += 2
                mensagem = "R$2 inserido."
            elif botao_5.collidepoint(event.pos):
                saldo += 5
                mensagem = "R$5 inserido."
            elif botao_a.collidepoint(event.pos):
                if saldo >= precos["A"]:
                    troco = saldo - precos["A"]
                    mensagem = f"Doce A entregue. Troco: R${troco},00" if troco > 0 else "Doce A entregue."
                    doce_img = doce_imgs["A"]
                    saldo = 0
                else:
                    mensagem = "Erro: saldo insuficiente para Doce A."
            elif botao_b.collidepoint(event.pos):
                if saldo >= precos["B"]:
                    troco = saldo - precos["B"]
                    mensagem = f"Doce B entregue. Troco: R${troco},00" if troco > 0 else "Doce B entregue."
                    doce_img = doce_imgs["B"]
                    saldo = 0
                else:
                    mensagem = "Erro: saldo insuficiente para Doce B."
            elif botao_c.collidepoint(event.pos):
                if saldo >= precos["C"]:
                    troco = saldo - precos["C"]
                    mensagem = f"Doce C entregue. Troco: R${troco},00" if troco > 0 else "Doce C entregue."
                    doce_img = doce_imgs["C"]
                    saldo = 0
                else:
                    mensagem = "Erro: saldo insuficiente para Doce C."
            # Verifica se o botão de voltar foi clicado
            elif botao_voltar.collidepoint(event.pos):
                pygame.quit()
                subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "Menu.py")])
                sys.exit()

    desenhar_tela()
    clock.tick(30)

pygame.quit()
sys.exit()
