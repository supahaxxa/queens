from math import ceil
from os import getcwd
from time import sleep
import library.functions as fx
import library.warehouse as data
import pygame

cwd = getcwd()

pygame.init()

WIDTH, HEIGHT = 720, 720
BLACK = "#000000"
BONE_WHITE = "#e7decc"
WHITE = "#ffffff"

with open(data.levels_file_to_open, 'r') as file:
	file_content = file.read().strip().split('\n')
	number_of_levels = len(file_content)
	del file_content

cross = pygame.image.load(cwd + '\\' + "assets\\cross.png")
cross = pygame.transform.scale(cross, (50, 50))
crown = pygame.image.load(cwd + '\\' + "assets\\crown.png")
crown = pygame.transform.scale(crown, (50, 50))
blank = pygame.surface.Surface((0, 0))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(pygame.image.load(cwd + '\\' + "assets\\game_icon.png"))

def level_button_action(n):
	data.level_to_open = n

def left_button_action():
	global starting_index
	starting_index -= 25

def right_button_action():
	global starting_index
	starting_index += 25

def draw_grid():
	for i in range(grid_size):
		for j in range(grid_size):
			bgcolor = data.colors[grid[i * grid_size + j]]
			placex, placey = left_right_margin + j * 50, 50 + i * 50
			pygame.draw.rect(screen, bgcolor, pygame.Rect(placex, placey, 50, 50))
			del bgcolor

			# horizontal borderlines for the grid
			if i == 0:
				pygame.draw.line(screen, BLACK, (placex, placey), (placex + 50, placey), 3)
			elif i + 1 == grid_size:
				pygame.draw.line(screen, BLACK, (placex, placey + 50), (placex + 50, placey + 50), 3)
			if i > 0:
				extra = 2 * (grid[i * grid_size + j] != grid[(i - 1) * grid_size + j])
				pygame.draw.line(screen, BLACK, (placex, placey), (placex + 50, placey), 1 + extra)
				del extra

			# vertical borderlines for the grid
			if j == 0:
				pygame.draw.line(screen, BLACK, (placex, placey), (placex, placey + 50), 3)
			elif j + 1 == grid_size:
				pygame.draw.line(screen, BLACK, (placex + 50, placey), (placex + 50, placey + 50), 3)
			if j > 0:
				extra = 2 * (grid[i * grid_size + j] != grid[i * grid_size + j - 1])
				pygame.draw.line(screen, BLACK, (placex, placey), (placex, placey + 50), 1 + extra)
				del extra

	del i, j, placex, placey

def draw_marker():
	markers = [blank, cross, crown]
	for i in range(grid_size):
		for j in range(grid_size):
			screen.blit(markers[grid_status[i * grid_size + j]], (left_right_margin + j * 50, 50 + i * 50))
	del markers, i, j

def check_completion():
	color_set = set()
	for i in range(grid_size):
		if grid_status[i * grid_size: (i + 1) * grid_size].count(2) != 1:
			return False
		column_crown_count = 0
		for j in range(grid_size):
			if grid_status[j * grid_size + i] == 2:
				column_crown_count += 1

			current_index = i * grid_size + j
			if j > 0 and grid_status[current_index] * grid_status[current_index - 1] == 4:
				return False		# left
			if j + 1 < grid_size and grid_status[current_index] * grid_status[current_index + 1] == 4:
				return False		# right
			if i * j > 0 and grid_status[current_index] * grid_status[current_index - grid_size - 1] == 4:
				return False		# top left
			if i > 0 and grid_status[current_index] * grid_status[current_index - grid_size] == 4:
				return False		# top
			if (i > 0 and j + 1 < grid_size) and grid_status[current_index] * grid_status[current_index - grid_size + 1] == 4:
				return False		# top right
			if (i + 1 < grid_size and j > 0) and grid_status[current_index] * grid_status[current_index + grid_size - 1] == 4:
				return False		# bottom left
			if i + 1 < grid_size and grid_status[current_index] * grid_status[current_index + grid_size] == 4:
				return False		# bottom
			if (i + 1 < grid_size and j + 1 < grid_size) and grid_status[current_index] * grid_status[current_index + grid_size + 1] == 4:
				return False		# bottom right

			if grid_status[i * grid_size + j] == 2:
				color_set.add(grid[i * grid_size + j])
		if column_crown_count != 1:
			return False
	if len(color_set) != grid_size:
		return False
	return True

