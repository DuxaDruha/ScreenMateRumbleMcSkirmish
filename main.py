import pygame
import random
import win32api
import win32con
import win32gui
import os
import sys


# Sprites block
class RumbleMcShirmish(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.attack_animation = False
        self.sprites = []
        self.sprites.append(pygame.image.load("data/standing/1.png"))
        self.sprites.append(pygame.image.load("data/standing/2.png"))
        self.sprites.append(pygame.image.load("data/standing/3.png"))
        self.sprites.append(pygame.image.load("data/standing/4.png"))
        self.sprites.append(pygame.image.load("data/standing/5.png"))
        self.sprites.append(pygame.image.load("data/standing/6.png"))
        self.sprites.append(pygame.image.load("data/standing/7.png"))
        self.sprites.append(pygame.image.load("data/standing/8.png"))
        self.sprites.append(pygame.image.load("data/standing/9.png"))
        self.sprites.append(pygame.image.load("data/standing/10.png"))
        self.sprites.append(pygame.image.load("data/standing/11.png"))
        self.sprites.append(pygame.image.load("data/standing/12.png"))
        self.sprites.append(pygame.image.load("data/standing/13.png"))
        self.sprites.append(pygame.image.load("data/standing/14.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]
    
    def standing(self):
        self.standing_animation = True

    def update(self, speed):
        if self.standing_animation == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.standing_animation = False

        self.image = self.sprites[int(self.current_sprite)]


pygame.init()
clock = pygame.time.Clock()

# Sizes
screen_width = 104
screen_height = 120

# Taskbar hight
monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")
taskbarHight = monitor_area[3] - work_area[3]

# Window position
monitor = pygame.math.Vector2(pygame.display.Info().current_w, pygame.display.Info().current_h)
window_position = (monitor.x / 2, (monitor.y) - screen_height - taskbarHight)

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % window_position
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption("ScreenMateRumbleMcSkirmish")

# Code for window transparency and for top window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 0, 128), 0, win32con.LWA_COLORKEY)
hwnd = win32gui.GetForegroundWindow()
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, int(window_position[0]), int(window_position[1]), 0, 0, win32con.SWP_NOSIZE)

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
player = RumbleMcShirmish(0, 0)
moving_sprites.add(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    player.standing()

	# Drawing
    screen.fill((255, 0, 128))
    moving_sprites.draw(screen)
    moving_sprites.update(0.25)
    pygame.display.flip()
    clock.tick(60)