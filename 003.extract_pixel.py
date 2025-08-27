"""
🎯 클래스 학습 3단계 - 픽셀 추출 및 배열 개념
📚 학습 목표: 이미지에서 픽셀 정보 추출과 배열 처리
🎮 실습: 픽셀 추출 간격을 바꿔보세요!

이번 단계에서 배울 것:
1. 이미지를 픽셀 배열로 변환하는 방법
2. 2차원 배열과 반복문을 이용한 픽셀 처리
3. RGB 색상 값 추출 방법
4. 픽셀 샘플링(간격 조절) 개념
5. 좌표계와 배열 인덱스의 관계
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
pygame.display.set_caption("파티클 시스템 - 3단계: 픽셀 추출")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# ========================================
# 🖼️ 2단계: 이미지 로딩 함수 (이전 단계에서 가져옴)
# ========================================

def load_and_resize_image(image_path, screen_width, screen_height):
    """
    이미지를 불러와서 화면 크기에 맞게 조정하는 함수
    """
    try:
        original_image = pygame.image.load(image_path)
        optimized_image = original_image.convert()
        
        original_width, original_height = optimized_image.get_size()
        scale = min(screen_width / original_width, screen_height / original_height)
        
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        
        resized_image = pygame.transform.scale(optimized_image, (new_width, new_height))
        return resized_image
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        pygame.quit()
        sys.exit()

# ========================================
# 🔍 3단계: 픽셀 추출 함수 정의
# ========================================

def extract_pixels(surface, step=5):
    """
    이미지에서 픽셀 정보를 추출하는 함수
    
    매개변수:
    - surface: 픽셀을 추출할 이미지 (pygame Surface)
    - step: 픽셀 추출 간격 (기본값: 5)
    
    반환값: 픽셀 정보 리스트 [(x, y, r, g, b), ...]
    """
    
    print(f"🔍 픽셀 추출을 시작합니다... (간격: {step}픽셀)")
    
    # 1단계: 이미지를 3차원 배열로 변환
    # pygame.surfarray.array3d()는 이미지를 (width, height, 3) 형태의 배열로 변환합니다
    # 3은 RGB 채널을 의미합니다 (Red, Green, Blue)
    pixel_array = pygame.surfarray.array3d(surface)
    
    # 배열의 크기 정보 출력
    array_width, array_height, channels = pixel_array.shape
    print(f"📊 배열 크기: {array_width} x {array_height} x {channels}")
    print(f"📊 이미지 크기: {surface.get_size()}")
    
    # 2단계: 픽셀 정보를 저장할 리스트 생성
    pixels = []
    
    # 3단계: 반복문을 이용해 픽셀 정보 추출
    # step 간격으로 픽셀을 샘플링합니다 (모든 픽셀을 추출하면 너무 많아집니다)
    
    extracted_count = 0  # 추출된 픽셀 개수 카운트
    
    # 세로 방향으로 step 간격만큼 이동
    for y in range(0, array_height, step):
        # 가로 방향으로 step 간격만큼 이동
        for x in range(0, array_width, step):
            
            # 현재 픽셀의 RGB 값 추출
            # pixel_array[x, y]는 (r, g, b) 형태의 튜플입니다
            r, g, b = pixel_array[x, y]
            
            # 픽셀 정보를 리스트에 추가
            # (x좌표, y좌표, 빨강값, 초록값, 파랑값)
            pixel_info = (x, y, r, g, b)
            pixels.append(pixel_info)
            
            extracted_count += 1
    
    print(f"✅ {extracted_count}개의 픽셀을 추출했습니다!")
    print(f"📈 추출 비율: {extracted_count} / {array_width * array_height} = {extracted_count / (array_width * array_height) * 100:.1f}%")
    
    return pixels

# ========================================
# 🎨 4단계: 픽셀을 화면에 표시하는 함수
# ========================================

def draw_pixels(surface, pixels, pixel_size=2):
    """
    추출된 픽셀들을 화면에 그리는 함수
    
    매개변수:
    - surface: 그릴 화면 (pygame Surface)
    - pixels: 픽셀 정보 리스트 [(x, y, r, g, b), ...]
    - pixel_size: 그릴 픽셀의 크기 (기본값: 2)
    """
    
    print(f"🎨 {len(pixels)}개의 픽셀을 화면에 그립니다...")
    
    # 이미지 중앙 정렬을 위한 오프셋 계산
    image_width, image_height = surface.get_size()
    screen_width, screen_height = pygame.display.get_surface().get_size()
    
    offset_x = (screen_width - image_width) // 2
    offset_y = (screen_height - image_height) // 2
    
    # 각 픽셀을 화면에 그리기
    for x, y, r, g, b in pixels:
        # 화면 좌표로 변환
        screen_x = x + offset_x
        screen_y = y + offset_y
        
        # 색상 생성
        color = (r, g, b)
        
        # 사각형으로 픽셀 그리기
        pygame.draw.rect(surface, color, (screen_x, screen_y, pixel_size, pixel_size))

# ========================================
# 📊 5단계: 픽셀 정보 분석 함수
# ========================================

def analyze_pixels(pixels):
    """
    추출된 픽셀들의 정보를 분석하는 함수
    
    매개변수:
    - pixels: 픽셀 정보 리스트 [(x, y, r, g, b), ...]
    """
    
    if not pixels:
        print("❌ 분석할 픽셀이 없습니다.")
        return
    
    print("📊 픽셀 정보 분석:")
    print(f"   총 픽셀 개수: {len(pixels)}")
    
    # RGB 값의 평균 계산
    total_r = sum(pixel[2] for pixel in pixels)  # 빨강 값들의 합
    total_g = sum(pixel[3] for pixel in pixels)  # 초록 값들의 합
    total_b = sum(pixel[4] for pixel in pixels)  # 파랑 값들의 합
    
    avg_r = total_r / len(pixels)
    avg_g = total_g / len(pixels)
    avg_b = total_b / len(pixels)
    
    print(f"   평균 색상: R={avg_r:.1f}, G={avg_g:.1f}, B={avg_b:.1f}")
    
    # 가장 밝은 픽셀과 가장 어두운 픽셀 찾기
    brightest = max(pixels, key=lambda p: p[2] + p[3] + p[4])  # RGB 합이 가장 큰 픽셀
    darkest = min(pixels, key=lambda p: p[2] + p[3] + p[4])    # RGB 합이 가장 작은 픽셀
    
    print(f"   가장 밝은 픽셀: {brightest}")
    print(f"   가장 어두운 픽셀: {darkest}")

# ========================================
# 🎮 6단계: 메인 게임 루프
# ========================================

def main():
    """
    메인 함수 - 게임의 시작점
    """
    print("🚀 픽셀 추출 시스템을 시작합니다...")
    print("📋 조작법:")
    print("   - ESC 키: 게임 종료")
    print("   - 창 닫기: 게임 종료")
    print("   - 숫자 키 1-9: 픽셀 추출 간격 변경")
    
    # 이미지 파일 경로 설정
    image_path = "훠.jpg"
    
    # 이미지 로딩
    try:
        loaded_image = load_and_resize_image(image_path, WIDTH, HEIGHT)
        print(f"🎯 '{image_path}' 이미지가 로드되었습니다!")
    except:
        print("❌ 이미지 로딩에 실패했습니다.")
        return
    
    # 초기 픽셀 추출
    current_step = 5  # 현재 픽셀 추출 간격
    pixels = extract_pixels(loaded_image, current_step)
    analyze_pixels(pixels)
    
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
                # 숫자 키로 픽셀 추출 간격 변경
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    new_step = event.key - pygame.K_0  # 1-9
                    if new_step != current_step:
                        current_step = new_step
                        print(f"\n🔄 픽셀 추출 간격을 {current_step}로 변경합니다...")
                        pixels = extract_pixels(loaded_image, current_step)
                        analyze_pixels(pixels)
        
        # 화면 그리기
        screen.fill(BLACK)
        
        # 픽셀들을 화면에 그리기
        draw_pixels(screen, pixels, pixel_size=current_step)
        
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
🧪 실습 과제 1: 픽셀 추출 간격 실험하기
숫자 키 1-9를 눌러서 픽셀 추출 간격을 바꿔보세요:
- 1: 매우 조밀한 픽셀 (모든 픽셀 추출)
- 5: 중간 간격 (기본값)
- 9: 매우 성긴 픽셀 (적은 픽셀 추출)

🧪 실습 과제 2: 픽셀 크기 조절하기
draw_pixels() 함수에서 pixel_size 매개변수를 바꿔보세요:
- pixel_size=1 (작은 픽셀)
- pixel_size=5 (큰 픽셀)
- pixel_size=current_step (간격과 같은 크기)

🧪 실습 과제 3: 색상 필터링 추가하기
특정 색상의 픽셀만 추출하는 기능을 추가해보세요:
def filter_pixels_by_color(pixels, min_brightness=100):
    return [p for p in pixels if p[2] + p[3] + p[4] > min_brightness]

🧪 실습 과제 4: 픽셀 정보 저장하기
추출된 픽셀 정보를 파일로 저장하는 기능을 추가해보세요:
import json
with open('pixels.json', 'w') as f:
    json.dump(pixels, f)

🎯 도전 과제:
1. 마우스로 특정 영역의 픽셀만 추출하기
2. 색상별로 픽셀을 분류하고 통계 내기
3. 픽셀을 크기나 밝기에 따라 정렬하기
4. 실시간으로 픽셀 추출 간격을 조절할 수 있는 UI 만들기
"""

# 프로그램 시작
if __name__ == "__main__":
    main()
