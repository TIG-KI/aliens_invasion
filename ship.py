import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, screen, ai_setting):
        super(Ship, self).__init__()
        #初始化飞船并设置其初始位置
        self.screen = screen
        self.ai_setting = ai_setting
        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('/home/null/Desktop/pygameExc/pictures/plane2.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将每搜新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #在飞船的属性center中存储最小数值
        self.center = float(self.rect.centerx)

        #移动标志
        self.moving_right = False
        self.moving_left = False

        #让飞船在屏幕上居中
        self.center = self.screen_rect.centerx

    def update(self):
        #根据移动标志调整飞船的位置
        #更新飞船的center值，而不是rect(使飞船的移动范围在屏幕的左右边框之内)
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_setting.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_setting.ship_speed_factor
        
        #根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        #在指定位置绘制飞船
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        #让飞船在屏幕上居中(飞船与外星人相撞之后重置飞船的位置)
        self.center = self.screen_rect.centerx

