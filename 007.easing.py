"""
🎯 파티클 시스템 학습 - 007.easing.py
📚 학습 목표: 마우스와 파티클의 상호작용과 자연스러운 움직임 구현
🎮 실습: 마우스를 움직여서 파티클들이 반응하는 것을 관찰해보세요!

단계별 학습:
1. pygame 초기화 및 화면 설정
2. 이미지 로딩 및 리사이즈
3. Particle 클래스 이해 (위치, 속도, 힘)
4. Effect 클래스 이해 (파티클 관리)
5. 물리 법칙 적용 (힘, 마찰력, 원래 위치로 돌아가기)
6. 마우스 상호작용 구현
"""

import pygame
import math
import sys

# ========================================
# 🎮 1단계: pygame 초기화 및 기본 설정
# ========================================

# pygame 라이브러리 초기화 (반드시 필요!)
pygame.init()

# 화면 설정
WIDTH = 1200  # 화면 가로 크기 (픽셀)
HEIGHT = 800  # 화면 세로 크기 (픽셀)
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 화면 생성
pygame.display.set_caption("파티클 시스템 - 마우스 상호작용")  # 창 제목

# 색상 정의 (R, G, B) - 0~255 사이의 값
WHITE = (255, 255, 255)  # 흰색
BLACK = (0, 0, 0)        # 검은색

# ========================================
# 🖼️ 2단계: 이미지 처리 함수
# ========================================

def load_and_resize_image(path, screen_width, screen_height):
    """
    이미지를 불러와서 화면 크기에 맞게 조정하는 함수
    
    매개변수:
    - path: 이미지 파일 경로
    - screen_width: 화면 가로 크기
    - screen_height: 화면 세로 크기
    
    반환값: 조정된 이미지 (pygame Surface)
    """
    try:
        # 이미지 불러오기
        image = pygame.image.load(path).convert()
        
        # 원본 이미지 크기 가져오기
        original_width, original_height = image.get_size()
        
        # 화면에 맞게 크기 조정 (비율 유지)
        # min()을 사용해서 이미지가 화면을 벗어나지 않도록 함
        scale = min(screen_width / original_width, screen_height / original_height)
        
        # 새로운 크기 계산
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        
        # 이미지 크기 조정
        return pygame.transform.scale(image, (new_width, new_height))
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        print(f"이미지 {path}를 불러올 수 없습니다.")
        print("프로그램을 종료합니다.")
        pygame.quit()
        sys.exit()

# ========================================
# ⚡ 3단계: Particle 클래스 (개별 파티클)
# ========================================

class Particle:
    """
    개별 파티클을 나타내는 클래스
    각 파티클은 위치, 속도, 색상 등의 속성을 가짐
    """
    
    def __init__(self, x, y, color, gap, effect):
        """
        Particle 객체 초기화
        
        매개변수:
        - x, y: 파티클의 초기 위치
        - color: 파티클 색상 (R, G, B)
        - gap: 파티클 간격 (크기 결정에 사용)
        - effect: Effect 객체 참조
        """
        # 기본 속성
        self.color = color          # 파티클 색상
        self.size = gap // 2        # 파티클 크기 (간격의 절반)
        self.effect = effect        # Effect 객체 참조
        
        # 현재 위치
        self.x = int(x)             # 현재 x 좌표
        self.y = int(y)             # 현재 y 좌표
        
        # 원래 위치 (파티클이 돌아갈 곳)
        self.origin_x = x           # 원래 x 좌표
        self.origin_y = y           # 원래 y 좌표
        
        # 물리 속성
        self.vx = 0                 # x 방향 속도
        self.vy = 0                 # y 방향 속도
        self.ease = 0.2             # 원래 위치로 돌아가는 강도 (0~1)
        self.friction = 0.95        # 마찰력 (0~1, 1에 가까울수록 마찰 없음)
    
    def draw(self, surface):
        """
        파티클을 화면에 그리는 함수
        
        매개변수:
        - surface: 그릴 화면 (pygame Surface)
        """
        # 사각형으로 파티클 그리기
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
    
    def update(self):
        """
        파티클의 물리 법칙을 적용하여 위치를 업데이트하는 함수
        마우스와의 상호작용, 마찰력, 원래 위치로 돌아가는 힘을 계산
        """
        # 🧲 1단계: 마우스와의 거리 계산
        dx = self.effect.mouse_x - self.x  # 마우스와 파티클의 x 거리
        dy = self.effect.mouse_y - self.y  # 마우스와 파티클의 y 거리
        distance = dx * dx + dy * dy       # 실제 거리 (제곱, 제곱근 계산 생략으로 성능 향상)
        
        # 🔥 2단계: 마우스가 파티클을 끌어당기는 힘 계산
        # 힘 = -마우스반경 / (거리 + 1) × 8
        # 음수: 끌어당기는 힘, 거리가 가까울수록 힘이 강해짐
        force = -self.effect.mouse_radius / (distance + 1) * 8
        
        # 🎯 3단계: 마우스 영향 범위 내에 있을 때만 힘 적용
        if distance < self.effect.mouse_radius:
            # 마우스 방향 계산 (삼각함수 사용)
            angle = math.atan2(dy, dx)  # 마우스를 향하는 각도
            
            # 힘을 x, y 방향으로 분해하여 속도에 적용
            self.vx += force * math.cos(angle)  # x 방향 속도 변화
            self.vy += force * math.sin(angle)  # y 방향 속도 변화
        
        # 🛑 4단계: 마찰력 적용 (속도 감소)
        self.vx *= self.friction  # x 속도에 마찰력 적용
        self.vy *= self.friction  # y 속도에 마찰력 적용
        
        # 🏠 5단계: 위치 업데이트 (속도 + 원래 위치로 돌아가는 힘)
        self.x += self.vx + (self.origin_x - self.x) * self.ease
        self.y += self.vy + (self.origin_y - self.y) * self.ease

