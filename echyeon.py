import pygame
import sys
import math
import random
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 80)

# 색
BG = (255, 209, 199)
FEVER_BG = [(255,200,200),(255,220,180),(255,240,200)]
PURPLE = (243, 229, 245)
PINK = (255, 182, 193)
WHITE = (255,255,255)
BLACK = (30,30,30)

ORANGE = (255,140,0)
LIGHT_ORANGE = (255,180,100)
GREEN = (80,200,120)
RED = (255,80,80)
BLUE = (100,150,255)

clock = pygame.time.Clock()

def spawn_carrot():
    return {"x":random.randint(50,750),"y":random.randint(50,550),"big":random.randint(1,5)==1}

def reset_game():
    return {
        "cx":400, "cy":300,
        "score":0,
        "last_fever":-1,
        "fever":False,
        "fever_start":0,
        "game_over":False,
        "carrots":[spawn_carrot() for _ in range(3)],
        "bombs":[
            {"x":random.randint(50,750),"y":random.randint(50,550),
             "dx":random.choice([-4,-3,3,4]),"dy":random.choice([-4,-3,3,4])}
            for _ in range(3)
        ],
        "items":[],
    }

state = reset_game()
retry_rect = pygame.Rect(300, 320, 200, 60)

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            if state["game_over"] and retry_rect.collidepoint(e.pos):
                state = reset_game()

    cx, cy = state["cx"], state["cy"]

    # 🖱️ 마우스 이동 (속도 개선)
    if not state["game_over"]:
        mx, my = pygame.mouse.get_pos()
        cx += (mx-cx)*0.25   # ← 더 빠르게!
        cy += (my-cy)*0.25

    state["cx"], state["cy"] = cx, cy

    # 배경
    screen.fill(random.choice(FEVER_BG) if state["fever"] else BG)

    # 피버 종료
    if state["fever"] and time.time()-state["fever_start"] > 10:
        state["fever"] = False

    # 🥕 당근
    if not state["game_over"]:
        new_carrots=[]
        for c in state["carrots"]:
            size=2 if c["big"] else 1
            color = LIGHT_ORANGE if c["big"] and int(time.time()*5)%2 else ORANGE

            pygame.draw.polygon(screen,color,[
                (c["x"],c["y"]),
                (c["x"]+20*size,c["y"]+50*size),
                (c["x"]-20*size,c["y"]+50*size)
            ])
            pygame.draw.ellipse(screen,GREEN,(c["x"]-10*size,c["y"]-20*size,20*size,20*size))

            if math.hypot(cx-c["x"],cy-c["y"]) < 40*size:
                gain = 5 if c["big"] else 1
                if state["fever"]: gain*=2
                state["score"] += gain
            else:
                new_carrots.append(c)

        while len(new_carrots)<(7 if state["fever"] else 3):
            new_carrots.append(spawn_carrot())
        state["carrots"]=new_carrots

    # 💣 장애물
    for b in state["bombs"]:
        if not state["game_over"]:
            b["x"] += b["dx"]
            b["y"] += b["dy"]

            if b["x"] < 20 or b["x"] > 780: b["dx"] *= -1
            if b["y"] < 20 or b["y"] > 580: b["dy"] *= -1

        pygame.draw.circle(screen, RED,(int(b["x"]),int(b["y"])),20)

        if not state["game_over"] and math.hypot(cx-b["x"],cy-b["y"])<40:
            state["game_over"] = True

    # 🔵 아이템 복구
    if random.random()<0.01:
        state["items"].append({"x":random.randint(50,750),"y":random.randint(50,550)})

    for it in state["items"][:]:
        pygame.draw.circle(screen, BLUE,(it["x"],it["y"]),10)
        if math.hypot(cx-it["x"],cy-it["y"])<40:
            state["score"]+=10
            state["items"].remove(it)

    # 피버
    if state["score"]>=300 and state["score"]//300 != state["last_fever"]:
        state["fever"]=True
        state["fever_start"]=time.time()
        state["last_fever"]=state["score"]//300

    # 🐰 토끼 (귀 복구!!)
    pygame.draw.circle(screen, PURPLE, (int(cx), int(cy)), 45)

    # 귀
    pygame.draw.ellipse(screen, PURPLE, (cx-25, cy-70, 20, 50))
    pygame.draw.ellipse(screen, PURPLE, (cx+5, cy-70, 20, 50))
    pygame.draw.ellipse(screen, PINK, (cx-20, cy-60, 10, 30))
    pygame.draw.ellipse(screen, PINK, (cx+10, cy-60, 10, 30))

    if state["game_over"]:
        pygame.draw.line(screen, BLACK, (cx-20, cy-15), (cx-10, cy-5), 3)
        pygame.draw.line(screen, BLACK, (cx-10, cy-15), (cx-20, cy-5), 3)
        pygame.draw.line(screen, BLACK, (cx+10, cy-15), (cx+20, cy-5), 3)
        pygame.draw.line(screen, BLACK, (cx+20, cy-15), (cx+10, cy-5), 3)
    else:
        pygame.draw.circle(screen, BLACK, (int(cx-15), int(cy-10)), 7)
        pygame.draw.circle(screen, BLACK, (int(cx+15), int(cy-10)), 7)

    pygame.draw.circle(screen, PINK, (int(cx), int(cy+5)), 5)

    # UI
    screen.blit(font.render(f"Score: {state['score']}",True,BLACK),(10,40))

    if state["game_over"]:
        text = big_font.render("GAME OVER", True, (255,0,0))
        screen.blit(text, (200, 200))

        pygame.draw.rect(screen, BLUE, retry_rect, border_radius=15)
        retry_text = font.render("RETRY", True, WHITE)
        screen.blit(retry_text, (retry_rect.x+60, retry_rect.y+20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

echo "# 20260177echyeon" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/echyeon/20260177echyeon.git
git push -u origin main