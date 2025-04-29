import pygame
import sys
import os
from math import sin
import subprocess

# Inicializa o Pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (70, 130, 180)
BLUE = (0, 120, 215)
LIGHT_GRAY = (230, 230, 230)
HOVER_COLOR = (0, 150, 255)
PURPLE = (130, 80, 200)
LIGHT_PURPLE = (180, 120, 250)

# Tela
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu de Casos")

# Fontes
try:
    font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 54)
    title_font = pygame.font.Font(None, 70)
except:
    font = pygame.font.SysFont(None, 36)
    large_font = pygame.font.SysFont(None, 54)
    title_font = pygame.font.SysFont(None, 70)

# Carrega ou cria imagens para o fundo
def criar_gradiente():
    gradient = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        cor = (
            int(LIGHT_BLUE[0] * (1 - y/HEIGHT) + DARK_BLUE[0] * (y/HEIGHT)),
            int(LIGHT_BLUE[1] * (1 - y/HEIGHT) + DARK_BLUE[1] * (y/HEIGHT)),
            int(LIGHT_BLUE[2] * (1 - y/HEIGHT) + DARK_BLUE[2] * (y/HEIGHT))
        )
        pygame.draw.line(gradient, cor, (0, y), (WIDTH, y))
    return gradient

# Cria o fundo com gradiente
background = criar_gradiente()

# Animação
tempo = 0
clock = pygame.time.Clock()

def desenhar_menu():
    global tempo
    tempo += 0.02
    
    # Desenha o fundo
    screen.blit(background, (0, 0))
    
    # Desenha alguns círculos decorativos que se movem
    for i in range(10):
        x = WIDTH//2 + sin(tempo + i * 0.5) * 250
        y = HEIGHT//2 + sin(tempo * 0.7 + i * 0.3) * 320
        tamanho = 15 + sin(tempo + i) * 10
        alpha = 100 + sin(tempo + i) * 50
        
        # Cria uma superfície com canal alpha
        circle_surf = pygame.Surface((int(tamanho*2), int(tamanho*2)), pygame.SRCALPHA)
        pygame.draw.circle(circle_surf, (*LIGHT_PURPLE, int(alpha)), 
                          (int(tamanho), int(tamanho)), int(tamanho))
        screen.blit(circle_surf, (int(x - tamanho), int(y - tamanho)))
    
    # Título com sombra
    titulo_texto = "Menu de Casos"
    sombra = title_font.render(titulo_texto, True, (50, 50, 100))
    titulo = title_font.render(titulo_texto, True, WHITE)
    
    # Desenha a sombra e o título
    screen.blit(sombra, (WIDTH//2 - titulo.get_width()//2 + 3, 103))
    screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 100))
    
    subtitulo = large_font.render("Escolha uma opção:", True, WHITE)
    screen.blit(subtitulo, (WIDTH//2 - subtitulo.get_width()//2, 170))
    
    # Verifica a posição do mouse para efeito hover
    mouse_pos = pygame.mouse.get_pos()
    
    # Botões com efeitos
    botao_case1 = pygame.Rect(WIDTH//2 - 180, 280, 360, 90)
    botao_case2 = pygame.Rect(WIDTH//2 - 180, 430, 360, 90)
    
    # Desenha botão 1 com efeito hover
    if botao_case1.collidepoint(mouse_pos):
        pygame.draw.rect(screen, HOVER_COLOR, botao_case1, border_radius=15)
        pygame.draw.rect(screen, BLUE, botao_case1, 3, border_radius=15)
        texto1 = font.render("Máquina de Doce", True, WHITE)
    else:
        pygame.draw.rect(screen, BLUE, botao_case1, border_radius=15)
        pygame.draw.rect(screen, LIGHT_GRAY, botao_case1, 2, border_radius=15)
        texto1 = font.render("Máquina de Doce", True, WHITE)
    
    # Desenha botão 2 com efeito hover
    if botao_case2.collidepoint(mouse_pos):
        pygame.draw.rect(screen, HOVER_COLOR, botao_case2, border_radius=15)
        pygame.draw.rect(screen, BLUE, botao_case2, 3, border_radius=15)
        texto2 = font.render("Elevador", True, WHITE)
    else:
        pygame.draw.rect(screen, BLUE, botao_case2, border_radius=15)
        pygame.draw.rect(screen, LIGHT_GRAY, botao_case2, 2, border_radius=15)
        texto2 = font.render("Elevador", True, WHITE)
    
    # Adiciona ícones ou símbolos aos botões (simplificados)
    pygame.draw.circle(screen, LIGHT_PURPLE, (botao_case1.left + 40, botao_case1.centery), 15)  # Ícone para Máquina de Doce
    pygame.draw.rect(screen, LIGHT_PURPLE, (botao_case2.left + 25, botao_case2.centery - 15, 30, 30), border_radius=5)  # Ícone para Elevador
    
    # Posiciona os textos nos botões
    screen.blit(texto1, (botao_case1.centerx - texto1.get_width()//2 + 10, botao_case1.centery - texto1.get_height()//2))
    screen.blit(texto2, (botao_case2.centerx - texto2.get_width()//2 + 10, botao_case2.centery - texto2.get_height()//2))
    
    # Desenha créditos na parte inferior da tela
    creditos = font.render("© 2025 - Automatos", True, WHITE)
    screen.blit(creditos, (WIDTH//2 - creditos.get_width()//2, HEIGHT - 50))
    
    pygame.display.flip()
    return botao_case1, botao_case2

# Funções dos casos
def executar_case1():
    try:
        subprocess.run([sys.executable, "MaquinaDeDoces.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar Case 1: {e}")

def executar_case2():
    try:
        subprocess.run([sys.executable, "Elevador.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar Case 2: {e}")

# Loop do menu
rodando = True
while rodando:
    clock.tick(60)  # Limita a 60 FPS
    botoes = desenhar_menu()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if botoes[0].collidepoint(event.pos):
                executar_case1()
            elif botoes[1].collidepoint(event.pos):
                executar_case2()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False

pygame.quit()
sys.exit()
