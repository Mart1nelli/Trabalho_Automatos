import pygame
import sys
import math

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
em_movimento = False

# Partículas para efeitos visuais
particulas = []

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

# Funções de easing mais avançadas
def ease_in_out_cubic(t):
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2

def ease_in_out_bounce(t):
    if t < 0.5:
        return (1 - bounce_out(1 - 2 * t)) / 2
    else:
        return (1 + bounce_out(2 * t - 1)) / 2

def bounce_out(t):
    n1 = 7.5625
    d1 = 2.75
    
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375

def ease_elastic(t):
    if t == 0 or t == 1:
        return t
    return pow(2, -10 * t) * math.sin((t - 0.075) * (2 * math.pi) / 0.3) + 1

# Sistema de partículas
def criar_particula(x, y, cor, velocidade, duracao, tamanho=3):
    return {
        'x': x,
        'y': y,
        'cor': cor,
        'vx': velocidade[0],
        'vy': velocidade[1],
        'duracao': duracao,
        'tempo': 0,
        'tamanho': tamanho
    }

def atualizar_particulas(delta_time):
    global particulas
    for p in particulas:
        p['tempo'] += delta_time
        p['x'] += p['vx'] * delta_time
        p['y'] += p['vy'] * delta_time
        p['vy'] += 0.2 * delta_time  # Gravidade
    
    # Remover partículas expiradas
    particulas = [p for p in particulas if p['tempo'] < p['duracao']]

def desenhar_particulas():
    for p in particulas:
        # Calcular opacidade baseada no tempo restante
        opacidade = 255 * (1 - p['tempo'] / p['duracao'])
        cor = list(p['cor'])
        if len(cor) == 3:
            cor.append(int(opacidade))
        else:
            cor[3] = int(opacidade)
        
        # Diminuir tamanho com o tempo
        tamanho = p['tamanho'] * (1 - p['tempo'] / p['duracao'])
        
        # Desenhar partícula
        pygame.draw.circle(
            screen, 
            cor, 
            (int(p['x']), int(p['y'])), 
            max(1, int(tamanho))
        )

