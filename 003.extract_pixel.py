import pygame
import math
import sys

# pygame 초기화
pygame.init()

# 화면 설정
WIDTH = 1200 # 너비
HEIGHT = 800 # 높이
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 표시될 화면(스크린) 지정
fullscreen = False  # 풀스크린으로 할지 말지

# 색상 정의 (r,g,b)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# 이미지 불러오기 and 리사이즈
def load_and_resize_image(path, screen_width, screen_height):
    try:
        image = pygame.image.load(path).convert() #  이미지 불러오기
        w,h = image.get_size()  # 이미지의 가로 세로 높이 추출
        scale = min(screen_width/w, screen_height/h)  # 화면 비율 정하기
        new_size = (int(w*scale), int(h*scale))
        return pygame.transform.scale(image,new_size)
    except Exception  as e :
        print(e)
        print(f"이미지 {path}를 불러올 수 없습니다.")
        pygame.quit()
        sys.exit()





# 클래스 만들기
class Effect:
    def __init__(self, width, height, image_path):
        """Effect 클래스 생성시 최초에 정의할 속성들"""
        self.width = width   # 화면 너비
        self.height = height # 화면 높이
        self.particles = []  # 이미지 분해해서 얻은 파티클을 담을 리스트
        self.gap = 20
        
        """속성을 모두 정의하면 그 다음에 이미지를 파티클로 분해"""
        self.load_image_particles(image_path) # Effect 인스턴스를 생성했을 때 실행
    
    
    def load_image_particles(self, image_path):
        """이미지에서 파티클 생성"""

        # 이미지 불러오기 & 사이즈 조정
        image = load_and_resize_image(image_path,self.width,self.height)

        # 이미지 사이즈 추출하기
        img_width, img_heigth = image.get_size() 

        # 이미지가 화면을 완전히 덮도록 중앙 정렬
        image_offset_x = (self.width - img_width)//2
        image_offset_y = (self.height - img_heigth)//2 

        # 🤓 픽셀 추출
        array = pygame.surfarray.array3d(image)
        for y in range(0, array.shape[1], self.gap):
            for x in range(0, array.shape[0], self.gap):
                
                image_x = x + image_offset_x
                image_y = y + image_offset_y

                if 0<= image_x < self.width and 0<= image_y < self.height:
                    r,g,b = array[x,y]
                    color = (r,g,b)
                    #self.particles.append()
                    pygame.draw.rect(screen, color, (x, y, self.gap//2, self.gap//2))

        
def main():
    image_path = "훠.jpg"
    global screen, fullscreen, WIDTH, HEIGHT #전역변수로 설정
    clock = pygame.time.Clock() # Framerate 조절을 위한 시계


    running = True # 진행 여부
    while running:  # 무한루프. 이제 running을 False 로 설정하면 루프 탈출하고 종료

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 나가기 버튼 누르면 
                running = False  # 루프 종료
            elif event.type == pygame.KEYDOWN: # 키를 누르면
                if event.key == pygame.K_ESCAPE: # 누른 키가 ESC 키면
                    running = False # 루프 종료

        
        screen.fill(BLACK)
        
        # 이미지 표시하기
        effect = Effect(WIDTH,HEIGHT, image_path)
        
        # 화면 업데이트
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
