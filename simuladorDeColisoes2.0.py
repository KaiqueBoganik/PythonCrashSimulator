import pygame
import random
import math

LARGURADAJANELA = 500
ALTURADAJANELA = 500
RAIODASBOLAS = 20
NUMERODEBOLAS = 50
VELOCIDADEDASBOLA = 100

pygame.init()
tela = pygame.display.set_mode((LARGURADAJANELA, ALTURADAJANELA))
tempo = pygame.time.Clock()

class Bola:
    def __init__(self, posX, posY, velocidadeX, velocidadeY, cor):
        self.x = posX
        self.y = posY
        self.vx = velocidadeX
        self.vy = velocidadeY
        self.cor = cor

    def mover(self, deltaTempo):
        self.x += self.vx * deltaTempo
        self.y += self.vy * deltaTempo

    def verificarBordas(self):
        if self.x - RAIODASBOLAS < 0:
            self.x = RAIODASBOLAS
            self.vx *= -1
        elif self.x + RAIODASBOLAS > LARGURADAJANELA:
            self.x = LARGURADAJANELA - RAIODASBOLAS
            self.vx *= -1

        if self.y - RAIODASBOLAS < 0:
            self.y = RAIODASBOLAS
            self.vy *= -1
        elif self.y + RAIODASBOLAS > ALTURADAJANELA:
            self.y = ALTURADAJANELA - RAIODASBOLAS
            self.vy *= -1

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), RAIODASBOLAS)


def criarBolas():
    return [
        Bola(
            random.randint(RAIODASBOLAS, LARGURADAJANELA - RAIODASBOLAS),
            random.randint(RAIODASBOLAS, ALTURADAJANELA - RAIODASBOLAS),
            random.uniform(-VELOCIDADEDASBOLA, VELOCIDADEDASBOLA),
            random.uniform(-VELOCIDADEDASBOLA, VELOCIDADEDASBOLA),
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )
        for _ in range(NUMERODEBOLAS)
    ]


def checarColisao(bola1, bola2):
    distX = bola1.x - bola2.x
    distY = bola1.y - bola2.y
    distancia = math.hypot(distX, distY)
    return distancia < 2 * RAIODASBOLAS


def processarColisao(bola1, bola2):
    distX = bola1.x - bola2.x
    distY = bola1.y - bola2.y
    distancia = math.hypot(distX, distY)
    if distancia == 0:
        distancia = 0.01

    normalX = distX / distancia
    normalY = distY / distancia

    sobreposicao = 2 * RAIODASBOLAS - distancia
    bola1.x += normalX * sobreposicao / 2
    bola1.y += normalY * sobreposicao / 2
    bola2.x -= normalX * sobreposicao / 2
    bola2.y -= normalY * sobreposicao / 2

    impulso = 2 * (
        bola1.vx * normalX + bola1.vy * normalY -
        bola2.vx * normalX - bola2.vy * normalY
    ) / 2
    bola1.vx -= impulso * normalX
    bola1.vy -= impulso * normalY
    bola2.vx += impulso * normalX
    bola2.vy += impulso * normalY


def atualizarBolas(bolas, deltaTempo):
    for i, bola1 in enumerate(bolas):
        bola1.mover(deltaTempo)
        bola1.verificarBordas()
        for bola2 in bolas[i + 1:]:
            if checarColisao(bola1, bola2):
                processarColisao(bola1, bola2)


def desenharBolas(bolas, tela):
    tela.fill((255, 255, 255))
    for bola in bolas:
        bola.desenhar(tela)
    pygame.display.flip()


def main():
    bolas = criarBolas()
    executando = True

    while executando:
        deltaTempo = tempo.tick(60) / 1000.0
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        atualizarBolas(bolas, deltaTempo)
        desenharBolas(bolas, tela)

    pygame.quit()


if __name__ == "__main__":
    main()