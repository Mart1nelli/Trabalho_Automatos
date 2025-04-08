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
pygame.display.set_caption("Simulador de Elevador")

# Fonte
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 48)

# Estados
andar_atual = 0
portas_abertas = False
mensagem = ""

# Retângulos
elevador = pygame.Rect(WIDTH//2 - 50, HEIGHT - 150, 100, 100)

# Função para desenhar os andares e elevador
def desenhar_tela():
    screen.fill(WHITE)
    
    # Andares
    for i in range(4):
        y = HEIGHT - (i+1) * 150
        pygame.draw.line(screen, BLACK, (100, y), (500, y), 2)
        texto = font.render(f"Andar {i}", True, BLACK)
        screen.blit(texto, (20, y - 20))

    # Elevador
    pygame.draw.rect(screen, BLUE if not portas_abertas else GREEN, elevador)
    texto_porta = "Portas Abertas" if portas_abertas else "Portas Fechadas"
    status = font.render(texto_porta, True, BLACK)
    screen.blit(status, (WIDTH//2 - status.get_width()//2, HEIGHT - 50))

    # Botões
    for i in range(4):
        botao = pygame.Rect(50 + i*130, 650, 100, 50)
        pygame.draw.rect(screen, GRAY, botao)
        screen.blit(font.render(str(i), True, BLACK), (botao.x + 40, botao.y + 10))

    # Mensagem
    msg_render = font.render(mensagem, True, RED)
    screen.blit(msg_render, (WIDTH//2 - msg_render.get_width()//2, 720))

    pygame.display.flip()

# Função para mover o elevador
def mover_para(destino):
    global andar_atual, portas_abertas, mensagem

    if destino == andar_atual:
        mensagem = f"Já estamos no andar {andar_atual}"
        portas_abertas = True
        return

    # Fecha portas para iniciar movimento
    portas_abertas = False
    desenhar_tela()
    pygame.time.delay(1000)

    passo = -1 if destino < andar_atual else 1
    while andar_atual != destino:
        andar_atual += passo
        elevador.y = HEIGHT - (andar_atual+1) * 150
        desenhar_tela()
        pygame.time.delay(1000)

    # Abre portas ao chegar
    portas_abertas = True
    mensagem = f"Chegou no andar {andar_atual}"
    desenhar_tela()
    pygame.time.delay(1000)

# Loop principal
clock = pygame.time.Clock()
rodando = True

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i in range(4):
                if pygame.Rect(50 + i*130, 650, 100, 50).collidepoint(x, y):
                    mover_para(i)

    desenhar_tela()
    clock.tick(30)

pygame.quit()
sys.exit()
