"""
一箭又一箭 - 箭头类
负责箭头的数据表示、动画更新和绘制。
"""
import math
import pygame
from constants import (
    ARROW_COLORS, CELL_SIZE, CELL_PADDING, DIRECTIONS,
    DANGER, WARNING, FLY_SPEED, FLY_DURATION,
    SHAKE_DURATION, SHAKE_AMPLITUDE, HINT_DURATION,
)


class Arrow:
    """网格中的单格箭头"""

    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction  # 'up' / 'down' / 'left' / 'right'
        self.color = ARROW_COLORS[direction]

        # 飞行动画
        self.is_flying = False
        self.fly_progress = 0.0
        self.fly_dx = 0.0  # 飞行累计偏移（像素）
        self.fly_dy = 0.0

        # 碰撞晃动
        self.is_shaking = False
        self.shake_timer = 0.0
        self.shake_dx = 0.0

        # 提示高亮
        self.is_hint = False
        self.hint_timer = 0.0

        # 缩放（飞出时缩小）
        self.scale = 1.0

    def update(self, dt):
        """每帧更新动画，返回 True 表示飞出动画结束，可移除"""
        # 飞出
        if self.is_flying:
            self.fly_progress += dt / FLY_DURATION
            dx, dy = DIRECTIONS[self.direction]
            self.fly_dx += dx * FLY_SPEED * dt
            self.fly_dy += dy * FLY_SPEED * dt
            self.scale = max(0.2, 1.0 - self.fly_progress * 0.6)
            if self.fly_progress >= 1.0:
                return True

        # 碰撞晃动
        if self.is_shaking:
            self.shake_timer += dt
            t = self.shake_timer / SHAKE_DURATION
            if t >= 1.0:
                self.is_shaking = False
                self.shake_dx = 0.0
            else:
                # 正弦衰减晃动
                self.shake_dx = math.sin(t * math.pi * 6) * SHAKE_AMPLITUDE * (1 - t)

        # 提示高亮倒计时
        if self.is_hint:
            self.hint_timer -= dt
            if self.hint_timer <= 0:
                self.is_hint = False

        return False

    def start_fly(self):
        self.is_flying = True
        self.fly_progress = 0.0

    def start_shake(self):
        self.is_shaking = True
        self.shake_timer = 0.0

    def start_hint(self):
        self.is_hint = True
        self.hint_timer = HINT_DURATION

    def is_animating(self):
        return self.is_flying or self.is_shaking

    def draw(self, surface, board_x, board_y):
        """绘制箭头到 surface，board_x/board_y 为棋盘左上角像素坐标"""
        cx = board_x + self.col * CELL_SIZE + CELL_SIZE // 2 + self.fly_dx + self.shake_dx
        cy = board_y + self.row * CELL_SIZE + CELL_SIZE // 2 + self.fly_dy

        size = int((CELL_SIZE - CELL_PADDING * 2) * self.scale)
        half = size // 2

        # 根据方向生成三角形顶点
        if self.direction == 'right':
            points = [(cx - half, cy - half), (cx + half, cy), (cx - half, cy + half)]
        elif self.direction == 'left':
            points = [(cx + half, cy - half), (cx - half, cy), (cx + half, cy + half)]
        elif self.direction == 'up':
            points = [(cx - half, cy + half), (cx, cy - half), (cx + half, cy + half)]
        else:  # down
            points = [(cx - half, cy - half), (cx, cy + half), (cx + half, cy - half)]

        # 颜色：碰撞变红，提示闪烁金色
        color = self.color
        if self.is_shaking:
            color = DANGER
        elif self.is_hint and int(self.hint_timer * 8) % 2 == 0:
            color = WARNING

        pygame.draw.polygon(surface, color, points)

    def get_state(self):
        """返回可序列化的状态元组"""
        return (self.row, self.col, self.direction)
