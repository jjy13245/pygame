import math
import random
import time
import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT
import config

class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)


class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0, 0), alive=True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.alive = alive

    def draw(self, surface) -> None:
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self):
        if self.alive:
            self.alive = False


class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list):
        for block in blocks:
            if self.rect.colliderect(block.rect) and block.alive:
                block.collide()
                self.dir = 360 - self.dir + random.randint(-5, 5)
                break

    def collide_paddle(self, paddle: Paddle) -> None:
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self):
        screen_width, screen_height = config.display_dimension
        
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.dir = 180 - self.dir
        
        if self.rect.bottom < 0:
            self.dir = 360 - self.dir
    
    def alive(self):
        screen_width, screen_height = config.display_dimension

        if self.rect.top > screen_height:
            return False
        return True


class Item:
    def __init__(self, pos, item_type="add_ball"):
        self.pos = pos
        self.rect = Rect(self.pos[0], self.pos[1], config.item_size[0], config.item_size[1])  # 크기 정의 (config에서 가져올 수 있음)
        self.type = item_type  # 아이템 종류, 기본값은 'add_ball'

    def __repr__(self):
        return f"Item({self.pos}, {self.type})"
    
    def move(self):
        # 아이템을 아래로 이동 (속도는 config에서 정의한 값을 사용)
        self.rect.top += config.item_speed  # 이동 속도는 config에서 설정한 값을 사용

    def check_collision(self, paddle):
        # Paddle과의 충돌을 확인
        if self.rect.colliderect(paddle.rect):
            return True
        return False

    def draw(self, surface):
        # 아이템을 화면에 그리기 (사각형으로 그릴 수 있음)
        pygame.draw.rect(surface, config.item_color, self.rect)


# 게임 루프에서 아이템들을 이동시키는 코드 예시 (아이템을 목록으로 관리하는 경우)
ITEMS = []  # 아이템들을 저장할 리스트

def tick():
    for item in ITEMS:
        item.move()  # 아이템을 이동시키는 부분
    
    # 추가적인 로직 (충돌 체크 등)
    for item in ITEMS:
        if item.check_collision(paddle):  # paddle과 충돌 체크
            # 충돌 시 아이템 처리
            pass

def main():
    # 초기화, pygame 실행 코드
    pygame.init()

    # Paddle과 Ball 초기화
    paddle = Paddle()
    ball = Ball()

    # 아이템 생성 예시
    item = Item((100, 100))
    ITEMS.append(item)

    # 게임 루프
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                paddle.move_paddle(event)

        tick()

        # 화면 업데이트 및 그리기
        screen.fill((0, 0, 0))  # 화면을 검정색으로 채우기
        ball.draw(screen)
        paddle.draw(screen)

        for item in ITEMS:
            item.draw(screen)  # 모든 아이템 그리기

        pygame.display.flip()  # 화면 업데이트

    pygame.quit()

if __name__ == "__main__":
    main()
