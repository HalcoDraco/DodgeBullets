import pygame
from values import *
from player import Player
from bullet import Bullet
from logic import tryMove, shootPlayer
from vec import Vec

collisions = 0

player1 = Player(200, 200)
player2 = Player(800, 800)
player3 = Player(200, 800)
player4 = Player(800, 200)
player5 = Player(200, 500)
player6 = Player(800, 500)

player0 = Player(500, 500)

context.players[player0.id()] = player0
context.players[player1.id()] = player1
context.players[player2.id()] = player2
context.players[player3.id()] = player3
context.players[player4.id()] = player4
context.players[player5.id()] = player5
context.players[player6.id()] = player6

id_main_player = player0.id()

pygame.init()

win = pygame.display.set_mode((map_size_x, map_size_y))
pygame.display.set_caption("The game")

clock = pygame.time.Clock()

dirs = [Vec(1, 0), Vec(1, 1), Vec(0, 1), Vec(-1, 1), Vec(-1, 0), Vec(-1, -1), Vec(0, -1), Vec(1, -1)]
positions = [Vec(350, 350), Vec(350, 650), Vec(650, 650), Vec(650, 350)]

def update():
    for player in context.players.values():
        player.move(player_speed)
        if player.id() == id_main_player:

            player.set_direction(tryMove(player, dirs[(int(context.tickCounter/40)%8)]))
        else:
            shootPlayer(player, id_main_player)
    
    delids = []
    for bullet in context.bullets.values():
        if bullet.outside_map(bullet_radius):
            delids.append(bullet.id())
            continue
        bullet.move(bullet_speed)
    for id in delids:
        del (context.bullets)[id]

    global collisions
    #check for collisions
    for bullet in context.bullets.values():   
        player = context.players[id_main_player]
        if player.pos().distance(bullet.pos()) < player_radius + bullet_radius:
            collisions += 1
            print("Collisions: " + str(collisions))

    
def draw():
    update()

    win.fill((0, 0, 0))

    for player in context.players.values():
        if player.id() == id_main_player:
            pygame.draw.circle(win, (0, 255, 0), (int(player.pos().x()), int(player.pos().y())), player_radius)
        else:
            pygame.draw.circle(win, (255, 0, 0), (int(player.pos().x()), int(player.pos().y())), player_radius)
    
    for bullet in context.bullets.values():
        pygame.draw.circle(win, (255, 255, 255), (int(bullet.pos().x()), int(bullet.pos().y())), bullet_radius)


run = True
while run:

    clock.tick(ticksPS)
    context.tickCounter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    
    draw()

    pygame.display.update()