#!/bin/python3
#!/usr/bin/env python3
# https://en.wikipedia.org/wiki/Shebang_(Unix)
"""Patrick Woltman
Tribute to John Horton Conway's "Game of Life" in python using pygame
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

------Rules of conway's game of life ------------------------------------------------

"0" = DEATH
"1" = LIFE

------Death------
If a living square is surrounded by empty squares then it will die of "LONELINESS"
If a living square is surrounded by 3 or more living squares it will die from "OVERCROWDING"

------LIFE------
If a dead square is surrounded by 3 living squares then it is "BORN"

------Resources used ---------------------------------------------------------------
    "Graphically beautiful youtube videos explaining Conway's game of life"
    https://www.youtube.com/watch?v=CgOcEZinQ2I&ab_channel=0524432
    https://www.youtube.com/watch?v=u4Nn3FDQm2k

    #Paper on conway by Martin Gardner
    https://www.dbs.ifi.lmu.de/Lehre/SEP/WS1112/vorprojekt/MathematicalGames.pdf

    http://www.math.com/students/wonders/life/life.html
"""

import os
import argparse
import subprocess
from datetime import datetime
import pygame
import random
import numpy as np

#------------------------------------------------------------------------------

#TODO: finish help document and pep8 the remainder
my_parser = argparse.ArgumentParser()
my_parser.add_argument('-s', '--size', action='store', type=int, nargs=2,
    help="Takes in two arguments that represent the size of the board.")
my_parser.add_argument('-g', '--generation', action='store', type=int,
    help="Sets the max generation.")
my_parser.add_argument('-p', '--population', action='store', type=int,
    help="Percentage of times that random cells of life are added to based on board size.")
my_parser.add_argument('-r', '--rate', action='store', type=int,
    help="Frame rate that is displated to the screen and used when converting to video.")
my_parser.add_argument('-t', '--text', action='store_true',
    help="Displays text to the screen and converted video.")
my_parser.add_argument('-d', '--delete', action='store_true',
    help="Flag used if you want the images of generations deleted when program is done running.")

# Sanity checks user inputs
args = my_parser.parse_args()

# Fills in default values if user did not define
if args.size is None:
    height = 200
    width = 200
else:
    if args.size[0] > 9 and args.size[1] > 9:
        height = int(args.size[0])
        width = int(args.size[1])
    else:
        print(f'ERROR: Minimum board size is 10 by 10')
        sys.exit(0)

if args.generation is None:
    maxgeneration = 250
else:
    maxgeneration = args.generation

if args.population is None:
    population = .2
else:
    population = args.population / 100

if args.rate is None:
    rate = 2
else:
    rate = args.rate

startTime = datetime.now()

# The main loop will carry on until the user 
# exit the game (e.g. clicks the close button).
mainLoop = True

path = os.getcwd()
isdir = os.path.isdir("temp")
np.random.seed(random.seed(datetime.now()))

pygame.init()

""" FiraCode is The Open Font License (OFL) is maintained by SIL International.
    It attempts to be a compromise between the values of the free software
    and typeface design communities. It is used for almost all open
    source font projects, including those by Adobe, Google and Mozilla.

https://github.com/tonsky/FiraCode/blob/master/LICENSE
"""
font = pygame.font.Font("FiraCode-Regular.ttf", int(height/10))

# Define some colors
black = ( 0, 0, 0)
white = ( 255, 255, 255)
orange = (255, 133, 0) # Used for text

# Generation 0
generation = 0
newtable = np.zeros((width,height))
oldtable = newtable

# Generation 1
# Randomly sets an intial state of living squares
for i in range(int(width * height * (population))):
    newtable[random.randint(0, width - 1 )][random.randint(0, height - 1 )] = 1

# Open a new window
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tribute to John Horton Conway's Game of Life")

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# Initially fills the background color to black representing generation 0
#  and outputs it to the screen
screen.fill(black)

if args.text == True:
    text = font.render("GEN: " + str(generation), True, orange)
    
    screen.blit(text, (int(width / 2 - text.get_width() // 2),
     int(height - (height * .1) - text.get_height() // 2)))

def counter(i,j,x,y,width,height):
    return int(oldtable[(x + i + width) % width][(y + j + height) % height])

def countNeighbors(oldtable,x,y):
    """Counts the living neighbors of a cell

    Args:
        oldtable: 
        x (int): cordanante of the starting cell
        y (int): coordinate of the starting cell

    Returns:
        int: count of the neighbors

    """
    temp = 1

    count = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if not (i==0 and j==0):  #TODO: this needs rewritin to be more understandable
                count += int(oldtable[(x + i + width) % width][(y + j + height) % height])

    for i in range(-1,2):
        for j in range(-1,2):
            temp += 1

    count -= int(oldtable[x][y])

    return count

if isdir == False:
    os.mkdir("temp")

# ----------- Main Program Loop -----------
while mainLoop:
    # --- Main event loop
    for event in pygame.event.get() :  # User did something
        if event.type == pygame.QUIT :  # If user clicked close
            mainLoop = False  # Flag that we are done so we exit this loop

    # Clears the screen and populates the next generation to the screen
    screen.fill(black)

    for x in range(width):
        for y in range(height):
            if oldtable[x][y] == 1:
                screen.set_at((x, y), (white))

    if args.text == True:
        text = font.render("GEN: " + str(generation), True, orange)
        
        screen.blit(text,(int(width / 2 - text.get_width() // 2),
         int(height - (height * .1) - text.get_height() // 2)))

    pygame.display.flip()

    # Outputs screenshots to disk
    pygame.image.save(screen, "temp/Generation" + str(generation) + '.jpg')

    oldtable = newtable

    # Calculates the state of the next generation
    for x in range(width):
        for y in range(height):
            neighbors =  countNeighbors(oldtable,x,y)
            # Calculate dead cells
            if oldtable[x][y] == 0 and neighbors == 3:
                newtable[x][y] = 1
            # Calculate alive cells
            elif oldtable[x][y] == 1 and (neighbors < 2 or neighbors > 3):
                newtable[x][y] = 0

    clock.tick(args.rate)

    #print("Generation: ", generation)
    generation +=1

    if generation > maxgeneration:
        mainLoop = False

print(datetime.now() - startTime)

#TODO: do some research on ffmpeg # I need to know if this is the best implementation of it
#ffmpeg -r 30 -f image2 -s 2160x1440 -i Generation%d.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p test5.mp4
os.chdir(path)
subprocess.call(['ffmpeg', '-r', str(args.rate), '-f', 'image2', '-s',
    str(str(width) + 'x' + str(height)), '-i', 'temp/Generation%d.jpg',
    '-vcodec', 'libx264', '-crf', '25', '-pix_fmt', 'yuv420p', 'output.mp4'])
if args.delete == True:
    filelist = [ f for f in os.listdir(str(path + "\\temp"))]
    for f in filelist:
        os.remove(os.path.join(str(path + "\\temp"), f))

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
