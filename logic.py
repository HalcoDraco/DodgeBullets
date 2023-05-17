from consts import *
from vec import Vec
from line3d import Line3d
from math import pi, radians as rad, sqrt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

sizeline = map_size/4

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def plot3d(lines, tline):
    ax.clear()
    for line in lines:
        line.vector.normalize()
        ax.plot([line.point.x, (line.point + line.vector*sizeline).x], [-line.point.y, -(line.point + line.vector*sizeline).y], [line.point.z, (line.point + line.vector*sizeline).z], color='r')

    tline.vector.normalize()
    tline.vector = tline.vector*0.3
    ax.plot([tline.point.x, (tline.point + tline.vector*sizeline).x], [-tline.point.y, -(tline.point + tline.vector*sizeline).y], [tline.point.z, (tline.point + tline.vector*sizeline).z], color='g')
    plt.pause(0.001)
def plot2d(bullets, player):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for bullet in bullets:
        ax.plot([bullet.pos.x], [-bullet.pos.y], 'ro')

    ax.plot([player.pos.x], [-player.pos.y], 'go')
    plt.show()


def calcCost(player, tryLine, near, lines):
    cost = 0
    for i, line in enumerate(lines):
        alti = tryLine.closestAltitude(line)
        if alti > 0:
            dist = tryLine.horizontalDistance(line, alti)      
            if dist < player_radius + bullet_radius+2:
                cost -= alti
    return cost

def tryAngle(player, dir, angle, costs, near, lines):
    for side in range(-1, 2, 2):
        tryDir = dir.rotation2d(angle*side)

        if (player.pos + (tryDir*(player_speed/ticksPS))).outside(player_radius):
            continue

        tryDir.normalize()
        tryDir = tryDir*player_speed
        tryDir.z = ticksPS
        tryLine = Line3d(player.pos, tryDir)
        cost = calcCost(player, tryLine, near, lines)
        if cost == 0:
            tryDir.z = 0
            return tryDir
        costs.append((cost, Vec(tryDir.x, tryDir.y)))

def tryMove(player, dir, bList):
    
    near = player.nearBullets(playerViewRadius, bList) 
    #near = [b for b in near if player.mayCollide(b, 0)]
    lines = []

    #lines creation
    for ent in near:
        lineDirection = Vec(ent.dir.x, ent.dir.y)
        lineDirection.normalize()
        lineDirection = lineDirection*bullet_speed
        lineDirection.z = ticksPS
        lines.append(Line3d(ent.pos, lineDirection))
    
    #xdtryLine = Line3d(player.pos, Vec(0, 0, 1))
    #plot3d(lines, xdtryLine)

    costs = []
    #first part
    dir.normalize()
    for a in range(0, 60, circular_step):
        angle = rad(a)
        ret = tryAngle(player, dir, angle, costs, near, lines)
        if ret != None:
            return ret, True

    #middle
    tryDir = Vec(0, 0, 1)
    tryLine = Line3d(player.pos, tryDir)
    costNoMove = calcCost(player, tryLine, near, lines)
    if costNoMove == 0:
        tryDir.z = 0
        return tryDir, True
    
    #second part
    for a in range(60, 179, circular_step):
        angle = rad(a)
        ret = tryAngle(player, dir, angle, costs, near, lines)
        if ret != None:
            return ret,True
    
    
    costs.append((costNoMove, Vec(0, 0)))

    minCost, minDir = costs[0][0], costs[0][1]
    for c, d in costs:
        if c < minCost:
            minCost = c
            minDir = d
    
    print("a")
    minDir.normalize()
    minDir = minDir*player_speed
    minDir.z = ticksPS
    
    #plot2d(near, player)
    
    minDir.z = 0

    return minDir, False

targetPosition = Vec(0, 0)
previousTargetPosition = Vec(0, 0)

def shootPlayer(player, targetId, pList, bullets, tickCounter):
    global targetPosition, previousTargetPosition

    target = pList[targetId]
    targetPosition = target.pos

    targetDirection = (targetPosition - previousTargetPosition)
    targetDirection.normalize()

    directionToTarget = (targetPosition - player.pos)
    directionToTarget.normalize() 
    directionToTarget = directionToTarget * (sqrt((bullet_speed)**2 + ((1/16) * bullet_speed)))

    direction = directionToTarget + targetDirection

    player.shoot(direction, bullets, tickCounter)

    previousTargetPosition = targetPosition