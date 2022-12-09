import pygame, sys, random

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
        self.screen_constraint()


class Ball(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, ball_speed, paddle, target):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.smoothscale(self.image, (25, 25))
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.speed_x = ball_speed * random.choice([-1,1])
        self.speed_y = ball_speed * random.choice([-1,1])
        self.paddle = paddle
        self.target = target
        self.active = True
    
    def collisions(self):
        if self.active:
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
            
            if pygame.sprite.spritecollide(self, self.target, False):
                collision_target = pygame.sprite.spritecollide(self, self.target, True)[0].rect
                if abs(self.rect.bottom - collision_target.top) < 5 and self.speed_y > 0:
                    self.speed_y *= -1
                if abs(self.rect.top - collision_target.bottom) < 5 and self.speed_y < 0:
                    self.speed_y *= -1
                if abs(self.rect.left - collision_target.right) < 5 and self.speed_x < 0:
                    self.speed_x *= -1
                if abs(self.rect.right - collision_target.left) < 5 and self.speed_x > 0:
                    self.speed_x *= -1

            
            if self.rect.bottom >= play_field.bottom or len(self.target) == 0:
                self.active = False
            
    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
            self.paddle.update()
        else:
            game_over = base_font.render("GAME OVER", True, "white")
            game_over_rect = game_over.get_rect(center=(screen_width/2, screen_height/2))
            screen.blit(game_over, game_over_rect)
    
    def restart(self):
        self.active = True
        self.rect.center = play_field.width/2, play_field.height/2
        self.speed_x = ball_speed * random.choice([-1,1])
        self.speed_y = ball_speed * random.choice([-1,1])

class Target(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (80,10))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
    


class GameManager():
    def __init__(self, ball_group, paddle_group, target_group):
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.target_group = target_group

    def update(self):
        # Drawing the objects
        self.ball_group.draw(screen)
        self.paddle_group.draw(screen)
        self.target_group.draw(screen)

        # Updating Objects
        self.ball_group.update()


# Initial Setup
pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 1200, 800
screen = pygame.display.set_mode((screen_width, screen_height))
paddle_speed = 7
ball_speed = 5

# Rounds
base_font = pygame.font.Font(None, 30)
round_no = base_font.render("Round 1", False, "white")
round_rect = round_no.get_rect(center=(screen_width-100, 50))


# Play Field
play_field = pygame.Rect(0,0, screen_width/1.05, screen_height/1.05)
play_field.center = (screen_width/2, screen_height/2)

# Paddle Group
paddle = Paddle("paddle.png", screen_width/2, screen_height/1.05, paddle_speed)
paddle_group = pygame.sprite.GroupSingle()
paddle_group.add(paddle)

# Target Block Group
target_group = pygame.sprite.Group()
for column in range(100, play_field.width, 100):
    for row in range(100, int(play_field.height/2), 100):
        target = Target("glasspaddle2.png", column, row)
        target_group.add(target)


# Ball Group
ball = Ball("ball.png", screen_width/2, screen_height/2, ball_speed, paddle_group, target_group)
ball_group = pygame.sprite.GroupSingle()
ball_group.add(ball)

# Main Game
main_game = GameManager(ball_group, paddle_group, target_group)

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
            if event.key == pygame.K_RETURN:
                if not ball.active:
                    ball.restart()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                paddle.movement += paddle.speed
            if event.key == pygame.K_RIGHT:
                paddle.movement -= paddle.speed

    screen.fill((30,30,30))
    pygame.draw.rect(screen, "white", play_field, 1)
    
    main_game.update()
    screen.blit(round_no, round_rect)
    
    pygame.display.flip()
    clock.tick(60)
