from math import ceil

import json
import pygame
import assets.warehouse as data

GRAY = (127, 127, 127)
BLACK = (0, 0, 0)
BONE_WHITE = "#E7DECC"
WHITE = (255, 255, 255)

# globals
click = False
cross = None
crown = None
font = 0
go_left_signal = False
go_right_signal = False
grid = []
grid_size = 0
grid_status = []
level_to_run = 0
screen = None
SIDE = 0


def area_of_triangle(p1: tuple, p2: tuple, p3: tuple):
	return 0.5 * abs(p1[0] * p2[1] + p2[0] * p3[1] + p3[0] * p1[1] - p1[1] * p2[0] - p2[1] * p3[0] - p3[1] * p1[0])


def check_completion():
	global grid, grid_size, grid_status

	color_set = set()
	for i in range(grid_size):
		if grid_status[i].count(2) != 1:
			return False
		column_crown_count = 0
		for j in range(grid_size):
			if grid_status[j][i] == 2:
				column_crown_count += 1

			r, c = i - 1, j - 1
			if (r >= 0 and c >= 0) and (grid_status[r][c] == 2 and grid_status[i][j] == 2):
				return False
			r, c = i - 1, j
			if r >= 0 and (grid_status[r][c] == 2 and grid_status[i][j] == 2):
				return False
			r, c = i - 1, j + 1
			if (r >= 0 and c < grid_size) and (grid_status[r][c] == 2 and grid_status[i][j] == 2):
				return False
			r, c = i, j - 1
			if c >= 0 and (grid_status[r][c] == 2 and grid_status[i][j] == 2):
				return False
			r, c = i, j + 1
			if c < grid_size and (grid_status[r][c] == 2 and grid_status[i][j] == 2):
				return False
			r, c = i + 1, j - 1
			if (r < grid_size and c >= 0) and (grid_status[r][c] == 2 and grid_status[i][j] == 2):
				return False
			r, c = i + 1, j
			if r < grid_size and (grid_status[r][c] == 2 and grid_status[i][j] == 2):
				return False
			r, c = i + 1, j + 1
			if (r < grid_size and c < grid_size) and (grid_status[r][c] == 2 and grid_status[i][j] == 2):
				return False

			if grid_status[i][j] == 2:
				color_set.add(grid[i][j])
		if column_crown_count != 1:
			return False
	if len(color_set) != grid_size:
		return False

	return True


def check_hover(l1, t1, width0, height0, radius0):
	if l1 + radius0 <= pygame.mouse.get_pos()[0] <= l1 + width0 - radius0 and t1 <= pygame.mouse.get_pos()[1] <= t1 + height0:
		return True			# checking vertical rect
	if l1 <= pygame.mouse.get_pos()[0] <= l1 + width0 and t1 + radius0 <= pygame.mouse.get_pos()[1] <= t1 + height0 - radius0:
		return True			# checking horizontal rect
	if distance(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], l1 + radius0, t1 + radius0) <= radius0:
		return True			# checking top left arc
	if distance(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], l1 + width0 - radius0, t1 + radius0) <= radius0:
		return True			# checking top right arc
	if distance(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], l1 + radius0, t1 + height0 - radius0) <= radius0:
		return True			# checking bottom left arc
	if distance(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], l1 + width0 - radius0, t1 + height0 - radius0) <= radius0:
		return True			# checking bottom right arc
	return False


def check_triangle_hover(p1: tuple, p2: tuple, p3: tuple):
	m = pygame.mouse.get_pos()
	area1 = area_of_triangle(p1, p2, m)
	area2 = area_of_triangle(p2, p3, m)
	area3 = area_of_triangle(p3, p1, m)

	if abs(area_of_triangle(p1, p2, p3) - area1 - area2 - area3) < 0.01:
		return True
	return False


