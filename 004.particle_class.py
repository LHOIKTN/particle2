"""
🎯 클래스 학습 4단계 - 클래스 기본 개념과 Particle 클래스
📚 학습 목표: 클래스와 객체 지향 프로그래밍의 기본 개념
🎮 실습: Particle 클래스의 속성과 메서드를 수정해보세요!

이번 단계에서 배울 것:
1. 클래스(Class)와 객체(Object)의 개념
2. 생성자(__init__) 메서드의 역할
3. 인스턴스 변수와 메서드의 정의
4. self 키워드의 의미와 사용법
5. 객체 생성과 메서드 호출 방법
"""

import pygame
import sys

# ========================================
# 🎮 1단계: pygame 초기화 및 기본 설정
# ========================================

pygame.init()

# 화면 설정
WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("파티클 시스템 - 4단계: 클래스 기본 개념")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# ========================================
# 🧩 2단계: 클래스 개념 설명
# ========================================

"""
📚 클래스(Class)란?
- 클래스는 객체를 만들기 위한 '틀' 또는 '설계도'입니다
- 예: 자동차 설계도 → 실제 자동차(객체)를 만들 수 있음
- 예: 쿠키 틀 → 여러 개의 쿠키(객체)를 만들 수 있음

📚 객체(Object)란?
- 클래스로부터 만들어진 실제 '인스턴스'입니다
- 각 객체는 고유한 속성(데이터)과 행동(메서드)을 가집니다
- 예: 자동차1(빨간색, 100km/h), 자동차2(파란색, 80km/h)

📚 인스턴스 변수란?
- 객체마다 가지고 있는 고유한 데이터입니다
- self.변수명 형태로 정의합니다
- 예: self.x, self.y, self.color

📚 메서드(Method)란?
- 객체가 할 수 있는 행동(함수)입니다
- self 매개변수를 첫 번째로 받습니다
- 예: self.draw(), self.move()
"""

# ========================================
# ⚡ 3단계: Particle 클래스 정의
# ========================================

class Particle:
    """
    파티클(입자)을 나타내는 클래스
    
    속성(Attributes):
    - x, y: 파티클의 위치
    - color: 파티클의 색상
    - size: 파티클의 크기
    
    메서드(Methods):
    - __init__(): 생성자 (객체 초기화)
    - draw(): 파티클을 화면에 그리기
    - move(): 파티클 이동
    """
    
    def __init__(self, x, y, color=WHITE, size=5):
        """
        생성자 메서드 - Particle 객체를 초기화합니다
        
        매개변수:
        - x: 파티클의 x 좌표
        - y: 파티클의 y 좌표
        - color: 파티클의 색상 (기본값: 흰색)
        - size: 파티클의 크기 (기본값: 5)
        
        self는 현재 객체를 가리키는 참조입니다
        """
        
        # 인스턴스 변수 정의 (객체의 속성)
        self.x = x          # 파티클의 x 좌표
        self.y = y          # 파티클의 y 좌표
        self.color = color  # 파티클의 색상
        self.size = size    # 파티클의 크기
        
        # 추가 속성들
        self.original_x = x  # 원래 x 위치 (나중에 돌아갈 곳)
        self.original_y = y  # 원래 y 위치 (나중에 돌아갈 곳)
        
        print(f"🎯 파티클이 생성되었습니다! 위치: ({x}, {y}), 색상: {color}, 크기: {size}")
    
    def draw(self, surface):
        """
        파티클을 화면에 그리는 메서드
        
        매개변수:
        - surface: 그릴 화면 (pygame Surface)
        """
        # pygame.draw.rect()로 사각형 그리기
        # (x, y, width, height) 형태로 사각형 정의
        rect = (self.x, self.y, self.size, self.size)
        pygame.draw.rect(surface, self.color, rect)
    
    def move(self, dx, dy):
        """
        파티클을 이동시키는 메서드
        
        매개변수:
        - dx: x 방향 이동량
        - dy: y 방향 이동량
        """
        # 현재 위치에 이동량을 더해서 새로운 위치 계산
        self.x += dx
        self.y += dy
        
        print(f"🔄 파티클이 이동했습니다: ({self.x - dx}, {self.y - dy}) → ({self.x}, {self.y})")
    
    def reset_position(self):
        """
        파티클을 원래 위치로 되돌리는 메서드
        """
        old_x, old_y = self.x, self.y
        self.x = self.original_x
        self.y = self.original_y
        
        print(f"🏠 파티클이 원래 위치로 돌아갔습니다: ({old_x}, {old_y}) → ({self.x}, {self.y})")
    
    def change_color(self, new_color):
        """
        파티클의 색상을 변경하는 메서드
        
        매개변수:
        - new_color: 새로운 색상 (R, G, B)
        """
        old_color = self.color
        self.color = new_color
        
        print(f"🎨 파티클 색상이 변경되었습니다: {old_color} → {new_color}")
    
    def get_info(self):
        """
        파티클의 정보를 반환하는 메서드
        
        반환값: 파티클 정보 문자열
        """
        return f"파티클 - 위치: ({self.x}, {self.y}), 색상: {self.color}, 크기: {self.size}"

# ========================================
# 🎨 4단계: 파티클 관리 함수들
# ========================================

