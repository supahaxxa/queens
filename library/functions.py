from math import atan2
import pygame

def area_of_polygon(*points: tuple[float, float]) -> float:
	points = ccw_sort(*points)
	result = 0
	size = len(points)
	for i in range(size):
		result += points[i % size][0] * points[(i + 1) % size][1]
		result -= points[(i + 1) % size][0] * points[i % size][1]

	return abs(result) * 0.5

def ccw_sort(*points: tuple[float, float]) -> list:
	number_of_points = len(points)
	x_sum = 0
	y_sum = 0
	for i in points:
		x_sum += i[0]
		y_sum += i[1]
	centroid = (x_sum / number_of_points, y_sum / number_of_points)
	angle_point_pairs = []
	for i in points:
		relative_angle = atan2(i[1] - centroid[1], i[0] - centroid[0])
		angle_point_pairs.append((relative_angle, i))
	angle_point_pairs = sorted(angle_point_pairs)
	return [i[1] for i in angle_point_pairs]

def check_mouse_pos_rect(left: float, top: float, width: float, height: float) -> bool:
	return left <= pygame.mouse.get_pos()[0] <= left + width and top <= pygame.mouse.get_pos()[1] <= top + height

def check_mouse_pos_polygon(*points: tuple[float, float]) -> bool:
	return area_of_polygon(*points, pygame.mouse.get_pos()) <= area_of_polygon(*points)

def distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
	return (((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)) ** 0.5

def render_text(
		display_screen: pygame.surface.Surface,
		text_to_show: str,
		font_object: pygame.font.Font,
		font_color: str | tuple[int, int, int],
		left: int,
		top: int
) -> None:
	rendered_text = font_object.render(text_to_show, True, font_color)
	text_rect = rendered_text.get_rect()
	text_rect.center = (left, top)
	display_screen.blit(rendered_text, text_rect)

def simulate_button(
		display_screen: pygame.surface.Surface,
		left: float,
		top: float,
		width: float,
		height: float,
		normal_color: str | tuple[int, int, int],
		hover_color: str | tuple[int, int, int],
		click_color: str | tuple[int, int, int],
		button_text: str,
		text_font: pygame.font.Font,
		text_color: str | tuple[int, int, int],
		is_clicked: bool,
		on_click
) -> None:
	if check_mouse_pos_rect(left, top, width, height):
		if is_clicked:
			pygame.draw.rect(display_screen, click_color, pygame.Rect(left, top, width, height))
			on_click()
		else:
			pygame.draw.rect(display_screen, hover_color, pygame.Rect(left, top, width, height))
	else:
		pygame.draw.rect(display_screen, normal_color, pygame.Rect(left, top, width, height))

	render_text(display_screen, button_text, text_font, text_color, round(left + width / 2), round(top + height / 2))

def simulate_polygon_button(
		display_screen: pygame.surface.Surface,
		normal_color: str | tuple[int, int, int],
		hover_color: str | tuple[int, int, int],
		click_color: str | tuple[int, int, int],
		is_clicked: bool,
		on_click,
		*points: tuple[float, float]
) -> None:
	if check_mouse_pos_polygon(*points):
		if is_clicked:
			pygame.draw.polygon(display_screen, click_color, points)
			on_click()
		else:
			pygame.draw.polygon(display_screen, hover_color, points)
	else:
		pygame.draw.polygon(display_screen, normal_color, points)