def distance(x1, y1, x2, y2):
	return (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5


def draw_cursor(ti, li):
	pygame.draw.circle(screen, GRAY, ((li + 1) * 50 + 25, (ti + 1) * 50 + 25), 3)


def draw_grid():
	global grid, grid_size, screen

	for i in range(len(grid)):
		for j in range(len(grid)):
			bgcolor = data.colors[grid[i][j]]
			left, top = (j + 1) * 50, (i + 1) * 50
			pygame.draw.rect(screen, bgcolor, pygame.Rect(left, top, 50, 50))

			if i == 0:
				pygame.draw.line(screen, BLACK, (left, top), (left + 50, top), 3)
			elif i - 1 >= 0:
				if grid[i][j] == grid[i - 1][j]:
					pygame.draw.line(screen, BLACK, (left, top), (left + 50, top), 1)
				else:
					pygame.draw.line(screen, BLACK, (left, top), (left + 50, top), 3)
			if i + 1 == len(grid):
				pygame.draw.line(screen, BLACK, (left, top + 50), (left + 50, top + 50), 3)

			if j == 0:
				pygame.draw.line(screen, BLACK, (left, top), (left, top + 50), 3)
			elif j - 1 >= 0:
				if grid[i][j] == grid[i][j - 1]:
					pygame.draw.line(screen, BLACK, (left, top), (left, top + 50), 1)
				else:
					pygame.draw.line(screen, BLACK, (left, top), (left, top + 50), 3)
			if j + 1 == len(grid):
				pygame.draw.line(screen, BLACK, (left + 50, top), (left + 50, top + 50), 3)

	del bgcolor, i, j, left, top


def draw_marker():
	global cross, crown, grid_size, grid_status, screen

	for i in range(grid_size):
		for j in range(grid_size):
			if grid_status[i][j] == 1:
				screen.blit(cross, ((j + 1) * 50, (i + 1) * 50))
			elif grid_status[i][j] == 2:
				screen.blit(crown, ((j + 1) * 50, (i + 1) * 50))


def draw_palette():
	global SIDE

	# left
	for i in range(5):
		l, t = 25, (i + 1) * 50 + 15
		pygame.draw.circle(screen, data.colors[i], (l, t), 15)
		render_text(str(i), l, t + 25)
	# right
	for i in range(5, 10):
		l, t = SIDE - 25, (i - 4) * 50 + 15
		pygame.draw.circle(screen, data.colors[i], (l, t), 15)
		render_text(str(i), l, t + 25)


def record_data(lvl_name):
	with open("assets/levels.json", 'r', encoding="utf-8") as file:
		json_data = json.load(file)
	json_data[lvl_name] = grid
	with open("assets/levels.json", 'w', encoding="utf-8") as file:
		json.dump(json_data, file)


def render_text(text, left, top):
	global font, screen

	text = font.render(text, True, BLACK)
	text_rect = text.get_rect()
	text_rect.center = (left, top)
	screen.blit(text, text_rect)


def simulate_button(l2, t2, width1, height1, radius1, level_name):
	global click, level_to_run, screen

	if check_hover(l2, t2, width1, height1, radius1):
		if click:
			pygame.draw.rect(screen, "#B82337", pygame.Rect(l2, t2, width1, height1), border_radius=radius1)
			level_to_run = level_name
		else:
			pygame.draw.rect(screen, "#FF304D", pygame.Rect(l2, t2, width1, height1), border_radius=radius1)
	else:
		pygame.draw.rect(screen, "#DC2941", pygame.Rect(l2, t2, width1, height1), border_radius=radius1)

	render_text(level_name, l2 + 25, t2 + 25)


def simulate_triangle_button(p1: tuple, p2: tuple, p3: tuple, signal_code):
	global click, go_left_signal, go_right_signal, screen

	if check_triangle_hover(p1, p2, p3):
		if click:
			pygame.draw.polygon(screen, "#B82337", [p1, p2, p3])

			if signal_code == "left":
				go_left_signal = True
			elif signal_code == "right":
				go_right_signal = True
		else:
			pygame.draw.polygon(screen, "#FF304D", [p1, p2, p3])
	else:
		pygame.draw.polygon(screen, "#DC2941", [p1, p2, p3])

		if signal_code == "left":
			go_left_signal = False
		elif signal_code == "right":
			go_right_signal = False


def level_builder():
	global font, grid, screen, SIDE

	done = False
	while not done:
		grid_size = int(input("\n\nEnter the size of the grid: "))
		level_name = input("Enter the name of the level: ")
		SIDE = (grid_size + 2) * 50

		pygame.init()

		screen = pygame.display.set_mode((SIDE, SIDE))
		pygame.display.set_caption("Queens - Level Builder")

		font = pygame.font.SysFont("Arial", 12)
		grid = [[-1 for j in range(grid_size)] for i in range(grid_size)]


		x, y = 0, 0

		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False
					if event.key == pygame.K_UP:
						y -= 1
						y %= grid_size
					if event.key == pygame.K_DOWN:
						y += 1
						y %= grid_size
					if event.key == pygame.K_LEFT:
						x -= 1
						x %= grid_size
					if event.key == pygame.K_RIGHT:
						x += 1
						x %= grid_size
					if pygame.K_0 <= event.key <= pygame.K_9:
						grid[y][x] = event.key - pygame.K_0

			screen.fill(WHITE)

			draw_grid()
			draw_palette()
			draw_cursor(y, x)

			pygame.display.update()

		record_data(level_name)
		print("[i] Recorded the grid data.")

		if input("Are you done? ") != "":
			done = True


def level_chooser():
	global click, font, go_left_signal, go_right_signal, level_to_run, screen

	pygame.init()

	SIDE = 450

	screen = pygame.display.set_mode((SIDE, SIDE))
	pygame.display.set_caption("Queens")

	font = pygame.font.SysFont("Arial", 24, bold=True)

	with open("assets/levels.json", 'r') as file:
		levels = json.load(file)
	level_names = list(levels.keys())

	click = False
	starting_index = 0
	go_left_signal = False
	go_right_signal = False

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				if event.key == pygame.K_LEFT and starting_index - 25 >= 0:
					starting_index -= 25
				if event.key == pygame.K_RIGHT and len(level_names) > starting_index + 25:
					starting_index += 25
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = True
			if event.type == pygame.MOUSEBUTTONUP:
				click = False

				if go_left_signal and starting_index - 25 >= 0:
					starting_index -= 25
					go_left_signal = False
				if go_right_signal and len(level_names) > starting_index + 25:
					starting_index += 25
					go_right_signal = False

		screen.fill(BONE_WHITE)

		for k in range(starting_index, starting_index + 25):
			if k >= len(level_names):
				continue
			i = (k % 25) % 5
			j = (k % 25) // 5
			simulate_button(50 + i * 75, 50 + j * 75, 50, 50, 5, level_names[k])
		if starting_index - 25 >= 0:
			simulate_triangle_button((14.17468245, 225), (35.82531755, 237.5), (35.82531755, 212.5), "left")
		if len(level_names) > starting_index + 25:
			simulate_triangle_button((SIDE - 14.17468245, 225), (SIDE - 35.82531755, 237.5), (SIDE - 35.82531755, 212.5), "right")

		if level_to_run:
			running = False

		pygame.display.update()

	pygame.quit()

	return level_to_run


def level_player(level_name):
	global crown, cross, font, grid, grid_size, grid_status, level_to_run, screen

	with open("assets/levels.json", 'r') as file:
		grid = json.load(file)
	grid = grid[level_name]

	grid_size = len(grid)
	SIDE = (grid_size + 2) * 50

	pygame.init()

	screen = pygame.display.set_mode((SIDE, SIDE))
	pygame.display.set_caption("Queens - Level " + level_name)

	grid_status = [[0 for j in range(grid_size)] for i in range(grid_size)]
	cross = pygame.image.load("assets/cross.png")
	crown = pygame.image.load("assets/crown.png")
	cross = pygame.transform.scale(cross, (50, 50))
	crown = pygame.transform.scale(crown, (50, 50))
	font = pygame.font.SysFont("Arial", 24)

	violations = 0
	completed = False
	clicked = False

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				if event.key == pygame.K_n:
					grid_status = [[0 for j in range(grid_size)] for i in range(grid_size)]
			if event.type == pygame.MOUSEBUTTONDOWN:
				if not completed:
					if 50 <= pygame.mouse.get_pos()[0] <= SIDE - 50 and 50 <= pygame.mouse.get_pos()[1] <= SIDE - 50:
						left = ceil(pygame.mouse.get_pos()[0] / 50) - 2
						top = ceil(pygame.mouse.get_pos()[1] / 50) - 2

						if pygame.mouse.get_pressed(3)[0]:
							grid_status[top][left] = (grid_status[top][left] + 1) % 3
						elif pygame.mouse.get_pressed(3)[2]:
							grid_status[top][left] = (grid_status[top][left] * (grid_status[top][left] - 1) + 2) % 4

		screen.fill(WHITE)

		draw_grid()
		draw_marker()

		if check_completion():
			render_text("Level Completed", SIDE // 2, SIDE - 25)
			completed = True

		pygame.display.update()

	pygame.quit()

	level_to_run = 0


if __name__ == "__main__":
	gameloop = True
	while gameloop:
		prompt = level_chooser()

		if prompt:
			level_player(prompt)
		else:
			gameloop = False