# ========================================
# 🎪 4단계: Effect 클래스 (파티클 시스템 관리)
# ========================================

class Effect:
    """
    전체 파티클 시스템을 관리하는 클래스
    이미지에서 파티클을 생성하고, 모든 파티클을 업데이트함
    """
    
    def __init__(self, width, height, image_path):
        """
        Effect 객체 초기화
        
        매개변수:
        - width: 화면 가로 크기
        - height: 화면 세로 크기
        - image_path: 파티클로 만들 이미지 파일 경로
        """
        # 화면 설정
        self.width = width          # 화면 가로 크기
        self.height = height        # 화면 세로 크기
        
        # 파티클 시스템 설정
        self.particles = []         # 파티클들을 담을 리스트
        self.gap = 10               # 파티클 간격 (픽셀)
        
        # 마우스 상호작용 설정
        self.mouse_radius = 1000    # 마우스 영향 반경
        self.mouse_x = 0            # 마우스 x 좌표
        self.mouse_y = 0            # 마우스 y 좌표
        
        # 이미지에서 파티클 생성
        self.load_image_particles(image_path)
    
    def load_image_particles(self, image_path):
        """
        이미지를 파티클로 분해하는 함수
        
        매개변수:
        - image_path: 이미지 파일 경로
        """
        print(f"🖼️ 이미지 '{image_path}'에서 파티클을 생성합니다...")
        
        # 1단계: 이미지 불러오기 및 크기 조정
        image = load_and_resize_image(image_path, self.width, self.height)
        
        # 2단계: 이미지 크기 정보 가져오기
        img_width, img_height = image.get_size()
        
        # 3단계: 이미지를 화면 중앙에 배치하기 위한 오프셋 계산
        image_offset_x = (self.width - img_width) // 2
        image_offset_y = (self.height - img_height) // 2
        
        # 4단계: 이미지를 3차원 배열로 변환 (RGB 값 추출용)
        pixel_array = pygame.surfarray.array3d(image)
        
        # 5단계: 픽셀을 파티클로 변환
        particle_count = 0
        for y in range(0, pixel_array.shape[1], self.gap):  # 세로 방향으로 간격만큼 이동
            for x in range(0, pixel_array.shape[0], self.gap):  # 가로 방향으로 간격만큼 이동
                
                # 화면 좌표로 변환
                screen_x = x + image_offset_x
                screen_y = y + image_offset_y
                
                # 화면 범위 내에 있는 픽셀만 파티클로 생성
                if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                    # 픽셀의 RGB 값 추출
                    r, g, b = pixel_array[x, y]
                    color = (r, g, b)
                    
                    # 파티클 생성 및 리스트에 추가
                    particle = Particle(screen_x, screen_y, color, self.gap, self)
                    self.particles.append(particle)
                    particle_count += 1
        
        print(f"✅ {particle_count}개의 파티클을 생성했습니다!")
    
    def update(self, surface):
        """
        모든 파티클을 업데이트하고 화면에 그리는 함수
        
        매개변수:
        - surface: 그릴 화면 (pygame Surface)
        """
        # 화면을 검은색으로 지우기
        surface.fill(BLACK)
        
        # 모든 파티클 업데이트 및 그리기
        for particle in self.particles:
            particle.update()  # 물리 법칙 적용
            particle.draw(surface)  # 화면에 그리기
    
    def set_mouse_position(self, x, y):
        """
        마우스 위치를 설정하는 함수
        
        매개변수:
        - x: 마우스 x 좌표
        - y: 마우스 y 좌표
        """
        self.mouse_x = x
        self.mouse_y = y

