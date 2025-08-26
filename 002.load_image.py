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


loaded_image = load_and_resize_image('훠.jpg',WIDTH,HEIGHT)




def main():

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
                elif event.key == pygame.K_f: # 누른 키가 f면 
                    fullscreen = not fullscreen # F키로 전체화면/창모드 전환

                    if fullscreen: # 전체화면인 경우  screen을 다시 설정
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        WIDTH, HEIGHT = screen.get_size() # 너비 높이도 다시 설정해주고,
                    else: # 창화면인 경우
                        screen = pygame.display.set_mode((1200, 800))  # 1200 x  800 창모드
                        WIDTH, HEIGHT = 1200, 800 
                    

        # 마우스 위치 업데이트
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #print(mouse_x,mouse_y)
        
        screen.fill(WHITE)
        
        # 이미지 표시하기
        screen.blit(loaded_image,(0,0))
        
        # 화면 업데이트
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
