import pygame
import math
import sys

# pygame 초기화
pygame.init()

# 화면 설정
WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle System")
fullscreen = False

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 이미지 불러오기 및 리사이즈
def load_and_resize_image(path, screen_width, screen_height):
    try:
        image = pygame.image.load(path).convert()
        w, h = image.get_size()
        # 화면 비율에 맞게 조정 (잘리지 않도록)
        scale = min(
            screen_width / w,
            screen_height / h
        )
        new_size = (int(w * scale), int(h * scale))
        return pygame.transform.scale(image, new_size)
    except:
        print(f"이미지 {path}를 불러올 수 없습니다. 기본 particle을 사용합니다.")
        return None

# 픽셀 추출
def extract_pixels(surface, step=5):
    pixels = []
    array = pygame.surfarray.array3d(surface)
    for y in range(0, array.shape[1], step):
        for x in range(0, array.shape[0], step):
            r, g, b = array[x, y]
            pixels.append((x, y, r, g, b))
    return pixels

class Particle:
    def __init__(self, x, y, effect, color=WHITE):
        self.origin_x = x
        self.origin_y = y
        self.effect = effect
        self.x = int(x)
        self.y = int(y)
        self.vx = 0
        self.vy = 0
        self.ease = 0.2
        self.friction = 0.95
        self.dx = 0
        self.dy = 0
        self.distance = 0
        self.force = 0
        self.angle = 0
        self.size = 2
        self.color = color

    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
    
    def update(self):
        # 마우스와의 거리 계산
        self.dx = self.effect.mouse_x - self.x
        self.dy = self.effect.mouse_y - self.y
        self.distance = self.dx * self.dx + self.dy * self.dy
        self.force = -self.effect.mouse_radius / (self.distance + 1) * 8  # 0으로 나누기 방지
        
        # 마우스 반경 내에 있을 때 힘 적용
        if self.distance < self.effect.mouse_radius:
            self.angle = math.atan2(self.dy, self.dx)
            self.vx += self.force * math.cos(self.angle)
            self.vy += self.force * math.sin(self.angle)
        
        # 위치 업데이트
        self.vx *= self.friction
        self.vy *= self.friction
        self.x += self.vx + (self.origin_x - self.x) * self.ease
        self.y += self.vy + (self.origin_y - self.y) * self.ease

class Effect:
    def __init__(self, width, height, image_path=None):
        self.width = width
        self.height = height
        self.particles_array = []
        self.gap = 7
        self.mouse_radius = 1000
        self.mouse_x = 0
        self.mouse_y = 0

        
        # 이미지 로드 시도
        if image_path:
            self.load_image_particles(image_path)
        else:
            self.init_grid_particles()
    
    def load_image_particles(self, image_path):
        """이미지에서 particle 생성"""
        image = load_and_resize_image(image_path, self.width, self.height)
        if image:
            img_width, img_height = image.get_size()
            # 이미지가 화면을 완전히 덮도록 중앙 정렬
            img_offset_x = (self.width - img_width) // 2
            img_offset_y = (self.height - img_height) // 2
            
            # 픽셀 추출
            pixels = extract_pixels(image, step=5)
            
            # particle 생성
            for px, py, r, g, b in pixels:
                image_x = px + img_offset_x
                image_y = py + img_offset_y
                # 화면 범위 내에 있는 particle만 생성
                if 0 <= image_x < self.width and 0 <= image_y < self.height:
                    color = (r, g, b)
                    self.particles_array.append(Particle(image_x, image_y, self, color))
            
            print(f"이미지에서 {len(self.particles_array)}개의 particle을 생성했습니다.")
        else:
            self.init_grid_particles()
    
    def init_grid_particles(self):
        """기본 격자 particle 생성"""
        self.particles_array = []
        for x in range(0, self.width, self.gap):
            for y in range(0, self.height, self.gap):
                self.particles_array.append(Particle(x, y, self))
        print(f"격자에서 {len(self.particles_array)}개의 particle을 생성했습니다.")
    
    def update(self, surface):
        # 화면 지우기
        surface.fill(BLACK)
        
        # 모든 particle 업데이트
        for particle in self.particles_array:
            particle.update()
            particle.draw(surface)
    
    def set_mouse_position(self, x, y):
        self.mouse_x = x
        self.mouse_y = y

def main():
    global screen, fullscreen, WIDTH, HEIGHT
    clock = pygame.time.Clock()
    
    # 이미지 경로 설정 (이미지가 있다면 경로를 지정하세요)
    image_path = "미카사.png"  # 이미지 파일 경로를 여기에 지정
    
    # Effect 객체 생성 (이미지가 있으면 이미지 사용, 없으면 격자 사용)
    try:
        effect = Effect(WIDTH, HEIGHT, image_path)
    except:
        effect = Effect(WIDTH, HEIGHT)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # 스페이스바로 이미지/격자 전환
                    if hasattr(effect, 'image_path') and effect.image_path:
                        effect = Effect(WIDTH, HEIGHT)  # 격자로 전환
                    else:
                        effect = Effect(WIDTH, HEIGHT, image_path)  # 이미지로 전환
                elif event.key == pygame.K_f:
                    # F키로 전체화면 전환
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        WIDTH, HEIGHT = screen.get_size()
                    else:
                        screen = pygame.display.set_mode((1200, 800))
                        WIDTH, HEIGHT = 1200, 800
                    # 화면 크기가 변경되었으므로 Effect 객체 재생성
                    try:
                        effect = Effect(WIDTH, HEIGHT, image_path)
                    except:
                        effect = Effect(WIDTH, HEIGHT)

        
        # 마우스 위치 업데이트
        mouse_x, mouse_y = pygame.mouse.get_pos()
        effect.set_mouse_position(mouse_x, mouse_y)
        
        # 효과 업데이트 및 그리기
        effect.update(screen)
        
        # 화면 업데이트
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
