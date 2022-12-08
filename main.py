import pygame, sys

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load("paddle.png")
        self.image = pygame.transform.scale(self.image, (160, 20))
        self.image_rect = self.image.get_rect(center=(x_pos, y_pos))
        self.speed = 3
    
    def update(self):
        self.image_rect.x += self.speed
        if self.image_rect.right >= play_field.right or self.image_rect.left <= play_field.left:
            self.speed *= -1

        screen.blit(self.image, self.image_rect)
    
class Ball(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load("ball.png")
        self.image = pygame.transform.smoothscale(self.image, (25, 25))

        self.image_rect = self.image.get_rect(center = (x_pos, y_pos))
        self.speed_x = 3
        self.speed_y = 3
    
    def update(self):
        self.image_rect.x += self.speed_x
        self.image_rect.y += self.speed_y
        if self.image_rect.top <= play_field.top or self.image_rect.bottom >= play_field.bottom:
            self.speed_y *= -1
        if self.image_rect.left <= play_field.left or self.image_rect.right >= play_field.right:
            self.speed_x *= -1
        
        screen.blit(self.image, self.image_rect)


# Initial Setup
pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 1000,800
screen = pygame.display.set_mode((screen_width, screen_height))

# Play Field
play_field = pygame.Rect(0,0, screen_width/1.05, screen_height/1.05)
play_field.center = (screen_width/2, screen_height/2)

# Paddle Group
paddle = Paddle(play_field.width/2, play_field.height/1.02)
paddle_group = pygame.sprite.Group()
paddle_group.add(paddle)

# Ball Group
ball = Ball(screen_width/2, screen_height/2)
ball_group = pygame.sprite.Group()
ball_group.add(ball)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((30,30,30))
    pygame.draw.rect(screen, "white", play_field, 1)
    paddle_group.update()
    ball_group.update()
    pygame.display.flip()
    clock.tick(60)
