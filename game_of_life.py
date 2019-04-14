import numpy as np
import ctypes
import tkinter as tk
import pygame
import time

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# screen_width = 4000
# screen_height = 2000


print(screen_width,screen_height)


black = (0,0,0)
grey = (10,10,10)
offgrey = (200,200,0)
white = (255,255,255)

margin = 1
height = 5
width = 5

rows = screen_height//(height+margin)
cols = screen_width//(width+margin)
# grid = []
# for row in range(rows):
#     grid.append([])
#     for column in range(cols):
#         grid[row].append(0)
oldcells = np.zeros((rows,cols))
cells = np.random.choice([1, 0], size=(rows,cols), p=[2./20, 18./20])
neighbours = np.zeros((rows,cols))

pygame.init

window = [screen_width,screen_height]
screen = pygame.display.set_mode(window)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Conway's Game of Life")

clock = pygame.time.Clock()


def neighbour_counter():
	for y in range(1,rows-1):
		for x in range(1,cols-1):
			if cells[y][x] == 1:
				neighbours[y][x] = (cells[y-1][x-1]+cells[y-1][x]+cells[y-1][x+1]
					                +cells[y][x-1]+cells[y][x+1]+
					                cells[y+1][x-1]+cells[y+1][x]+cells[y+1][x+1])
			if cells[y][x] == 0:
				neighbours[y][x] = -(cells[y-1][x-1]+cells[y-1][x]+cells[y-1][x+1]
					                +cells[y][x-1]+cells[y][x+1]+
					                cells[y+1][x-1]+cells[y+1][x]+cells[y+1][x+1])
	cells_update()

def cells_update():
	oldcells = cells
	np.copyto(oldcells, cells) 
	for y in range(1,rows-1):
		for x in range(1,cols-1):
			if cells[y][x] == 1:
				if neighbours[y][x] < 2:
					cells[y][x] = 0
				elif neighbours[y][x] <4:
					cells[y][x] = 1
				elif neighbours[y][x] <9:
					cells[y][x] = 0
				continue
			else:
				if neighbours[y][x] == -3:
					cells[y][x] = 1
	update_window()

def update_window():
    for row in range(1,rows-1):
        for column in range(1,cols-1):
            color = grey
            if oldcells[row][column] == 1:            
                color = offgrey
            if cells[row][column] == 1:
            	color = white
            pygame.draw.rect(screen,
                             color,
                             [(margin + width) * column + margin,
                              (margin + height) * row + margin,
                              width,
                              height])
    # time.sleep(.020)
    clock.tick(100)
    pygame.display.flip()
    neighbour_counter()


def main():
	done = False
	while not done:
	    for event in pygame.event.get():
	        if event.type == pygame.QUIT:
	            done = True
	        elif event.type == pygame.MOUSEBUTTONDOWN:
	            # User clicks the mouse. Get the position
	            pos = pygame.mouse.get_pos()
	            # Change the x/y screen coordinates to grid coordinates
	            mouse_col = pos[0]//(width + margin)
	            mouse_row = pos[1]//(height + margin)
	            if cells[mouse_row][mouse_col] == 0:
	            	cells[mouse_row][mouse_col] = 1
	            else:
	            	cells[mouse_row][mouse_col] = 0

	            print("Click ", pos, "Grid coordinates: ", mouse_row, mouse_col)
	 
	    screen.fill(black)

	    update_window()

	    clock.tick(60)
	 
	    # Go ahead and update the screen with what we've drawn.
	    pygame.display.flip()
	 
	pygame.quit()

main()