click = False
completed = False
running = True
starting_index = 0

while running:
	for event in pygame.event.get():
		if data.current_screen:
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					data.current_screen = 0
					data.level_to_open = None
					completed = False
				if event.key == pygame.K_r:
					grid_status = [0 for i in grid]
					completed = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True
				m = pygame.mouse.get_pos()
				mpress = pygame.mouse.get_pressed(3)
				if not completed:
					if left_right_margin <= m[0] <= WIDTH - left_right_margin and 50 <= m[1] <= 50 + grid_size * 50:
						left = ceil((m[0] - left_right_margin) / 50) - 1
						top = ceil(m[1] / 50) - 2
						if mpress[0]:
							grid_status[top * grid_size + left] = (grid_status[top * grid_size + left] + 1) % 3
						elif mpress[2]:
							grid_status[top * grid_size + left] = (grid_status[top * grid_size + left] * (grid_status[top * grid_size + left] - 1) + 2) % 4
			if event.type == pygame.MOUSEBUTTONUP:
				click = False
		else:
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				if event.key == pygame.K_LEFT and starting_index - 25 >= 0:
					starting_index -= 25
				if event.key == pygame.K_RIGHT and number_of_levels > starting_index + 25:
					starting_index += 25
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True
			if event.type == pygame.MOUSEBUTTONUP:
				click = False

	screen.fill(BONE_WHITE)

	if data.current_screen:
		pygame.display.set_caption("Queens - Level " + str(data.level_to_open))
		font = pygame.font.SysFont("Arial", 24)

		draw_grid()
		draw_marker()

		if check_completion():
			fx.render_text(screen, "Level Completed", font, BLACK, WIDTH // 2, HEIGHT - 25)
			completed = True
	else:
		pygame.display.set_caption("Queens - choose a level to play")
		font = pygame.font.SysFont("Arial", 48, bold=True)

		for k in range(starting_index, starting_index + 25):
			if k >= number_of_levels:
				continue
			i = (k % 25) % 5
			j = (k % 25) // 5
			fx.simulate_button(screen, 50 + i * 129, 50 + j * 129, 104, 104, "#dc2941", "#ff304d", "#b82337", str(k + 1),
							font, "#f0f0ff", click, lambda: level_button_action(k + 1))
		if starting_index - 25 >= 0:
			fx.simulate_polygon_button(screen, "#dc2941", "#ff304d", "#b82337", click, lambda: left_button_action(), (14.17468245, 360),
									(35.82531755, 372.5), (35.82531755, 347.5))
		if number_of_levels > starting_index + 25:
			fx.simulate_polygon_button(screen, "#dc2941", "#ff304d", "#b82337", click, lambda: right_button_action(), (WIDTH - 14.17468245, 360),
									(WIDTH - 35.82531755, 372.5), (WIDTH - 35.82531755, 347.5))

		if data.level_to_open:
			data.current_screen = 1

			with open(data.levels_file_to_open, 'r') as file:
				file_content = file.read().strip().split('\n')
				grid = file_content[data.level_to_open - 1].split(',')
				grid = list(map(int, grid))
				del file_content
			grid_size = round(len(grid) ** 0.5)
			grid_status = [0 for i in grid]
			left_right_margin = (WIDTH - grid_size * 50) // 2

	pygame.display.update()
	sleep(0.02)
pygame.quit()
