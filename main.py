import pygame
import win32api
import win32con
import win32gui
import os
from scripts.load import appendAnimation
import time
from random import randint, choice


pygame.init()


class Rumble(object):
    def __init__(self, coorX, coorY):
        
        self.x = coorX
        self.y = coorY
        self.targetX = self.x
        self.time0 = time.time()
        self.speed = 2.5
        self.running = True
        self.direction = 0
        self.isLeft = False
        
        # АНИМАЦИЯ СТОЙКИ НАЧАЛО
        self.standing_animation = False
        
        self.standing_sprites = []
        appendAnimation(self.standing_sprites, "data/standing/", 14, '.png')
        self.current_standing_sprite = 0
        
        self.image = self.standing_sprites[self.current_standing_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        # АНИМАЦИЯ СТОЙКИ КОНЕЦ
        
        
        # АНИМАЦИЯ БЕГА НАЧАЛО
        self.running_animation = False
        
        self.running_sprites = []
        appendAnimation(self.running_sprites, "data/running/", 8, '.gif')
        self.current_running_sprite = 0
        
        self.image = self.running_sprites[self.current_running_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        # АНИМАЦИЯ БЕГА КОНЕЦ
        
    def animation(self):
        if self.running and self.x != self.targetX:
            self.standing_animation = False
            self.running_animation = True
        else:
            self.standing_animation = True
            self.running_animation = False
        

    def move(self):
        time1 = time.time()
        if time1 - self.time0 >= randint(12, 30):
            dist = randint(400, 700)
            self.direction = choice([-1, 1])
            
            self.targetX = self.x + dist * self.direction
            self.time0 = time1
        
        if self.direction == 1:
            if self.x > monitor.x:
                self.x = 0 - 152
                self.targetX -= monitor.x
            else:
                if self.x < self.targetX:
                    self.x += self.speed
                    self.running = True
                    if self.x > self.targetX:
                        self.x = self.targetX
                        self.running = False
        else:
            if self.x < 0 - 152:
                self.x = monitor.x
                self.targetX += monitor.x
            else:
                if self.x > self.targetX:
                    self.x -= self.speed
                    self.running = True
                    if self.x < self.targetX:
                        self.x = self.targetX
                        self.running = False
            
        

    def draw(self, surface, speed):
        if self.standing_animation == True:
            self.current_standing_sprite += speed
            if int(self.current_standing_sprite) >= len(self.standing_sprites):
                self.current_standing_sprite = 0
            self.image = self.standing_sprites[int(self.current_standing_sprite)]
        elif self.running_animation == True:
            self.current_running_sprite += speed
            if int(self.current_running_sprite) >= len(self.running_sprites):
                self.current_running_sprite = 0
            self.image = self.running_sprites[int(self.current_running_sprite)]


        key = pygame.key.get_pressed()
        if self.direction == -1:
            surface.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
            self.isLeft = True
        if self.direction == 1:
            surface.blit(self.image, (self.x, self.y))
            self.isLeft = False
        elif self.isLeft:
            surface.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
        else:
            surface.blit(self.image, (self.x, self.y))
                


# Taskbar hight
monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")
taskbarHight = monitor_area[3] - work_area[3]
monitor = pygame.math.Vector2(pygame.display.Info().current_w, pygame.display.Info().current_h)

# Sizes
screen_width = monitor.x
screen_height = 144
# Window position
monitor = pygame.math.Vector2(pygame.display.Info().current_w, pygame.display.Info().current_h)
window_position = (int(monitor.x - screen_width) / 2, (monitor.y) - screen_height - taskbarHight)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % window_position
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
fuchsia = (255, 0, 128)  # Transparency color
dark_red = (139, 0, 0)
pygame.display.set_caption("ScreenMateRumbleMcSkirmish")
# set icon
programIcon = pygame.image.load('data/imgs/logo.png')
pygame.display.set_icon(programIcon)


# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
hwnd = win32gui.GetForegroundWindow()
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, int(window_position[0]), int(window_position[1]), 0, 0, win32con.SWP_NOSIZE)


rumble = Rumble(randint(152, int(monitor.x) - 152), 0)
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    rumble.move()
    rumble.animation()
    

    screen.fill(fuchsia)
    rumble.draw(screen, 0.25)
    pygame.display.update()

    clock.tick(60)