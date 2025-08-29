import pygame
import sys
from pygame import SurfaceType
# pygame 초기화
pygame.init()

# 화면 설정
WIDTH = 1280 # 너비
HEIGHT = 720 # 높이


# 색상 정의 (r,g,b)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# 이미지 불러오기 and 리사이즈
def load_and_resize_image(image_path, screen_width, screen_height):
    try:

        # 1. 이미지 파일 불러오기
        # 이미지 최적화 (성능 향상) 
        # .convert()는 이미지를 화면 형식에 맞게 변환 
        image = pygame.image.load(image_path).convert() 

        # 2. 이미지의 가로 세로 높이 추출
        image_width,image_height = image.get_size()  
        print(f"📐 원본 이미지 크기: {image_width} x {image_height}")
        # 3. 화면(screen)에 맞는 크기 계산
        # min() 함수를 사용해서 이미지가 화면을 벗어나지 않도록
        # 비율을 유지하면서 화면에 맞게 조정

        # 가로 비율 계산
        width_ratio = screen_width / image_width
        # 세로 비율 계산  
        height_ratio = screen_height / image_height
        # 더 작은 비율을 선택 (이미지가 화면을 벗어나지 않도록)
        scale = min(width_ratio, height_ratio)

        # 4. 새로운 크기 계산
        new_width = int(image_width * scale)
        new_height = int(image_height * scale)

        print(f"📏 조정된 크기: {new_width} x {new_height}")
        print(f"📊 스케일 비율: {scale:.2f}")
        new_size = (new_width, new_height)

        # 리사이즈 된 이미지 반환
        return pygame.transform.scale(image,new_size)
    
    except FileNotFoundError:
        # 파일을 찾을 수 없을 때
        print(f"❌ 오류: '{image_path}' 파일을 찾을 수 없습니다.")
        print("💡 이미지 파일이 현재 폴더에 있는지 확인해주세요.")
        pygame.quit()
        sys.exit()
        
    except pygame.error as e:
        # pygame 관련 오류 (지원하지 않는 이미지 형식 등)
        print(f"❌ pygame 오류: {e}")
        pygame.quit()
        sys.exit()
        
    except Exception as e:
        # 기타 예상치 못한 오류
        print(f"❌ 예상치 못한 오류: {e}")
        pygame.quit()
        sys.exit()





# 전체 파티클 시스템을 관리하는 클래스
# 이미지에서 파티클을 생성(픽셀 추출), 모든 파티클을 업데이트
class Effect:
    def __init__(self, width, height, image_path):
        """Effect 클래스 생성시 최초에 정의할 속성들"""

        self.width = width   
        self.height = height 


        self.particles = []  
        self.gap = 20 
        
        self.load_image_particles(image_path) 
    
    
    def load_image_particles(self, image_path):
        """이미지에서 파티클 생성"""

        
        image = load_and_resize_image(image_path,self.width,self.height)

        
        img_width, img_heigth = image.get_size() 



        image_offset_x = (self.width - img_width)//2
        image_offset_y = (self.height - img_heigth)//2 

       
        array = pygame.surfarray.array3d(image)
        print(f"이미지의 픽셀 배열: {array}")
        print(f"이미지의 픽셀 배열의 구성 (x, y, color): {array.shape}")
        

        # y 축은 세로 축 
        # x 축은 가로 축
        for y in range(0, array.shape[1], self.gap):  
            for x in range(0, array.shape[0], self.gap):
                
                
                image_x = x + image_offset_x
                image_y = y + image_offset_y

                
                if 0<= image_x < self.width and 0<= image_y < self.height:
                    r,g,b = array[x,y]
                    color = (r,g,b)
                    particle = (x,y,color)
                    self.particles.append(particle)

    def update(self, surface:SurfaceType):
        """
        모든 파티클을 업데이트하고 화면에 그리는 함수
        surface: 그릴 화면 (pygame Surface)
        """

        surface.fill(BLACK)
        
        for particle in self.particles:
            x,y,color = particle
            pygame.draw.rect(surface, color, (x,y,self.gap//2, self.gap//2))
        




                    
        
def main():
    image_path = "훠.jpg"
    global screen, WIDTH, HEIGHT #전역변수로 설정
    clock = pygame.time.Clock() # Framerate 조절을 위한 시계
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 표시될 화면(스크린) 지정
    screen_width, screen_height = screen.get_size()
    effect = Effect(screen_width, screen_height, image_path)
    running = True # 진행 여부
    while running:  # 무한루프. 이제 running을 False 로 설정하면 루프 탈출하고 종료

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 나가기 버튼 누르면 
                running = False  # 루프 종료
            elif event.type == pygame.KEYDOWN: # 키를 누르면
                if event.key == pygame.K_ESCAPE: # 누른 키가 ESC 키면
                    running = False # 루프 종료

        
        # 화면 업데이트
        effect.update(screen)
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
