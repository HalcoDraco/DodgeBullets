import pygame
from consts import *
from player import Player
from bullet import Bullet
from logic import tryMove, shootPlayer
from vec import Vec

tickCounter = 0

bullets = {}
players = {}

player1 = Player(Vec(200, 200))
player2 = Player(Vec(800, 800))
player3 = Player(Vec(200, 800))
player4 = Player(Vec(800, 200))

player0 = Player(Vec(350, 150))

players[player0.id] = player0
players[player1.id] = player1
players[player2.id] = player2
players[player3.id] = player3
players[player4.id] = player4

id_main_player = player0.id

pygame.init()

win = pygame.display.set_mode((map_size, map_size))
pygame.display.set_caption("The game")

clock = pygame.time.Clock()

def dir_center(player):
    return Vec(map_size/2, map_size/2) - player.pos - Vec(1, 11)

def update():
    for player in players.values():
        player.move(player_speed)
        if player.id == id_main_player:
            player.dir = tryMove(player, dir_center(player), bullets)
        else:
            shootPlayer(player, id_main_player, players, bullets, tickCounter)
    
    delids = []
    for bullet in bullets.values():
        if bullet.pos.outside(2):
            delids.append(bullet.id)
            continue
        bullet.move(bullet_speed)
    for id in delids:
        del bullets[id]
    
def draw():
    update()

    win.fill((0, 0, 0))

    for player in players.values():
        if player.id == id_main_player:
            pygame.draw.circle(win, (0, 255, 0), (int(player.pos.x), int(player.pos.y)), player_radius)
        else:
            pygame.draw.circle(win, (255, 0, 0), (int(player.pos.x), int(player.pos.y)), player_radius)
    
    for bullet in bullets.values():
        pygame.draw.circle(win, (255, 255, 255), (int(bullet.pos.x), int(bullet.pos.y)), bullet_radius)

run = True
while run:
    clock.tick(ticksPS)
    tickCounter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    
    draw()

    pygame.display.update()