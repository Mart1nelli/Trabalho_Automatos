import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Tela
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu de Casos")

# Fonte
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 48)

def desenhar_menu():
    screen.fill(WHITE)
    titulo = large_font.render("Escolha o Caso", True, BLACK)
    screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 100))

    botao_case1 = pygame.Rect(WIDTH//2 - 150, 250, 300, 80)
    botao_case2 = pygame.Rect(WIDTH//2 - 150, 400, 300, 80)

    pygame.draw.rect(screen, GRAY, botao_case1)
    pygame.draw.rect(screen, GRAY, botao_case2)

    texto1 = font.render("Case 1 - Máquina de Doce", True, BLACK)
    texto2 = font.render("Case 2 - Elevador", True, BLACK)

    screen.blit(texto1, (WIDTH//2 - texto1.get_width()//2, 275))
    screen.blit(texto2, (WIDTH//2 - texto2.get_width()//2, 425))

    pygame.display.flip()
    return botao_case1, botao_case2

# Funções dos casos

def executar_case1():
    import subprocess
    subprocess.run([sys.executable, "MaquinaDeDoces.py"])

def executar_case2():
    import subprocess
    subprocess.run([sys.executable, "Elevador.py"])

# Loop do menu
rodando = True
while rodando:
    botoes = desenhar_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if botoes[0].collidepoint(event.pos):
                executar_case1()
            elif botoes[1].collidepoint(event.pos):
                executar_case2()

pygame.quit()
sys.exit()
