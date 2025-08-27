"""
🎯 클래스 학습 2단계 - 이미지 로딩 및 함수 개념
📚 학습 목표: 함수 정의와 이미지 처리 방법
🎮 실습: 다른 이미지 파일을 로드해보세요!

이번 단계에서 배울 것:
1. 함수 정의와 호출 방법
2. 매개변수(parameter)와 반환값(return) 개념
3. 이미지 파일 로딩 방법
4. 예외 처리(try-except) 개념
5. 이미지 크기 조정 방법
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
pygame.display.set_caption("파티클 시스템 - 2단계: 이미지 로딩")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# ========================================
# 🖼️ 2단계: 이미지 로딩 함수 정의
# ========================================

def load_and_resize_image(image_path, screen_width, screen_height):
    """
    이미지를 불러와서 화면 크기에 맞게 조정하는 함수
    
    매개변수(Parameters):
    - image_path: 이미지 파일 경로 (문자열)
    - screen_width: 화면 가로 크기 (정수)
    - screen_height: 화면 세로 크기 (정수)
    
    반환값(Return Value): 조정된 이미지 (pygame Surface)
    
    예외 처리: 이미지 로드 실패 시 프로그램 종료
    """
    
    print(f"🖼️ 이미지 '{image_path}'를 로딩합니다...")
    
    try:
        # 1단계: 이미지 파일 불러오기
        # pygame.image.load()는 이미지 파일을 pygame Surface로 변환합니다
        original_image = pygame.image.load(image_path)
        
        # 2단계: 이미지 최적화 (성능 향상)
        # .convert()는 이미지를 화면 형식에 맞게 변환합니다
        optimized_image = original_image.convert()
        
        # 3단계: 원본 이미지 크기 가져오기
        original_width, original_height = optimized_image.get_size()
        print(f"📐 원본 이미지 크기: {original_width} x {original_height}")
        
        # 4단계: 화면에 맞는 크기 계산
        # min() 함수를 사용해서 이미지가 화면을 벗어나지 않도록 합니다
        # 비율을 유지하면서 화면에 맞게 조정합니다
        
        # 가로 비율 계산
        width_ratio = screen_width / original_width
        # 세로 비율 계산  
        height_ratio = screen_height / original_height
        # 더 작은 비율을 선택 (이미지가 화면을 벗어나지 않도록)
        scale = min(width_ratio, height_ratio)
        
        # 5단계: 새로운 크기 계산
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        
        print(f"📏 조정된 크기: {new_width} x {new_height}")
        print(f"📊 스케일 비율: {scale:.2f}")
        
        # 6단계: 이미지 크기 조정
        # pygame.transform.scale()은 이미지 크기를 조정하는 함수입니다
        resized_image = pygame.transform.scale(optimized_image, (new_width, new_height))
        
        print("✅ 이미지 로딩 완료!")
        return resized_image
        
    except FileNotFoundError:
        # 파일을 찾을 수 없을 때
        print(f"❌ 오류: '{image_path}' 파일을 찾을 수 없습니다.")
        print("💡 이미지 파일이 현재 폴더에 있는지 확인해주세요.")
        pygame.quit()
        sys.exit()
        
    except pygame.error as e:
        # pygame 관련 오류 (지원하지 않는 이미지 형식 등)
        print(f"❌ pygame 오류: {e}")
        print("💡 지원하는 이미지 형식: PNG, JPG, JPEG, GIF, BMP")
        pygame.quit()
        sys.exit()
        
    except Exception as e:
        # 기타 예상치 못한 오류
        print(f"❌ 예상치 못한 오류: {e}")
        pygame.quit()
        sys.exit()

# ========================================
# 🎨 3단계: 이미지 표시 함수 정의
# ========================================

def draw_image_centered(surface, image):
    """
    이미지를 화면 중앙에 그리는 함수
    
    매개변수:
    - surface: 그릴 화면 (pygame Surface)
    - image: 그릴 이미지 (pygame Surface)
    """
    
    # 화면 크기 가져오기
    screen_width, screen_height = surface.get_size()
    
    # 이미지 크기 가져오기
    image_width, image_height = image.get_size()
    
    # 중앙 위치 계산
    # 화면 중앙 = (화면 크기 - 이미지 크기) / 2
    center_x = (screen_width - image_width) // 2
    center_y = (screen_height - image_height) // 2
    
    # 이미지를 화면에 그리기
    # surface.blit()은 한 Surface를 다른 Surface에 그리는 함수입니다
    surface.blit(image, (center_x, center_y))

# ========================================
# 🎮 4단계: 메인 게임 루프
# ========================================

def main():
    """
    메인 함수 - 게임의 시작점
    """
    print("🚀 이미지 로딩 시스템을 시작합니다...")
    print("📋 조작법:")
    print("   - ESC 키: 게임 종료")
    print("   - 창 닫기: 게임 종료")
    
    # 이미지 파일 경로 설정
    # 여기에 원하는 이미지 파일명을 입력하세요
    image_path = "훠.jpg"  # 이미지 파일이 현재 폴더에 있어야 합니다
    
    # 이미지 로딩
    try:
        loaded_image = load_and_resize_image(image_path, WIDTH, HEIGHT)
        print(f"🎯 '{image_path}' 이미지가 성공적으로 로드되었습니다!")
    except:
        print("❌ 이미지 로딩에 실패했습니다.")
        return
    
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
        
        # 화면 그리기
        screen.fill(BLACK)  # 배경을 검은색으로 지우기
        
        # 이미지를 화면 중앙에 그리기
        draw_image_centered(screen, loaded_image)
        
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
🧪 실습 과제 1: 다른 이미지 파일 로드하기
image_path 변수를 다른 이미지 파일명으로 바꿔보세요:
- "미카사.png"
- "리바이.png" 
- "거인2.webp"
- "무지성거인.jpg"

🧪 실습 과제 2: 함수 매개변수 실험하기
load_and_resize_image() 함수 호출 시 매개변수를 바꿔보세요:
- load_and_resize_image(image_path, 800, 600) (더 작은 화면)
- load_and_resize_image(image_path, 1600, 900) (더 큰 화면)

🧪 실습 과제 3: 이미지 크기 정보 출력하기
load_and_resize_image() 함수에 다음 코드를 추가해보세요:
print(f"이미지 파일 경로: {image_path}")
print(f"화면 크기: {screen_width} x {screen_height}")

🧪 실습 과제 4: 새로운 함수 만들어보기
이미지를 화면의 다른 위치에 그리는 함수를 만들어보세요:
def draw_image_at_position(surface, image, x, y):
    surface.blit(image, (x, y))

🎯 도전 과제:
1. 키보드로 이미지를 움직일 수 있도록 만들어보기
2. 마우스 클릭한 위치에 이미지를 그리기
3. 여러 개의 이미지를 동시에 표시하기
4. 이미지 회전 기능 추가하기
"""

# 프로그램 시작
if __name__ == "__main__":
    main()
