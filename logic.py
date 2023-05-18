from values import *
from vec import Vec
from line3d import Line3d
from math import pi, radians as rad, sqrt

import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def plot3d(lines, tline):
    plotline_bullet_alt = max(map_size_x, map_size_y)*ticksPS/bullet_speed
    ax.clear()
    for line in lines:
        line_points = tuple(zip(line.point(), line.get_point_from_value(plotline_bullet_alt)))
        ax.plot(*line_points, color='r')

    line_points = tuple(zip(tline.point(), tline.get_point_from_value(plotline_bullet_alt*player_speed/bullet_speed)))
    ax.plot(*line_points, color='g')
    plt.pause(0.001)

def calcCost(tryLine, lines):
    cost = 0
    for line in lines:
        alti = tryLine.closestAltitude(line)
        if alti > 0:
            dist = tryLine.horizontalDistance(line, alti)      
            if dist < player_radius + bullet_radius + avoidance_distance:
                cost += 1/(alti**2)
    return cost

def tryAngle(player, dir, angle, costs, lines):
    for side in range(-1, 2, 2):
        df = dir.flattened()
        tryDir = df.rotated2d(angle*side)

        tryDir.normalize()
        tryDir = tryDir*player_speed
        tryDir.elevate(ticksPS)

        td = tryDirection(player, tryDir, costs, lines)
        if td == -1:
            continue
        elif td != None:
            return td

def tryDirection(player, tryDir, costs, lines):

    if (player.pos() + (tryDir.flattened().normalized()*(player_speed/ticksPS))).outside2d(player_radius, 0, map_size_x, 0, map_size_y):
        return -1

    tryLine = Line3d(*(player.pos().get_coords()), *(tryDir.get_coords()))
    cost = calcCost(tryLine, lines)
    tryDir.flatten()
    if cost == 0:
        return tryDir
    costs.append((cost, tryDir))

def tryMove(player, dir):
    
    nearBullets = player.closeBullets(playerViewRadius) 
    lines = set()
    costs = []

    #lines creation
    for bllt in nearBullets.values():
        lineDirection = bllt.dir()
        lineDirection.normalize()
        lineDirection = lineDirection*bullet_speed
        lineDirection.elevate(ticksPS)
        lines.add(Line3d(*(bllt.pos().get_coords()), *(lineDirection.get_coords())))

    direc = dir.normalized()*player_speed
    plot3d(lines, Line3d(*(player.pos().get_coords()), *(direc.elevated(ticksPS).get_coords())))

    dir.normalize()
    for a in range(0, 179, circular_step):
        if a >= 30 and a < 30+circular_step:
            result = tryDirection(player, Vec(0, 0, 1), costs, lines)
            if result != None and result != -1:
                return result

        angle = rad(a)
        result = tryAngle(player, dir, angle, costs, lines)
        if result != None:
            return result
    
    minCost, minDir = costs[0][0], costs[0][1]
    for c, d in costs:
        if c < minCost:
            minCost = c
            minDir = d
    
    minDir.flatten()
    minDir.normalize()
    
    return minDir

"""
def shootPlayer(player, targetId):
    target = context.players[targetId]
    player.shoot(player.direction_to(target))
"""


def shootPlayer(player, targetId):

    target = context.players[targetId]

    targetDirection = target.dir().normalized()
    targetDirection = targetDirection * player_speed #gives correct norm to match player speed

    directionToTarget = player.direction_to(target).normalized()
    directionToTarget = directionToTarget * sqrt(bullet_speed**2 - player_speed**2) 

    direction =  directionToTarget + targetDirection

    player.shoot(direction)

