import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #表示单个外星人的类

    def __init__(self, ai_setting, screen):
        #初始化外星人并设置其起始位置
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_setting = ai_setting

        #加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('/home/null/Desktop/pygameExc/pictures/alien2.png')
        self.rect = self.image.get_rect()

        #每个外星人最初都寄在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #储存外星人的准确位置
        self.x = float(self.rect.x)

        #外星人设置(飞行速度)
        self.alien_speed_factor = 1

    def  check_edges(self):
        #如果alien 处于屏幕边缘 就返回True
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self):
        #向左向右移动外星人
        self.x += (self.ai_setting.alien_speed_factor * self.ai_setting.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        #在指定位置绘制外星人
        self.screen.blit(self.image, self.rect)