"""
一箭又一箭 - 常量配置
"""
import os
import pygame

# ===== 窗口 =====
WIDTH = 800
HEIGHT = 900
FPS = 60

# ===== 颜色 =====
BG_COLOR = (30, 30, 46)
PANEL_COLOR = (45, 45, 65)
GRID_COLOR = (60, 60, 85)
CELL_COLOR = (50, 50, 72)
TEXT_COLOR = (235, 235, 245)
TEXT_DIM = (160, 160, 180)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (90, 150, 200)
BUTTON_DISABLED = (80, 80, 100)
ACCENT = (100, 200, 150)
DANGER = (220, 80, 80)
WARNING = (230, 180, 60)

# 箭头四方向颜色
ARROW_COLORS = {
    'up': (80, 200, 120),
    'down': (80, 150, 220),
    'left': (230, 150, 70),
    'right': (200, 100, 200),
}

# 方向向量 (dx, dy) — dx 对应列变化，dy 对应行变化
DIRECTIONS = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0),
}

# ===== 棋盘 =====
CELL_SIZE = 56
CELL_PADDING = 4

# ===== 动画参数 =====
FLY_SPEED = 500        # 飞出速度 像素/秒
FLY_DURATION = 0.35    # 飞出动画时长 秒
SHAKE_DURATION = 0.3   # 碰撞晃动时长
SHAKE_AMPLITUDE = 8    # 晃动幅度
HINT_DURATION = 2.0    # 提示高亮时长

# ===== 存档 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "saves")
SAVE_FILE = os.path.join(SAVE_DIR, "save.json")


def get_font(size):
    """加载支持中文的字体，找不到则用默认字体"""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",   # 黑体
        "C:/Windows/Fonts/simsun.ttc",   # 宋体
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return pygame.font.Font(fp, size)
    return pygame.font.Font(None, size)