# ========================================
# 🎮 5단계: 메인 게임 루프
# ========================================

def main():
    """
    메인 함수 - 게임의 시작점
    """
    # 이미지 파일 경로 설정
    image_path = "훠.jpg"  # 여기에 원하는 이미지 파일명을 입력하세요
    
    # 게임 설정
    clock = pygame.time.Clock()  # 프레임 레이트 조절용 시계
    
    print("🚀 파티클 시스템을 시작합니다...")
    
    # Effect 객체 생성 (이미지에서 파티클 생성)
    try:
        effect = Effect(WIDTH, HEIGHT, image_path)
    except Exception as e:
        print(f"❌ 오류: {e}")
        print("프로그램을 종료합니다.")
        pygame.quit()
        sys.exit()
    
    # 게임 루프 변수
    running = True  # 게임 실행 여부
    
    print("🎮 게임이 시작되었습니다!")
    print("📋 조작법:")
    print("   - 마우스 움직임: 파티클들이 마우스를 따라 움직입니다")
    print("   - ESC 키: 게임 종료")
    print("   - 창 닫기: 게임 종료")
    
    # 🎮 메인 게임 루프
    while running:
        # 이벤트 처리 (키보드, 마우스 입력 등)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 버튼
                running = False
            elif event.type == pygame.KEYDOWN:  # 키보드 키 누름
                if event.key == pygame.K_ESCAPE:  # ESC 키
                    running = False
        
        # 마우스 위치 업데이트
        mouse_x, mouse_y = pygame.mouse.get_pos()
        effect.set_mouse_position(mouse_x, mouse_y)
        
        # 파티클 시스템 업데이트 및 그리기
        effect.update(screen)
        
        # 화면 업데이트 (더블 버퍼링)
        pygame.display.flip()
        
        # 프레임 레이트 제한 (60 FPS)
        clock.tick(60)
    
    # 게임 종료
    print("👋 게임을 종료합니다.")
    pygame.quit()
    sys.exit()

# ========================================
# 🎯 실습 과제 및 실험
# ========================================

"""
파티클 움직임 조절
Particle 클래스의 update() 메서드에서 다음 값들을 바꿔보세요:
- self.ease = 0.2 → 0.1 (더 천천히 원래 위치로 돌아감)
- self.ease = 0.2 → 0.5 (더 빨리 원래 위치로 돌아감)
- self.friction = 0.95 → 0.9 (더 강한 마찰력)
- self.friction = 0.95 → 0.98 (더 약한 마찰력)

 마우스 영향력 조절
Effect 클래스의 __init__ 메서드에서 다음 값을 바꿔보세요:
- self.mouse_radius = 1000 → 500 (마우스 영향 범위 축소)
- self.mouse_radius = 1000 → 2000 (마우스 영향 범위 확대)

 파티클 크기 조절
Effect 클래스의 __init__ 메서드에서 다음 값을 바꿔보세요:
- self.gap = 10 → 5 (더 작은 파티클, 더 많은 개수)
- self.gap = 10 → 20 (더 큰 파티클, 더 적은 개수)

 힘의 강도 조절
Particle 클래스의 update() 메서드에서 다음 값을 바꿔보세요:
- * 8 → * 4 (더 약한 힘)
- * 8 → * 16 (더 강한 힘)


"""

# 프로그램 시작
if __name__ == "__main__":
    main()