# Efeito de chegada do elevador
def efeito_chegada():
    for _ in range(15):
        x = elevador.centerx + random.randint(-elevador_width//2, elevador_width//2)
        y = elevador.bottom - 5
        velocidade = (random.uniform(-0.5, 0.5), random.uniform(-2, -0.5))
        cor = random.choice([(255, 255, 150, 200), (255, 230, 150, 200)])
        particulas.append(criar_particula(x, y, cor, velocidade, random.uniform(0.5, 1.5), random.uniform(2, 4)))

# Efeito de partida do elevador
def efeito_partida():
    for _ in range(15):
        x = elevador.centerx + random.randint(-elevador_width//2, elevador_width//2)
        y = elevador.bottom
        velocidade = (random.uniform(-0.3, 0.3), random.uniform(0.5, 2))
        cor = random.choice([(150, 150, 180, 200), (200, 200, 220, 200)])
        particulas.append(criar_particula(x, y, cor, velocidade, random.uniform(0.5, 1.5), random.uniform(2, 4)))

# Efeito de botão pressionado
def efeito_botao(botao_idx):
    centro_x = 50 + botao_idx * 130 + 50  # Centro do botão
    centro_y = 45  # Centro do botão
    for _ in range(20):
        angulo = random.uniform(0, 2 * math.pi)
        distancia = random.uniform(0, 20)
        x = centro_x + math.cos(angulo) * distancia
        y = centro_y + math.sin(angulo) * distancia
        velocidade = (math.cos(angulo) * random.uniform(0.5, 2), 
                      math.sin(angulo) * random.uniform(0.5, 2))
        cor = (255, 215, 0, 200)  # Amarelo com transparência
        particulas.append(criar_particula(x, y, cor, velocidade, random.uniform(0.5, 1.2), random.uniform(2, 4)))

# Desenhar elevador com sombras e reflexos
def desenhar_elevador():
    # Sombra do elevador
    sombra = elevador.inflate(20, 10).move(5, 5)
    pygame.draw.rect(screen, (30, 30, 30, 100), sombra, border_radius=10)
    
    # Estrutura base do elevador
    pygame.draw.rect(screen, (60, 60, 60), elevador.inflate(10, 10), border_radius=10)
    
    # Brilho/reflexo gradual na parte superior
    for i in range(10):
        reflexo_y = elevador.top + i
        opacidade = 150 - i * 10
        pygame.draw.line(
            screen, 
            (220, 220, 230, opacidade), 
            (elevador.left + 5, reflexo_y), 
            (elevador.right - 5, reflexo_y), 
            1
        )
    
    # Corpo principal do elevador
    pygame.draw.rect(screen, (180, 180, 200), elevador, border_radius=10)
    
    # Linha central
    pygame.draw.line(screen, (100, 100, 120), (elevador.centerx, elevador.top + 5), 
                     (elevador.centerx, elevador.bottom - 5), 3)
    
    # Painel do elevador com LED
    painel = pygame.Rect(elevador.right - 15, elevador.top + 20, 10, 60)
    pygame.draw.rect(screen, (100, 100, 100), painel, border_radius=4)
    
    # LED piscante quando em movimento
    if em_movimento:
        led_cor = RED if pygame.time.get_ticks() % 1000 < 500 else (100, 0, 0)
    else:
        led_cor = GREEN if portas_abertas else YELLOW
    
    # Desenho do LED com brilho
    pygame.draw.circle(screen, led_cor, painel.center, 4)
    pygame.draw.circle(screen, (255, 255, 255, 100), 
                      (painel.center[0]-1, painel.center[1]-1), 1)
    
    # Desenho das portas com gradiente se fechadas
    if not portas_abertas:
        # Porta esquerda com gradiente
        for i in range(porta_esquerda.width):
            shade = 160 + int(20 * i / porta_esquerda.width)
            pygame.draw.line(
                screen, 
                (shade, shade, shade+10), 
                (porta_esquerda.left + i, porta_esquerda.top), 
                (porta_esquerda.left + i, porta_esquerda.bottom), 
                1
            )
        
        # Porta direita com gradiente
        for i in range(porta_direita.width):
            shade = 180 - int(20 * i / porta_direita.width)
            pygame.draw.line(
                screen, 
                (shade, shade, shade+10), 
                (porta_direita.left + i, porta_direita.top), 
                (porta_direita.left + i, porta_direita.bottom), 
                1
            )
        
        # Bordas das portas
        pygame.draw.rect(screen, (100, 100, 110), porta_esquerda, 1, border_radius=3)
        pygame.draw.rect(screen, (100, 100, 110), porta_direita, 1, border_radius=3)

# Desenhar andar com efeitos visuais
def desenhar_andar(i, highlight=False):
    y = y_do_andar(i)
    bloco = pygame.Rect(80, y - (ANDAR_ALTURA // 2 - elevador_height // 2), WIDTH - 160, ANDAR_ALTURA)
    
    # Cor base do andar
    cor_base = (200, 220, 255) if i == andar_atual else (255, 255, 180) if luzes_chamada[i] else GRAY
    
    # Efeito pulsante para andar atual ou chamado
    pulse = 0
    if i == andar_atual or luzes_chamada[i]:
        pulse = math.sin(pygame.time.get_ticks() * 0.003) * 15
        cor_base = (
            min(255, cor_base[0] + int(pulse)),
            min(255, cor_base[1] + int(pulse)),
            min(255, cor_base[2])
        )
    
    # Desenhar andar com gradiente
    pygame.draw.rect(screen, cor_base, bloco, border_radius=8)
    
    # Linhas de piso com profundidade
    for linha in range(10, ANDAR_ALTURA, 15):
        opacidade = 100 + (linha % 50)  # Variação de opacidade para efeito 3D
        cor_linha = (DARK_GRAY[0], DARK_GRAY[1], DARK_GRAY[2], opacidade)
        pygame.draw.line(
            screen, 
            cor_linha, 
            (bloco.left + 10, y - (ANDAR_ALTURA // 2 - elevador_height // 2) + linha), 
            (bloco.right - 10, y - (ANDAR_ALTURA // 2 - elevador_height // 2) + linha), 
            1
        )
    
    # Linha principal do andar
    pygame.draw.line(
        screen, 
        DARK_GRAY, 
        (bloco.left, y - (ANDAR_ALTURA // 2 - elevador_height // 2)), 
        (bloco.right, y - (ANDAR_ALTURA // 2 - elevador_height // 2)), 
        5
    )
    
    # Bordas do andar
    pygame.draw.rect(screen, BLACK, bloco, 2, border_radius=8)
    
    # Placa do andar com reflexo
    placa = pygame.Rect(bloco.left - 60, y - 15, 50, 30)
    pygame.draw.rect(screen, BLACK, placa, border_radius=6)
    
    # Reflexo na placa
    reflexo = pygame.Rect(placa.left + 2, placa.top + 2, placa.width - 4, 5)
    pygame.draw.rect(screen, (70, 70, 70), reflexo, border_radius=3)
    
    # Número do andar
    texto_placa = font.render(str(i), True, GREEN)
    screen.blit(texto_placa, (placa.centerx - texto_placa.get_width() // 2, placa.centery - texto_placa.get_height() // 2))
    
    # Luz de chamada com brilho
    cor_luz = YELLOW if luzes_chamada[i] else DARK_GRAY
    
    # Brilho externo da luz
    if luzes_chamada[i]:
        # Efeito pulsante
        tamanho_brilho = 15 + int(math.sin(pygame.time.get_ticks() * 0.01) * 5)
        pygame.draw.circle(
            screen, 
            (255, 255, 100, 50), 
            (bloco.right - 20, y - 40), 
            tamanho_brilho
        )
    
    # Luz principal
    pygame.draw.circle(screen, cor_luz, (bloco.right - 20, y - 40), 10)
    
    # Reflexo na luz
    pygame.draw.circle(
        screen, 
        (255, 255, 255, 150), 
        (bloco.right - 23, y - 43), 
        3
    )

# Desenhar tela completa com efeitos
def desenhar_tela(highlight_botao=None):
    screen.fill(WHITE)
    
    # Desenhar andares
    for i in range(NUM_ANDARES):
        desenhar_andar(i, i == highlight_botao)
    
    # Desenhar elevador
    desenhar_elevador()
    
    # Desenhar botões com efeitos
    for i in range(NUM_ANDARES):
        botao = pygame.Rect(50 + i * 130, 20, 100, 50)
        sombra = pygame.Rect(botao.x + 5, botao.y + 5, botao.width, botao.height)
        
        # Sombra do botão
        pygame.draw.rect(screen, (50, 50, 50, 100), sombra, border_radius=12)
        
        # Cor principal do botão
        cor = YELLOW if highlight_botao == i else (230, 230, 230)
        
        # Efeito quando está sendo chamado
        if luzes_chamada[i] and not (i == andar_atual and portas_abertas):
            pulse = math.sin(pygame.time.get_ticks() * 0.01) * 25
            cor = (
                min(255, cor[0] + int(pulse)),
                min(255, cor[1]),
                min(255, 50 + int(pulse))
            )
        
        # Desenhar botão com gradiente
        pygame.draw.rect(screen, cor, botao, border_radius=12)
        
        # Adicionar reflexo superior
        reflexo = pygame.Rect(botao.x + 5, botao.y + 5, botao.width - 10, 10)
        pygame.draw.rect(screen, (255, 255, 255, 150), reflexo, border_radius=6)
        
        # Borda do botão
        pygame.draw.rect(screen, BLACK, botao, 2, border_radius=12)
        
        # Texto do botão
        txt = font.render(str(i), True, BLACK)
        screen.blit(txt, (botao.centerx - txt.get_width() // 2, botao.centery - txt.get_height() // 2))
    
    # Mensagens com efeito de digitação
    if mensagem:
        status_texto = f"{mensagem} - {'Portas Abertas' if portas_abertas else 'Portas Fechadas'}"
        status_render = font.render(status_texto, True, BLACK)
        
        # Sombra do texto
        sombra_render = font.render(status_texto, True, (100, 100, 100))
        screen.blit(sombra_render, (WIDTH // 2 - status_render.get_width() // 2 + 2, 87))
        
        # Texto principal
        screen.blit(status_render, (WIDTH // 2 - status_render.get_width() // 2, 85))
    
    # Desenhar partículas por cima de tudo
    desenhar_particulas()
    
    pygame.display.flip()

# Animação das portas com física
def abrir_portas():
    global portas_abertas
    
    # Som de porta abrindo (simulado com partículas)
    for _ in range(5):
        x = elevador.centerx
        y = elevador.centery
        particulas.append(criar_particula(
            x, y, 
            (220, 220, 250, 150), 
            (random.uniform(-1, 1), random.uniform(-1, 1)), 
            0.5, 
            2
        ))
    
    frames = 40
    for i in range(frames):
        # Usar ease_elastic para dar sensação de movimento mecânico
        fator = ease_elastic(i / frames)
        porta_esquerda.width = max(0, elevador_width // 2 - int(fator * (elevador_width // 2)))
        porta_direita.x = elevador.left + elevador_width // 2 + int(fator * (elevador_width // 2))
        porta_direita.width = max(0, elevador_width // 2 - int(fator * (elevador_width // 2)))
        
        # Adicionar partículas nas bordas das portas
        if i % 5 == 0:
            particulas.append(criar_particula(
                porta_esquerda.right, 
                porta_esquerda.centery + random.randint(-40, 40), 
                (200, 200, 220, 150), 
                (random.uniform(0.1, 0.5), random.uniform(-0.2, 0.2)), 
                0.3
            ))
            particulas.append(criar_particula(
                porta_direita.left, 
                porta_direita.centery + random.randint(-40, 40), 
                (200, 200, 220, 150), 
                (random.uniform(-0.5, -0.1), random.uniform(-0.2, 0.2)), 
                0.3
            ))
        
        # Atualizar partículas
        atualizar_particulas(1/60)
        desenhar_tela()
        pygame.time.delay(10)
    
    portas_abertas = True

def fechar_portas():
    global portas_abertas
    
    frames = 50
    for i in range(frames):
        # Usar bounce para dar impressão de portas se fechando com um baque
        fator = ease_in_out_bounce(i / frames)
        porta_esquerda.width = int(fator * (elevador_width // 2))
        porta_direita.x = elevador.left + elevador_width // 2 + (elevador_width // 2 - int(fator * (elevador_width // 2)))
        porta_direita.width = int(fator * (elevador_width // 2))
        
        # Efeito de colisão no final
        if i > frames - 5:
            particulas.append(criar_particula(
                elevador.centerx, 
                elevador.centery + random.randint(-40, 40), 
                (180, 180, 180, 100), 
                (random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3)), 
                0.5
            ))
        
        # Atualizar partículas
        atualizar_particulas(1/60)
        desenhar_tela()
        pygame.time.delay(10)
    
    # Som de porta fechando (simulado com partículas)
    for _ in range(10):
        x = elevador.centerx
        y = elevador.centery
        particulas.append(criar_particula(
            x, y, 
            (150, 150, 180, 200), 
            (random.uniform(-2, 2), random.uniform(-2, 2)), 
            0.7, 
            3
        ))
    
    portas_abertas = False

# Movimento do elevador com física e camera shake
def mover_para(destino):
    global andar_atual, mensagem, portas_abertas, em_movimento
    
    if destino == andar_atual:
        mensagem = f"Já estamos no andar {andar_atual}"
        abrir_portas()
        return
    
    # Ativar luz de chamada
    luzes_chamada[destino] = True
    mensagem = f"Indo para o andar {destino}"
    fechar_portas()  # Fechar as portas suavemente antes de mover
    
    # Efeito de partida
    efeito_partida()
    em_movimento = True
    
    # Movimento com física
    start_y = elevador.y
    target_y = y_do_andar(destino)
    distancia = target_y - start_y
    duracao = 2.0
    frames = int(duracao * 60)
    
    # Definir direção (subindo ou descendo)
    subindo = target_y < start_y
    
    # Simulação de aceleração e desaceleração
    for frame in range(frames):
        t = min(1, frame / frames)
        
        # Easing cubic para movimento mais natural
        eased_t = ease_in_out_cubic(t)
        elevador.y = int(start_y + eased_t * distancia)
        porta_esquerda.y = elevador.y
        porta_direita.y = elevador.y
        
        # Efeito de camera shake no início e no fim do movimento
        shake = 0
        if frame < frames * 0.1 or frame > frames * 0.9:
            shake = random.randint(-2, 2)
            elevador.x = elevador_x + shake
            porta_esquerda.x = elevador.x
            porta_direita.x = elevador.x + porta_esquerda.width
        
        # Partículas de movimento
        if frame % 10 == 0:
            if subindo:
                # Partículas caindo quando subindo
                particulas.append(criar_particula(
                    elevador.centerx + random.randint(-40, 40), 
                    elevador.bottom + 10, 
                    (150, 150, 200, 150), 
                    (random.uniform(-0.2, 0.2), random.uniform(1, 3)), 
                    1.0
                ))
            else:
                # Partículas subindo quando descendo
                particulas.append(criar_particula(
                    elevador.centerx + random.randint(-40, 40), 
                    elevador.top - 10, 
                    (150, 150, 200, 150), 
                    (random.uniform(-0.2, 0.2), random.uniform(-3, -1)), 
                    1.0
                ))
        
        # Atualizar partículas
        atualizar_particulas(1/60)
        desenhar_tela()
        pygame.time.delay(1000 // 60)
    
    # Resetar posição do elevador após o shake
    elevador.x = elevador_x
    porta_esquerda.x = elevador.x
    porta_direita.x = elevador.x + porta_esquerda.width
    
    andar_atual = destino
    mensagem = f"Chegou no andar {andar_atual}"
    luzes_chamada[andar_atual] = False
    em_movimento = False
    
    # Efeito de chegada
    efeito_chegada()
    abrir_portas()  # Abrir as portas suavemente ao chegar

# Inicialização
import random
elevador.y = y_do_andar(0)
porta_esquerda.y = elevador.y
porta_direita.y = elevador.y

# Abrir portas na inicialização
portas_abertas = True
porta_esquerda.width = 0
porta_direita.x = elevador.right
porta_direita.width = 0

# Loop principal
clock = pygame.time.Clock()
rodando = True
ultimo_tempo = pygame.time.get_ticks() / 1000.0

while rodando:
    mouse_hover = None
    
    # Calcular delta time para animações consistentes
    tempo_atual = pygame.time.get_ticks() / 1000.0
    delta_time = tempo_atual - ultimo_tempo
    ultimo_tempo = tempo_atual
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i in range(NUM_ANDARES):
                botao = pygame.Rect(50 + i * 130, 20, 100, 50)
                if botao.collidepoint(x, y) and not em_movimento:
                    efeito_botao(i)
                    mover_para(i)
        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            for i in range(NUM_ANDARES):
                if pygame.Rect(50 + i * 130, 20, 100, 50).collidepoint(mx, my):
                    mouse_hover = i
    
    # Atualizar partículas
    atualizar_particulas(delta_time)
    
    # Adicionar partículas ambientais ocasionalmente
    if random.random() < delta_time * 0.5:  # ~50% de chance por segundo
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        particulas.append(criar_particula(
            x, y, 
            (255, 255, 255, 50), 
            (random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)), 
            random.uniform(1, 2), 
            random.uniform(1, 2)
        ))
    
    desenhar_tela(mouse_hover)
    clock.tick(60)

pygame.quit()
sys.exit()