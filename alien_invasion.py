import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    
    pygame.init()
    ai_setting = Settings()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    #设置背景颜色
    bg_color = (250, 250, 250)

    #创建一艘飞船
    ship = Ship(screen, ai_setting)

    # #创建一个外星人的实例
    # alien = Alien(ai_setting,screen)

    #创建一个用于存储子弹的编组,一个外星人编组
    bullets = Group()
    aliens = Group()

    #创建外星人群
    gf.create_fleet(ai_setting, screen, ship, aliens)

    #创建gamestats实例
    stats = GameStats(ai_setting)

    #创建一个button实例
    play_button = Button(ai_setting, screen, 'Play')

    #创建一个scoreBoard()实例
    sb = Scoreboard(ai_setting, screen, stats)

    #开始游戏主循环
    while True:

        gf.check_events(ai_setting, screen, ship, bullets, stats, play_button, aliens)

        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_setting, screen, ship, stats, sb)
            gf.update_aliens(ai_setting, aliens, ship, bullets, stats, screen)
            #print(len(bullets)), 打印屏幕上子弹的个数
        gf.update_screen(ai_setting, screen, ship, bullets, aliens, play_button, stats, sb)     

run_game()