def create_particles(count=10):
    """
    여러 개의 파티클을 생성하는 함수
    
    매개변수:
    - count: 생성할 파티클 개수
    
    반환값: 파티클 리스트
    """
    particles = []
    
    print(f"🚀 {count}개의 파티클을 생성합니다...")
    
    for i in range(count):
        # 랜덤한 위치에 파티클 생성
        import random
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        
        # 랜덤한 색상 선택
        colors = [RED, GREEN, BLUE, YELLOW, WHITE]
        color = random.choice(colors)
        
        # 랜덤한 크기 (3~10)
        size = random.randint(3, 10)
        
        # Particle 객체 생성
        particle = Particle(x, y, color, size)
        particles.append(particle)
    
    print(f"✅ {len(particles)}개의 파티클이 생성되었습니다!")
    return particles

def draw_all_particles(surface, particles):
    """
    모든 파티클을 화면에 그리는 함수
    
    매개변수:
    - surface: 그릴 화면
    - particles: 파티클 리스트
    """
    for particle in particles:
        particle.draw(surface)

def move_all_particles(particles, dx, dy):
    """
    모든 파티클을 이동시키는 함수
    
    매개변수:
    - particles: 파티클 리스트
    - dx: x 방향 이동량
    - dy: y 방향 이동량
    """
    for particle in particles:
        particle.move(dx, dy)

# ========================================
# 🎮 5단계: 메인 게임 루프
# ========================================

def main():
    """
    메인 함수 - 게임의 시작점
    """
    print("🚀 클래스 학습 시스템을 시작합니다...")
    print("📋 조작법:")
    print("   - ESC 키: 게임 종료")
    print("   - 방향키: 모든 파티클 이동")
    print("   - R 키: 파티클들을 원래 위치로")
    print("   - C 키: 파티클 색상 변경")
    print("   - I 키: 파티클 정보 출력")
    print("   - N 키: 새로운 파티클들 생성")
    
    # 파티클 생성
    particles = create_particles(15)
    
    # 게임 설정
    clock = pygame.time.Clock()
    running = True
    
    # 🎮 메인 게임 루프
    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    move_all_particles(particles, -10, 0)  # 왼쪽으로 이동
                elif event.key == pygame.K_RIGHT:
                    move_all_particles(particles, 10, 0)   # 오른쪽으로 이동
                elif event.key == pygame.K_UP:
                    move_all_particles(particles, 0, -10)  # 위로 이동
                elif event.key == pygame.K_DOWN:
                    move_all_particles(particles, 0, 10)   # 아래로 이동
                elif event.key == pygame.K_r:
                    # 모든 파티클을 원래 위치로
                    for particle in particles:
                        particle.reset_position()
                elif event.key == pygame.K_c:
                    # 모든 파티클 색상 변경
                    import random
                    colors = [RED, GREEN, BLUE, YELLOW, WHITE]
                    for particle in particles:
                        particle.change_color(random.choice(colors))
                elif event.key == pygame.K_i:
                    # 파티클 정보 출력
                    print("\n📊 파티클 정보:")
                    for i, particle in enumerate(particles):
                        print(f"  {i+1}. {particle.get_info()}")
                elif event.key == pygame.K_n:
                    # 새로운 파티클들 생성
                    particles = create_particles(15)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                new_particle = Particle(x, y)
                particles.append(new_particle)
        
        # 화면 그리기
        screen.fill(BLACK)
        
        # 모든 파티클 그리기
        draw_all_particles(screen, particles)
        
        # 화면 업데이트
        pygame.display.flip()
        clock.tick(60)
    
    # 게임 종료
    print("👋 게임을 종료합니다.")
    pygame.quit()
    sys.exit()

# ========================================
# 🎯 실습 과제
# ========================================

"""
🧪 실습 과제 1: Particle 클래스에 새로운 속성 추가하기
Particle 클래스의 __init__ 메서드에 새로운 속성을 추가해보세요:
- self.speed: 파티클의 속도
- self.life: 파티클의 생명력
- self.visible: 파티클이 보이는지 여부

🧪 실습 과제 2: 새로운 메서드 추가하기
Particle 클래스에 새로운 메서드를 추가해보세요:
def grow(self):
    self.size += 1  # 크기 증가

def shrink(self):
    if self.size > 1:
        self.size -= 1  # 크기 감소

🧪 실습 과제 3: 파티클 개수 조절하기
create_particles() 함수의 기본값을 바꿔보세요:
- create_particles(5)  # 적은 파티클
- create_particles(50) # 많은 파티클

🧪 실습 과제 4: 마우스 클릭으로 파티클 생성하기
마우스 클릭한 위치에 파티클을 생성하는 기능을 추가해보세요:
elif event.type == pygame.MOUSEBUTTONDOWN:
    x, y = pygame.mouse.get_pos()
    new_particle = Particle(x, y)
    particles.append(new_particle)

🎯 도전 과제:
1. 파티클들이 서로 충돌하는지 감지하는 기능
2. 파티클의 생명력이 시간이 지나면서 감소하는 기능
3. 파티클들이 중력의 영향을 받도록 만들기
4. 파티클을 드래그해서 이동할 수 있는 기능
"""

# 프로그램 시작
if __name__ == "__main__":
    main()
