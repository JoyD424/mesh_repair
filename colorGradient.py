import sys, random, pygame, math
import numpy as np
from pygame.locals import *

# To run: use python 2.7 (not python3)

# Initialize random
random.seed()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
RADIUS = 1 # radius of vertex (when rendering)
LINEWIDTH = 1 # thickness of edges (when rendering)

# Colors
red =  [255, 0, 0]
white = [255, 255, 255]
black = [0, 0, 0]

# Pygame initialize screen:
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



# COORDINATE CONVERSION FUNCTIONS: 
# THIS IS THE CORRECT CONVERSION FUNCTION...
# Convert from pygame coordinates to cartesian coordinates
def toCartesianCoordinates(posn):
    newX = posn[0] - (SCREEN_WIDTH / 2)
    newY = -1 * (posn[1] - (SCREEN_HEIGHT / 2))
    return (newX, newY)

# Convert cartesian to pygame coordinates (top left corner in pygame is (0,0))
def toPygameCoordinates(posn):
   newX = posn[0] + (SCREEN_WIDTH / 2)
   newY = (-1 * posn[1]) + (SCREEN_HEIGHT / 2)
   return (newX, newY) 


# PYGAME RELATED RENDERING FUNCTIONS:
# Return the rbg value of the winding number
# Color scale:
# Pink (5) --> Red (1) --> Yellow (1/2) --> Green (1/4) --> Sky Blue (0) --> Navy (-1/2) --> Purple (-5)
# (255, 0, 255) <-- (255,0,0) <-- (255, 255, 0) <-- (0, 255, 0) <-- (0, 255, 255) <-- (0, 0, 255) <-- (123, 0, 255)
def assignRGBValue(n):
    # print n # TEST
    def incrementValue(i):
        return i/255
    if n == -20: # TEST 
        return [255, 0, 255] # TEST
    if n > 1:
        # print("N: " + str(n)) # TEST
        n = n - 1
        # print("IncrementValue: " + str(incrementValue(2.0))) # TEST
        blueValue = int(n / incrementValue(1.0))
        rgb = [255, 0, blueValue]
        # print(rgb) # TEST
    elif n > .5:
        n = n - .5
        greenValue = 255 - int(round(n / incrementValue(.5)))
        # print("Green value: " + str(greenValue)) # TEST
        rgb = [255, greenValue, 0]
    elif n > .25:
        n = n - .25
        redValue = int(round(n / incrementValue(.25)))
        rgb = [redValue, 255, 0]
    elif n > 0:
        blueValue = 255 - int(round(n / incrementValue(.25)))
        rgb = [0, 255, blueValue]
    elif n > -1:
        greenValue = 255 + int(round(n / incrementValue(1.0))) 
        rgb = [0, greenValue, 255]
    elif n >= -1:
        # print("N: " + str(n)) # TEST
        n += .5
        redValue = -1 * int(round(n / (1.5/123.0)))
        # print("RedValue: " + str(redValue)) # TEST
        rgb = [redValue, 0, 255]
        # print(rgb) # TEST
    else:
        print(n)
        print("ERROR: WINDING NUMBER NOT IN COLOR RANGE!")
        rgb = [0, 0, 0]
    return rgb

# Render colorful version (like synesthesia with winding numbers)
def render():
    pygame.init()
    pygame.display.set_caption("Open Spiral")
    DISPLAYSURF.fill(white)

    # Fill in screen
    increment = .006
    for x in range(0, SCREEN_WIDTH + 1):
        # print (increment * x)
        w = -1.0 + float(increment * x)
        print w
        color = assignRGBValue(w)
        # print(color) # TEST
        # coordinate = (x, SCREEN_HEIGHT / 2)
        # pygame.draw.circle(DISPLAYSURF, color, coordinate, RADIUS, 0)
        pygame.draw.line(DISPLAYSURF, color, (x, 0), (x, SCREEN_HEIGHT), LINEWIDTH)
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
    return



# MAIN:
def main(): 
    render()
    return
  

# Run:
if __name__ == "__main__":
    main()