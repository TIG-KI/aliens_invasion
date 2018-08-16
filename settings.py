class Settings():
    #储存外星人入侵的所有设置的类
    def __init__(self):
        '''初始化游戏的静态设置'''
        #初始化屏幕设置
        self.screen_width = 750
        self.screen_height = 900
        self.bg_color = (230, 230, 230)

        #添加属性用于控制飞船速度，控制飞船在每次循环移动的距离
        # self.ship_speed_factor = 1.5
        # #将飞船的数量限制在3个
        self.ship_limit = 3

        #子弹设置
        #self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        #储存所允许的最大的子弹数
        self.bullets_allowed = 3

        #外星人设置
        #self.alien_speed_factor = 1
        self.fleet_drop_speed = 40
        # fleet_direction为1 表示向右移，为-1表示向左移
        #self.fleet_direction = 1

        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        #fleet_direction为1表示向右，为-1表示向左
        self.fleet_direction = 1

        self.alien_point = 50

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        