from os import getcwd
from os.path import exists
from time import sleep
import library.functions as fx
import library.warehouse as data
import pygame

cwd = getcwd()

pygame.init()
font = pygame.font.SysFont("Arial", 12)

WIDTH, HEIGHT = 720, 720
BLACK = "#000000"
GRAY = "#7f7f7f"
BONE_WHITE = "#e7decc"

grid_size = 11
grid = [-1] * grid_size * grid_size
left_margin = (WIDTH - 50 * grid_size) // 2
top_margin = 50
x = y = 0

if not exists(data.levels_file_to_open):
	with open(data.levels_file_to_open, 'w') as file:
		file.write('')

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Queens - Level Builder")

def draw_grid(n):
	for fk in range(n * n):
		fi, fj = fk // n, fk % n
		bgcolor = data.colors[grid[fk]]
		left, top = fj * 50 + left_margin, fi * 50 + top_margin
		pygame.draw.rect(screen, bgcolor, pygame.Rect(left, top, 50, 50))

		if fi == 0:
			pygame.draw.line(screen, BLACK, (left, top), (left + 50, top), 3)
		elif fi - 1 >= 0:
			if grid[fk] == grid[fk - n]:
				pygame.draw.line(screen, BLACK, (left, top), (left + 50, top), 1)
			else:
				pygame.draw.line(screen, BLACK, (left, top), (left + 50, top), 3)
		if fi + 1 == n:
			pygame.draw.line(screen, BLACK, (left, top + 50), (left + 50, top + 50), 3)

		if fj == 0:
			pygame.draw.line(screen, BLACK, (left, top), (left, top + 50), 3)
		elif fj - 1 >= 0:
			if grid[fk] == grid[fk - 1]:
				pygame.draw.line(screen, BLACK, (left, top), (left, top + 50), 1)
			else:
				pygame.draw.line(screen, BLACK, (left, top), (left, top + 50), 3)
		if fj + 1 == n:
			pygame.draw.line(screen, BLACK, (left + 50, top), (left + 50, top + 50), 3)

	del fi, fj, fk, bgcolor, left, top

def draw_palette():
	for fi in range(10):
		left, top = 40, fi * 50 + 65
		pygame.draw.circle(screen, data.colors[fi], (left, top), 15)
		fx.render_text(screen, str(fi), font, BLACK, left, top + 25)

def draw_cursor(li, ti):
	pygame.draw.circle(screen, GRAY, (li * 50 + left_margin + 25, ti * 50 + top_margin + 25), 3)

def record_data():
	new_line = ','.join([*map(str, grid)])

	with open(data.levels_file_to_open, 'a') as f_file:
		f_file.write(new_line + '\n')

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
			if event.key in {pygame.K_LEFT, pygame.K_a}:
				x = (x - 1) % grid_size
			if event.key in {pygame.K_RIGHT, pygame.K_d}:
				x = (x + 1) % grid_size
			if event.key in {pygame.K_UP, pygame.K_w}:
				y = (y - 1) % grid_size
			if event.key in {pygame.K_DOWN, pygame.K_s}:
				y = (y + 1) % grid_size
			if pygame.K_0 <= event.key <= pygame.K_9:
				grid[y * grid_size + x] = event.key - pygame.K_0
			if event.key == pygame.K_PAGEUP and grid_size < 11:
				grid_size += 1
				grid = [-1] * grid_size * grid_size
				left_margin = (WIDTH - 50 * grid_size) // 2
				x = y = 0
			if event.key == pygame.K_PAGEDOWN and grid_size > 5:
				grid_size -= 1
				grid = [-1] * grid_size * grid_size
				left_margin = (WIDTH - 50 * grid_size) // 2
				x = y = 0
			if event.key == pygame.K_RETURN and -1 not in grid:
				record_data()
				print("[i] Stored a level.")
				grid = [-1] * grid_size * grid_size
				x = y = 0

	screen.fill(BONE_WHITE)

	draw_grid(grid_size)
	draw_palette()
	draw_cursor(x, y)

	pygame.display.update()

	sleep(0.02)
