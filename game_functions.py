import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_setting, screen, ship, bullets, stats, aliens):

    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_r and not stats.game_active:
        #使光标隐藏
        pygame.mouse.set_visible(False)

        stats.game_active = True
        stats.ship_left = ai_setting.ship_limit

        #删除屏幕上的aliens和bullets
        aliens.empty()
        bullets.empty()
        #创建新的aliens 并使ship居中
        create_fleet(ai_setting, screen, ship, aliens)
        ship.center_ship()

    # elif event.key == pygame.K_p and:
    #     stats.game_active = True
    
    #创建一颗子弹
    elif event.key == pygame.K_SPACE:
        #创建新子弹并将其加入到编组bullets中
        if len(bullets) < ai_setting.bullets_allowed:
            new_bullet = Bullet(ai_setting, screen, ship)
            bullets.add(new_bullet)
    
    #设置关闭游戏的快捷键
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_setting, screen, ship, bullets, stats, play_button, aliens):
    #响应按键和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_setting, screen, ship, bullets, stats, aliens)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, stats, play_button, mouse_x, mouse_y, aliens, bullets, ship, screen)

def check_play_button(ai_setting, stats, play_button, mouse_x, mouse_y, aliens, bullets, ship, screen):
    #在玩家单机play按钮时开始新游戏(只有点击了button区域并且当前stats.game_active 的值为false 时才能重新开始)
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and  not stats.game_active:
        #重置游戏设置
        ai_setting.initialize_dynamic_settings

        #当游戏开始时将光标隐藏
        pygame.mouse.set_visible(False)

        #重置游戏统计
        stats.reset_stats()
        stats.game_active = True

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人并让飞船居中
        create_fleet(ai_setting, screen, ship, aliens)
        ship.center_ship()    

def check_fleet_edges(ai_setting, aliens):
    #外星人到达边缘采取的措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            break

def change_fleet_direction(ai_setting, aliens):
    #将整群外星人下移，并改变他们的方向
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1
            
def update_screen(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb):
    #更新屏幕上的图像，并切换到新的屏幕
    #每次循环都会重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    #让最近绘制的屏幕可见
    pygame.display.flip()

    #显示得分
    sb.show_score()

    #如果游戏处于非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    #让最近绘制的button可见
    pygame.display.flip()

def update_bullets(bullets, aliens, ai_setting, screen, ship, stats, sb):
    #更新子弹位置，删除已消失的子弹
    #更新子弹的位置
    bullets.update()

    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(bullets, aliens, ai_setting, screen, ship, stats, sb)

def check_bullet_alien_collisions(bullets, aliens, ai_setting, screen, ship, stats, sb):
    #检查子弹是否击中了外星人
    #如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
       stats.score += ai_setting.alien_point
       sb.prep_score() 

    #检查编组aliens是否为空，为空就调用create_fleet()
    if len(aliens) == 0:
        #删除现有的子弹并新建一批外星人
        bullets.empty()
        ai_setting.increase_speed()
        create_fleet(ai_setting, screen, ship, aliens)

def ship_hit(ai_setting, stats, screen, ship, aliens, bullets):
    #响应被外星人撞到的飞船

    #检查飞的剩余数量如果大于零剩余数量减一 否则 game_active = False 游戏界面不再刷新
    if stats.ship_left > 0:
        #将ship_left减1
        stats.ship_left -= 1
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    #清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    #创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_setting, screen, ship, aliens)
    ship.center_ship()

    #暂停
    sleep(0.5)

    print(stats.ship_left)

def check_aliens_bottom(ai_setting, stats, screen, ship, aliens, bullets):
    #检查外星人是否到达了底端
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被外星人被撞到了一样处理
            ship_hit(ai_setting, stats, screen, ship, aliens, bullets)

def update_aliens(ai_setting, aliens, ship, bullets, stats, screen):
    #更新外星人群中所有外星人的位置
    #检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    check_fleet_edges(ai_setting, aliens)
    aliens.update()

    #检查飞船与外星人的碰撞(函数遍历整个aliens 编组并返回以一个与飞船发生碰撞的外星人，如果没有发生碰撞 函数将返回None)
    if pygame.sprite.spritecollideany(ship, aliens):
        #print("ship bit")
        ship_hit(ai_setting, stats, screen, ship, aliens, bullets)

    #检查外星人是否到达屏幕底部
    check_aliens_bottom(ai_setting, stats, screen, ship, aliens, bullets)

def get_number_aliens_x(ai_setting, alien_width):
    #计算每行可容纳多少个外星人
    available_space_x = ai_setting.screen_width - (alien_width * 2)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_setting, ship_height, alien_height):
    #计算屏幕可以容纳多少行外星人
    available_space_y = (ai_setting.screen_height - (3 * alien_height) - ship_height)
    number_rows = int( available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_setting, screen, aliens, alien_number, row_number):
    #创建一个外星人并将其放在当前行
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_setting, screen, ship, aliens):
    #创建一个外星人，并计算一行可以容纳多少个外星人   
    alien = Alien(ai_setting, screen)
    number_aliens_x = get_number_aliens_x(ai_setting, alien.rect.width)
    number_rows = get_number_rows(ai_setting, ship.rect.height, alien.rect.height)

    #创建外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_setting, screen, aliens, alien_number, row_number)
        
        