import pygame
import sys

pygame.init()

# Cores
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)
STEEL = (160, 160, 170)

# Tela
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Elevador")

# Fonte
font = pygame.font.SysFont("arial", 24)
large_font = pygame.font.SysFont("arial", 40, bold=True)

# Estados
andar_atual = 0
portas_abertas = False
mensagem = ""
NUM_ANDARES = 4
ANDAR_ALTURA = 150
luzes_chamada = {i: False for i in range(NUM_ANDARES)}

# Elevador
elevador_width = 100
elevador_height = 100
elevador_x = WIDTH // 2 - elevador_width // 2
elevador_y = 0  # será posicionado com y_do_andar

elevador = pygame.Rect(elevador_x, 0, elevador_width, elevador_height)

# Portas
porta_esquerda = pygame.Rect(elevador.left, elevador.top, elevador_width // 2, elevador_height)
porta_direita = pygame.Rect(elevador.left + elevador_width // 2, elevador.top, elevador_width // 2, elevador_height)

# Centralizar o elevador quando chega no andar
def y_do_andar(andar):
    topo_bloco = HEIGHT - (andar + 1) * ANDAR_ALTURA
    return topo_bloco + (ANDAR_ALTURA - elevador_height) // 2

# Desenhar elevador 
def desenhar_elevador():
    # Elevador
    pygame.draw.rect(screen, (60, 60, 60), elevador.inflate(10, 10), border_radius=10)
    pygame.draw.rect(screen, (180, 180, 200), elevador, border_radius=10)
    pygame.draw.line(screen, (100, 100, 120), (elevador.centerx, elevador.top), (elevador.centerx, elevador.bottom), 3)

    # Painel do elevador
    painel = pygame.Rect(elevador.right - 15, elevador.top + 20, 10, 60)
    pygame.draw.rect(screen, (100, 100, 100), painel, border_radius=4)
    pygame.draw.circle(screen, RED, painel.center, 4)

    # Desenho das portas se fechadas
    if not portas_abertas:
        pygame.draw.rect(screen, STEEL, porta_esquerda)
        pygame.draw.rect(screen, STEEL, porta_direita)

# Desenhar tela completa
def desenhar_tela(highlight_botao=None):
    screen.fill(WHITE)

    for i in range(NUM_ANDARES):
        y = y_do_andar(i)
        bloco = pygame.Rect(80, y - (ANDAR_ALTURA // 2 - elevador_height // 2), WIDTH - 160, ANDAR_ALTURA)

        cor_bloco = (200, 220, 255) if i == andar_atual else (255, 255, 180) if luzes_chamada[i] else GRAY
        pygame.draw.rect(screen, cor_bloco, bloco, border_radius=8)
        pygame.draw.rect(screen, BLACK, bloco, 2, border_radius=8)

        for linha in range(10, ANDAR_ALTURA, 15):
            pygame.draw.line(screen, DARK_GRAY, (bloco.left + 10, y - (ANDAR_ALTURA // 2 - elevador_height // 2) + linha), (bloco.right - 10, y - (ANDAR_ALTURA // 2 - elevador_height // 2) + linha), 1)
        pygame.draw.line(screen, DARK_GRAY, (bloco.left, y - (ANDAR_ALTURA // 2 - elevador_height // 2)), (bloco.right, y - (ANDAR_ALTURA // 2 - elevador_height // 2)), 5)

        placa = pygame.Rect(bloco.left - 60, y - 15, 50, 30)
        pygame.draw.rect(screen, BLACK, placa, border_radius=6)
        texto_placa = font.render(str(i), True, GREEN)
        screen.blit(texto_placa, (placa.centerx - texto_placa.get_width() // 2, placa.centery - texto_placa.get_height() // 2))

        cor_luz = YELLOW if luzes_chamada[i] else DARK_GRAY
        pygame.draw.circle(screen, cor_luz, (bloco.right - 20, y - 40), 10)

    desenhar_elevador()

    for i in range(NUM_ANDARES):
        botao = pygame.Rect(50 + i * 130, 20, 100, 50)
        sombra = pygame.Rect(botao.x + 2, botao.y + 2, botao.width, botao.height)
        cor = YELLOW if highlight_botao == i else (230, 230, 230)
        pygame.draw.rect(screen, DARK_GRAY, sombra, border_radius=12)
        pygame.draw.rect(screen, cor, botao, border_radius=12)
        pygame.draw.rect(screen, BLACK, botao, 2, border_radius=12)

        txt = font.render(str(i), True, BLACK)
        screen.blit(txt, (botao.centerx - txt.get_width() // 2, botao.centery - txt.get_height() // 2))

    if mensagem:
        status_texto = f"{mensagem} - {'Portas Abertas' if portas_abertas else 'Portas Fechadas'}"
        status_render = font.render(status_texto, True, BLACK)
        screen.blit(status_render, (WIDTH // 2 - status_render.get_width() // 2, 85))

    pygame.display.flip()

# Easing para suavidade
def ease_in_out(t):
    return t * t * (3 - 2 * t)

# Animação das portas 
def abrir_portas():
    global portas_abertas
    for i in range(30):  # Aumentando o número de quadros para suavizar mais o movimento
        fator = ease_in_out(i / 30)
        porta_esquerda.width = max(0, elevador_width // 2 - int(fator * (elevador_width // 2)))
        porta_direita.x = elevador.left + elevador_width // 2 + int(fator * (elevador_width // 2))
        porta_direita.width = max(0, elevador_width // 2 - int(fator * (elevador_width // 2)))
        desenhar_tela()
        pygame.time.delay(12)
    portas_abertas = True

def fechar_portas():
    global portas_abertas
    for i in range(50):  # Aumentando o número de quadros para suavizar ainda mais
        fator = ease_in_out(i / 50)
        porta_esquerda.width = int(fator * (elevador_width // 2))
        porta_direita.x = elevador.left + elevador_width // 2 + (elevador_width // 2 - int(fator * (elevador_width // 2)))
        porta_direita.width = int(fator * (elevador_width // 2))
        desenhar_tela()
        pygame.time.delay(12)
    portas_abertas = False

# Movimento do elevador 
def mover_para(destino):
    global andar_atual, mensagem, portas_abertas

    if destino == andar_atual:
        mensagem = f"Já estamos no andar {andar_atual}"
        abrir_portas()
        return

    luzes_chamada[destino] = True
    mensagem = f"Indo para o andar {destino}"
    fechar_portas()  # Fechar as portas suavemente antes de mover

    start_y = elevador.y
    target_y = y_do_andar(destino)
    distancia = target_y - start_y
    duracao = 1.5
    frames = int(duracao * 60)

    for frame in range(frames):
        t = min(1, frame / frames)
        eased_t = ease_in_out(t)
        elevador.y = int(start_y + eased_t * distancia)
        porta_esquerda.y = elevador.y
        porta_direita.y = elevador.y
        desenhar_tela()
        pygame.time.delay(1000 // 60)

    andar_atual = destino
    mensagem = f"Chegou no andar {andar_atual}"
    luzes_chamada[andar_atual] = False
    abrir_portas()  # Abrir as portas suavemente ao chegar

# Início no andar 0 centralizado
elevador.y = y_do_andar(0)
porta_esquerda.y = elevador.y
porta_direita.y = elevador.y

# Loop principal
clock = pygame.time.Clock()
rodando = True

while rodando:
    mouse_hover = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i in range(NUM_ANDARES):
                if pygame.Rect(50 + i * 130, 20, 100, 50).collidepoint(x, y):
                    mover_para(i)
        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            for i in range(NUM_ANDARES):
                if pygame.Rect(50 + i * 130, 20, 100, 50).collidepoint(mx, my):
                    mouse_hover = i

    desenhar_tela(mouse_hover)
    clock.tick(60)

pygame.quit()
sys.exit()