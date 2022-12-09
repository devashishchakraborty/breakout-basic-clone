import pygame, sys

class Paddle(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, paddle_speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (180, 16))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.speed = paddle_speed
        self.movement = 0
    
    def screen_constraint(self):
        if self.rect.left <= play_field.left + 5:
            self.rect.left = play_field.left + 5
        if self.rect.right >= play_field.right - 5: 
            self.rect.right = play_field.right - 5

    def update(self):
        self.rect.x += self.movement
        screen.blit(self.image, self.rect)
        self.screen_constraint()


class Ball(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, ball_speed, paddle, target):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.smoothscale(self.image, (25, 25))
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.speed_x = ball_speed
        self.speed_y = ball_speed
        self.paddle = paddle
        self.target = target
    
    def collisions(self):
        if self.rect.top <= play_field.top:
            self.speed_y *= -1
        if self.rect.left <= play_field.left or self.rect.right >= play_field.right:
            self.speed_x *= -1

        if pygame.sprite.spritecollide(self, self.paddle, False):
            collision_paddle = pygame.sprite.spritecollide(self, self.paddle, False)[0].rect
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.speed_y *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.speed_y *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
        
        if pygame.sprite.spritecollide(self, self.target, True):
            collision_target = pygame.sprite.spritecollide(self, self.target, True)[0].rect
            if abs(self.rect.bottom - collision_target.top) < 5 and self.speed_y > 0:
                self.speed_y *= -1
            if abs(self.rect.top - collision_target.bottom) < 5 and self.speed_y < 0:
                self.speed_y *= -1
            if abs(self.rect.left - collision_target.right) < 5 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.right - collision_target.left) < 5 and self.speed_x > 0:
                self.speed_x *= -1
            
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.collisions()
        screen.blit(self.image, self.rect)


class Target(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (80,10))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
    
    def update(self):
        screen.blit(self.image, self.rect)



# Initial Setup
pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 1200, 800
screen = pygame.display.set_mode((screen_width, screen_height))
speed = 5

# Play Field
play_field = pygame.Rect(0,0, screen_width/1.05, screen_height/1.05)
play_field.center = (screen_width/2, screen_height/2)

# Paddle Group
paddle = Paddle("paddle.png", screen_width/2, screen_height/1.05, speed)
paddle_group = pygame.sprite.GroupSingle()
paddle_group.add(paddle)

# Target Block Group
target_group = pygame.sprite.Group()
for column in range(100, play_field.width, 100):
    for row in range(100, int(play_field.height/2), 100):
        target = Target("glasspaddle2.png", column, row)
        target_group.add(target)


# Ball Group
ball = Ball("ball.png", screen_width/2, screen_height/2, speed, paddle_group, target_group)
ball_group = pygame.sprite.GroupSingle()
ball_group.add(ball)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle.movement -= paddle.speed
            if event.key == pygame.K_RIGHT:
                paddle.movement += paddle.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                paddle.movement += paddle.speed
            if event.key == pygame.K_RIGHT:
                paddle.movement -= paddle.speed

    screen.fill((30,30,30))
    pygame.draw.rect(screen, "white", play_field, 1)
    
    target_group.update()
    paddle_group.update()
    ball_group.update()
    
    pygame.display.flip()
    clock.tick(60)
