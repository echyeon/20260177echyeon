# 6주차 실습 기록





#### 사용한 에셋

###### \-이미지: \[CC]  Animals and Tea by Strawheart ( pixel-ani-dog.gif ) /  (제작자 링크) http://mtsids.com/

###### \-사운드: \[CC0] Dog barking mono by Brandon Morris



#### 사용한 ai프롬포트



\# ChatGPT \& 사용자 대화 기록



\---



\### 사용자

>>> %Run -c $EDITOR\_CONTENT  

Traceback (most recent call last):  

&#x20; File "<string>", line 50  

&#x20;   for y in range(HEIGHT):  

&#x20;   ^^^  

IndentationError: expected an indented block after function definition on line 49



\### ChatGPT

IndentationError입니다. Python에서는 함수, 반복문, 조건문 뒤에 반드시 들여쓰기 된 블록이 필요합니다.



\---



\### 사용자

gksrnrdjfhakfgo



\### ChatGPT

앗, 키보드가 엉켰거나 테스트용 문장 같아요 😅



\---



\### 사용자

한국어로말해



\### ChatGPT

좋아요, 한국어로 대화할게요. 😄



\---



\### 사용자

Pygame 코드 업로드



\### ChatGPT

코드에 Indentation 문제와 들여쓰기 문제, 사운드 경로 문제 등이 있네요.  

Python에서 반복문, 함수 정의 뒤에는 항상 들여쓰기 필요합니다.



\---



\### 사용자

그냥 하나의 코드로 해줘



\### ChatGPT

전체 코드를 하나의 Pygame 스크립트로 합쳐서 정리했습니다.  

(들여쓰기, 반복문, 이벤트 처리 모두 수정)



\---



\### 사용자

FileNotFoundError: No file 'shoot.wav' found...



\### ChatGPT

문제 원인: `shoot.wav` 파일이 현재 작업 폴더에 없음  

해결: 파일을 코드와 같은 폴더에 넣거나 절대 경로 지정



```python

shoot\_s = pygame.mixer.Sound("C:/Users/HOSEO/Desktop/shoot.wav")

사용자



스페이스바 누르면 소리나게해줘



ChatGPT

import pygame



pygame.init()

pygame.mixer.init()



screen = pygame.display.set\_mode((400, 300))

clock = pygame.time.Clock()



img = pygame.image.load("player.png").convert\_alpha()

rect = img.get\_rect(center=(200,150))



shoot\_sound = pygame.mixer.Sound("shoot.wav")



running = True

while running:

&#x20;   clock.tick(60)

&#x20;   for event in pygame.event.get():

&#x20;       if event.type == pygame.QUIT:

&#x20;           running = False

&#x20;       if event.type == pygame.KEYDOWN:

&#x20;           if event.key == pygame.K\_SPACE:

&#x20;               shoot\_sound.play()

&#x20;   screen.fill((30,30,40))

&#x20;   screen.blit(img, rect)

&#x20;   pygame.display.flip()



pygame.quit()

사용자



이미지가 gif 파일인데 그대로 움직이게는 못해?



ChatGPT



pygame.image.load()는 GIF 애니메이션을 자동 재생 못하고 첫 프레임만 읽습니다.



해결 방법:



GIF를 여러 PNG로 쪼개서 애니메이션처럼 재생

PIL 라이브러리로 GIF 프레임 추출 후 Pygame에서 재생



예: PNG 쪼개기 방식



frames = \[pygame.image.load("frame0.png"),

&#x20;         pygame.image.load("frame1.png"),

&#x20;         pygame.image.load("frame2.png")]



frame\_index = 0

timer = 0



\# 게임 루프 안에서

timer += 1

if timer % 10 == 0:

&#x20;   frame\_index = (frame\_index + 1) % len(frames)

screen.blit(frames\[frame\_index], (x, y))



#### 

