import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Comparison")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

player = pygame.Rect(100, 100, 80, 60)
speed = 5

fixed = pygame.Rect(WIDTH // 2 - 40, HEIGHT // 2 - 30, 80, 60)

angle = 0
rotation_speed = 1

# --------------------------
# 🔺 OBB 충돌 함수 (SAT)
# --------------------------
def get_axes(points):
    axes = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        edge = (p2[0] - p1[0], p2[1] - p1[1])
        normal = (-edge[1], edge[0])
        
        length = math.hypot(normal[0], normal[1])
        axes.append((normal[0]/length, normal[1]/length))
    return axes

def project(points, axis):
    dots = [p[0]*axis[0] + p[1]*axis[1] for p in points]
    return min(dots), max(dots)

def obb_collision(p1, p2):
    axes = get_axes(p1) + get_axes(p2)
    for axis in axes:
        min1, max1 = project(p1, axis)
        min2, max2 = project(p2, axis)
        if max1 < min2 or max2 < min1:
            return False
    return True

running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed

    if keys[pygame.K_z]:
        rotation_speed = 3
    else:
        rotation_speed = 1

    angle += rotation_speed

    screen.fill(WHITE)

    # --------------------------
    # 🔴 AABB 충돌
    # --------------------------
    aabb_hit = player.colliderect(fixed)

    # --------------------------
    # 🔵 Circle 충돌
    # --------------------------
    p_center = player.center
    f_center = fixed.center

    p_radius = player.width // 2
    f_radius = fixed.width // 2

    dx = p_center[0] - f_center[0]
    dy = p_center[1] - f_center[1]
    distance = math.hypot(dx, dy)

    circle_hit = distance < (p_radius + f_radius)

    # --------------------------
    # 🟢 OBB 생성
    # --------------------------
    def get_rotated_rect(rect, angle):
        cx, cy = rect.center
        w, h = rect.width, rect.height
        
        corners = [
            (-w/2, -h/2),
            ( w/2, -h/2),
            ( w/2,  h/2),
            (-w/2,  h/2)
        ]

        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        result = []
        for x, y in corners:
            rx = x * cos_a - y * sin_a
            ry = x * sin_a + y * cos_a
            result.append((cx + rx, cy + ry))
        return result

    player_obb = get_rotated_rect(player, 0)   # 플레이어는 회전 없음
    fixed_obb = get_rotated_rect(fixed, angle)

    obb_hit = obb_collision(player_obb, fixed_obb)

    # --------------------------
    # 🎨 오브젝트 그리기
    # --------------------------
    pygame.draw.rect(screen, GRAY, player)
    pygame.draw.rect(screen, GRAY, fixed)

    pygame.draw.rect(screen, RED, player, 2)
    pygame.draw.rect(screen, RED, fixed, 2)

    pygame.draw.circle(screen, BLUE, p_center, p_radius, 2)
    pygame.draw.circle(screen, BLUE, f_center, f_radius, 2)

    pygame.draw.polygon(screen, GREEN, fixed_obb, 2)

    # --------------------------
    # 📝 텍스트 출력
    # --------------------------
    circle_text = font.render(f"Circle: {'HIT' if circle_hit else 'MISS'}", True, BLUE)
    aabb_text = font.render(f"AABB: {'HIT' if aabb_hit else 'MISS'}", True, RED)
    obb_text = font.render(f"OBB: {'HIT' if obb_hit else 'MISS'}", True, GREEN)

    screen.blit(circle_text, (10, 10))
    screen.blit(aabb_text, (10, 40))
    screen.blit(obb_text, (10, 70))

    pygame.display.flip()

pygame.quit()
sys.exit()