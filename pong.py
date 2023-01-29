import pygame
import math
import time
import os
from pygame import mixer


class paddle:

    def __init__(self, window, height=200, width=20, x=0, y=0, color=(255, 255, 255)):
        self.window = window
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.ini_x = x
        self.ini_y = y
        self.x_vel = 0
        self.y_vel = 0
        self.y_vel_ref = 10
        self.color = color
        self.el_rect = self.rect()
        self.score = 0

    def rect(self):
        self.el_rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.el_rect)

    def stop(self):
        self.x_vel = 0
        self.y_vel = 0

    def init_pos(self):
        self.x = self.ini_x
        self.y = self.ini_y
        self.stop()

    def out_of_bounds(self):
        if self.x <= 0:
            return 1
        elif self.x >= window.get_width() - self.width:
            return 2
        elif self.y <= 0:
            return 3
        elif self.y >= window.get_height() - self.height:
            return 4
        else:
            return 0

    def update_pos(self):
        self.x += self.x_vel
        self.x = max(self.x, 0)
        self.x = min(self.x, window.get_width() - self.width)
        self.y += self.y_vel
        self.y = max(self.y, 0)
        self.y = min(self.y, window.get_height() - self.height)


class ball(paddle):

    def __init__(self, window, height=15, width=15, x=0, y=0,
                 color=(255, 255, 255)):
        paddle.__init__(self, window, height, width, x, y, color)
        self.max_vel = 20
        self.thrown = False
        self.shots_nr = 0
        self.shots_inc = 5
        self.x_vel_shot = 2.5
        self.x_vel_ini = 10

    def stop(self):
        paddle.stop(self)
        self.shots_nr = 0

    def stick(self, obj, x=0, y=0, left=True):
        if left is True:
            self.x = obj.x + x - self.width
        else:
            self.x = obj.x + obj.width + x
        self.y = obj.y + y + self.height

    def update_pos(self, bounce_x=False, bounce_y=True):
        self.x += self.x_vel
        if bounce_x is True:
            if self.x <= 0 or self.x >= window.get_width() - self.width:
                self.x_vel = - self.x_vel
            self.x = max(self.x, 0)
            self.x = min(self.x, window.get_width() - self.width)

        self.y += self.y_vel
        if bounce_y is True:
            if self.y <= 0 or self.y >= window.get_height() - self.height:
                ball_1.y_vel = - ball_1.y_vel
                sound_wall = mixer.Sound('wall_2.wav')
                sound_wall.play()
            self.y = max(self.y, 0)
            self.y = min(self.y, window.get_height() - self.height)

    def increase_x_speed(self):
        if self.x_vel != 0:
            self.x_vel = self.x_vel / abs(self.x_vel) * (self.x_vel_ini + self.shots_nr // self.shots_inc * self.x_vel_shot)

    def collide(self, obj, left=False):
        if (self.y >= obj.y and self.y <= obj.y + obj.height) or \
           (self.y + self.height >= obj.y and \
            self.y + self.height <= obj.y + obj.height):
            if left is True:
                if self.x + self.width >= obj.x:
                    return True
                else:
                    return False
            elif self.x_vel < 0:
                if self.x <= obj.x + obj.width:
                    return True
                else:
                    return False
        else:
            return False

    def update_collide(self, obj, left=False):
        if self.collide(obj, left) and self.x_vel != 0:
            sound_collision = mixer.Sound('wall.wav')
            sound_collision.play()
            self.shots_nr += 1
            self.increase_x_speed()
            reflect_angl = math.atan(self.y_vel/self.x_vel) + math.pi / 4 * (self.y + self.height / 2 - obj.y - obj.height / 2) / (obj.height / 2)
            self.x_vel = - self.x_vel
            self.y_vel = - (math.tan(reflect_angl) * self.x_vel)
            self.y_vel = max(self.y_vel, -self.max_vel)
            self.y_vel = min(self.y_vel, self.max_vel)

    def get_angle(self):
        if self.x_vel == 0:
            return 0
        else:
            return math.atan(self.y_vel/self.x_vel)
    
def print_score(window, color, x, y, score=0):
    score_digits = list(str(score))
    for digit in score_digits[::-1]:
        print_digit(window, color, x, y, int(digit))
        x -= 70

def print_digit(window, color, x, y, digit=0):
    dict_seg = {0:(1, 1, 1, 1, 1, 1, 0), 1:(0, 0, 0, 1, 1, 0, 0),
                2:(0, 1, 1, 0, 1, 1, 1), 3:(0, 0, 1, 1, 1, 1, 1),
                4:(1, 0, 0, 1, 1, 0, 1), 5:(1, 0, 1, 1, 0, 1, 1),
                6:(1, 1, 1, 1, 0, 0, 1), 7:(0, 0, 0, 1, 1, 1, 0),
                8:(1, 1, 1, 1, 1, 1, 1), 9:(1, 0, 0, 1, 1, 1, 1)}
    long_height = 80
    short_height = 40
    width = 30
    thick = 10
    list_rect = [pygame.Rect(x, y, thick, short_height),
                 pygame.Rect(x, y + short_height, thick, long_height),
                 pygame.Rect(x, y + short_height + long_height - thick,
                             width + 2*thick, thick),
                 pygame.Rect(x + thick + width, y + short_height, thick,
                             long_height),
                 pygame.Rect(x + thick + width, y, thick, short_height),
                 pygame.Rect(x, y, width + 2*thick, thick),
                 pygame.Rect(x, y + short_height, width + 2*thick, thick)]
    
    for i, seg in enumerate(dict_seg[digit]):
            if seg == 1:
                pygame.draw.rect(window, color, list_rect[i])

os.environ['SDL_VIDEO_CENTERED'] = '1'
                
pygame.init()

pygame.display.set_caption('Pong')

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

window_height = 960
window_width = 1280
resolution = (window_width, window_height)
black = (0, 0, 0)
white = (255, 255, 255)

font = pygame.font.Font('freesansbold.ttf', 25)
font2 = pygame.font.Font('freesansbold.ttf', 50)

image = pygame.image.load('Image002.png')

window = pygame.display.set_mode(resolution)

paddle_1 = paddle(window, x=(window_width - 20 - 20), y=(window_height // 2 - 200 // 2))
paddle_2 = paddle(window, x=20, y=(window_height // 2 - 200 // 2))
ball_1 = ball(window)
ball_1.stick(paddle_1)

paddle_1_y_pos_prev = window_height // 2 - paddle_1.height // 2
paddle_1_y_p_prev = window_height // 2 - paddle_1.height // 2

let_width = 5
let_height = 30
let_gap = 15
pos_y_let = 0
pos_x_let = window_width // 2 - let_width // 2

active_paddle = paddle_1

show_fps = False

launched = True
while launched:
    start_time = time.perf_counter()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle_2.y_vel = - paddle_2.y_vel_ref
            elif event.key == pygame.K_s:
                paddle_2.y_vel = paddle_2.y_vel_ref
            elif event.key == pygame.K_SPACE:
                if ball_1.thrown is False:
                    paddle_2_y_pos_prev = paddle_2.y
            elif event.key == pygame.K_ESCAPE:
                launched = False
            elif event.key == pygame.K_F2:
                show_fps = not show_fps
            elif event.key == pygame.K_F1:
                paddle_1.score = 0
                paddle_2.score = 0
                ball_1.init_pos()
                ball_1.thrown = False
                paddle_1.init_pos()
                paddle_2.init_pos()
                active_paddle = paddle_1
                ball_1.stick(paddle_1)
            elif event.key == pygame.K_KP_PLUS:
                paddle_2.y_vel_ref += 2
            elif event.key == pygame.K_KP_MINUS:
                paddle_2.y_vel_ref -= 2
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                paddle_2.stop()
            elif event.key == pygame.K_SPACE:
                if ball_1.thrown is False and active_paddle is paddle_2:
                    ball_1.x_vel = ball_1.x_vel_ini
                    ball_1.y_vel = (paddle_2.y - paddle_2_y_pos_prev) / 20
                    ball_1.thrown = True
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            paddle_1.y = pos[1] - paddle_1.height // 2
            if ball_1.thrown is False and active_paddle is paddle_1:
                if paddle_1.y > 0 and paddle_1.y + paddle_1.height < window_height:
                    ball_1.stick(paddle_1)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 :
                if ball_1.thrown is False:
                    paddle_1_y_pos_prev = paddle_1.y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if ball_1.thrown is False and active_paddle is paddle_1:
                    ball_1.x_vel = -ball_1.x_vel_ini
                    ball_1.y_vel = (paddle_1.y - paddle_1_y_pos_prev) / 20
                    ball_1.thrown = True
            
    window.fill(black)

    paddle_1.update_pos()
    paddle_2.update_pos()
    ball_1.update_pos()

    if ball_1.thrown is False and active_paddle is paddle_2:
        ball_1.stick(paddle_2, left=False)

    if ball_1.out_of_bounds() == 1 or ball_1.out_of_bounds() == 2:
        sound_out = mixer.Sound('lost.wav')
        sound_out.play()
        if ball_1.out_of_bounds() == 1:
            paddle_1.score += 1
        else:
            paddle_2.score += 1
        #paddle_1.init_pos()
        #paddle_2.init_pos()
        ball_1.init_pos()
        ball_1.thrown = False
        if active_paddle is paddle_1:
            active_paddle = paddle_2
            ball_1.stick(paddle_2, left=False)
        else:
            active_paddle = paddle_1
            ball_1.stick(paddle_1)
    else:
        angle = ball_1.get_angle()
        ball_1.update_collide(paddle_1, left=True)
        ball_1.update_collide(paddle_2)

    paddle_1.rect()
    paddle_2.rect()
    ball_1.rect()
  
    pos_y_let = 0
    pos_x_let = window_width // 2 - let_width // 2
    
    while pos_y_let < window_height:
        let_rect = pygame.Rect(pos_x_let, pos_y_let, let_width, let_height)
        pygame.draw.rect(window, white, let_rect)
        pos_y_let += let_height + let_gap

##    text_pos = font.render(f'Position of the ball : {ball_1.x}, {ball_1.y}', True, white)
##    text_vel = font.render(f'Velocity of the ball : {ball_1.x_vel}, {ball_1.y_vel}', True, white)
##    text_out = font.render(f'Out : {ball_1.out_of_bounds()}', True, white)
##    text_vel_prev = font.render(f'New velocity of the ball : {ball_1.x_vel}, {new_ball_y_v}', True, white)
##    text_angl = font.render(f'Angle : {angle}', True, white)
##    text_ref_angl = font.render(f'Reflected angle : {reflect_angl}', True, white)
        
    text_shots = font.render(f'Nr shots : {ball_1.shots_nr}', True, white)
##    text_score_1 = font2.render(f'{paddle_1.score}', True, white)
##    text_score_2 = font2.render(f'{paddle_2.score}', True, white)
    print_score(window, white, int(window.get_width()*3/4 - 20), 50, paddle_1.score)
    print_score(window, white, int(window.get_width()*1/4 - 20), 50, paddle_2.score)

##    window.blit(text_pos, (10,10))
##    window.blit(text_vel, (10,70))
##    window.blit(text_out, (10,70))
##    window.blit(text_vel_prev, (10,70))
##    window.blit(text_angl, (10,100))
##    window.blit(text_ref_angl, (10,130))
    
    window.blit(text_shots, (10,10))
##    window.blit(text_score_1, (int(window.get_width()*3/4), window.get_height() - 60))
##    window.blit(text_score_2, (int(window.get_width()*1/4), window.get_height() - 60))
##    window.blit(image, (0, 0))
    
    paddle_1.draw()
    paddle_2.draw()
    ball_1.draw()
    end_time = time.perf_counter()
    time.sleep(max(0,0.0166 -(end_time-start_time)))
    end_time = time.perf_counter()
    if show_fps is True:
        text_fps = font.render(f'FPS : {round(1/(end_time - start_time),0)}', True, white)
        window.blit(text_fps, (10,40))
    pygame.display.update()
