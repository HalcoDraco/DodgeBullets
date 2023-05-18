# CONSTANTS
map_size_x = 1000 # px
map_size_y = 1000 # px

ticksPS = 30 # ticks per second

player_speed = 80 # px per second
bullet_speed = 2*player_speed # px per second

player_radius = 8 # px
bullet_radius = 2 # px

shootCooldown = 1400/player_speed # ticks
avoidance_distance = 4 # px of distance between player and bullet

circular_step = 3 # number of angles to use when trying to find a free spot
playerViewRadius = 400 # px

from context import Context
context = Context()
