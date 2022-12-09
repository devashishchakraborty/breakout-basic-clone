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
        if self.rect.left <= play_field.left:
            self.rect.left = play_field.left
        if self.rect.right >= play_field.right:
            self.rect.right = play_field.right

    def update(self):
        self.rect.x += self.movement
        screen.blit(self.image, self.rect)
        self.screen_constraint()

class Ball(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, ball_speed, paddle):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.smoothscale(self.image, (25, 25))
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.speed_x = ball_speed
        self.speed_y = ball_speed
        self.paddle = paddle
    
    def collisions(self):
        if self.rect.top <= play_field.top:
            self.speed_y *= -1
        if self.rect.left <= play_field.left or self.rect.right >= play_field.right:
            self.speed_x *= -1
        if self.rect.bottom >= play_field.bottom:
            pygame.quit()
            sys.exit()
            
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

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.collisions()
        screen.blit(self.image, self.rect)


# Initial Setup
pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 1360, 720
screen = pygame.display.set_mode((screen_width, screen_height))
speed = 5

# Play Field
play_field = pygame.Rect(0,0, screen_width/1.05, screen_height/1.05)
play_field.center = (screen_width/2, screen_height/2)

# Paddle Group
paddle = Paddle("paddle.png", play_field.width/2, play_field.height/1.02, speed)
paddle_sprite = pygame.sprite.GroupSingle()
paddle_sprite.add(paddle)

# Ball Group
ball = Ball("ball.png", screen_width/2, screen_height/2, speed, paddle_sprite)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

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
    
    paddle_sprite.update()
    ball_sprite.update()
    
    pygame.display.flip()
    clock.tick(60)
