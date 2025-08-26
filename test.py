import pygame
import math
import random
import time
import sys

# 설정
pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("도트 이미지 원 안에서 애니메이션")
clock = pygame.time.Clock()

# 상태
is_image = False


# 이미지 불러오기 및 리사이즈
def load_and_resize_image(path, screen_width, screen_height):
    image = pygame.image.load(path).convert()
    w, h = image.get_size()
    diagonal = math.sqrt(w**2 + h**2)
    max_radius = min(screen_width, screen_height) / 2  # 반지름 제한
    scale = min(
        (screen_width * 0.8) / w,
        (screen_height * 0.8) / h,
        max_radius * 2 / diagonal,  # 외접원이 화면을 넘지 않게
    )
    new_size = (int(w * scale), int(h * scale))
    return pygame.transform.scale(image, new_size)


image = load_and_resize_image("미카사.png", WIDTH * 0.8, HEIGHT * 0.8)
img_width, img_height = image.get_size()
img_offset_x = WIDTH // 2 - img_width // 2
img_offset_y = HEIGHT // 2 - img_height // 2
img_center_x = WIDTH // 2
img_center_y = HEIGHT // 2
bounding_radius = math.sqrt((img_width / 2) ** 2 + (img_height / 2) ** 2)


# 픽셀 추출
def extract_pixels(surface, step=5):
    pixels = []
    array = pygame.surfarray.array3d(surface)
    for y in range(0, array.shape[1], step):
        for x in range(0, array.shape[0], step):
            r, g, b = array[x, y]
            pixels.append((x, y, r, g, b))
    return pixels


# easing
def ease_in_out_cubic(t):
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2


# Dot 클래스
class Dot:
    def __init__(self, x, y, r, g, b, image_x, image_y):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.image_x = image_x
        self.image_y = image_y
        self.target_x = image_x if is_image else x
        self.target_y = image_y if is_image else y
        self.start_x = self.x
        self.start_y = self.y
        self.start_time = time.time()
        self.duration = 1.5 + random.random()

    def update(self):
        t = (time.time() - self.start_time) / self.duration
        if t >= 1.0:
            self.start_x = self.x
            self.start_y = self.y
            if is_image:
                self.target_x = self.image_x
                self.target_y = self.image_y
            else:
                angle = random.uniform(0, 2 * math.pi)
                self.target_x = math.cos(angle) * bounding_radius + img_center_x
                self.target_y = math.sin(angle) * bounding_radius + img_center_y
            self.start_time = time.time()
            self.duration = 1.5 + random.random()
            t = 0
        eased_t = ease_in_out_cubic(t)
        self.x = self.start_x + (self.target_x - self.start_x) * eased_t
        self.y = self.start_y + (self.target_y - self.start_y) * eased_t

    def draw(self, surface):
        pygame.draw.circle(
            surface, (self.r, self.g, self.b), (int(self.x), int(self.y)), 2
        )


# Dot 초기화
dots = []
for px, py, r, g, b in extract_pixels(image, step=5):
    image_x = px + img_offset_x
    image_y = py + img_offset_y
    angle = random.uniform(0, 2 * math.pi)
    rand_x = math.cos(angle) * bounding_radius + img_center_x
    rand_y = math.sin(angle) * bounding_radius + img_center_y
    dots.append(Dot(rand_x, rand_y, r, g, b, image_x, image_y))

# 메인 루프
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_image = not is_image
            for dot in dots:
                dot.start_time = time.time()

    for dot in dots:
        dot.update()
        dot.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
